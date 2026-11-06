"""MultiADS (ICCV 2025, official code in third_party/MultiADS) trained and evaluated on the bridge data with this repository's protocol.

Training follows the official train.py: frozen open_clip ViT-L-14-336 at 518, one linear layer per feature level (6/12/18/24),
text embeddings for [good, crack, corrosion, spalling, efflorescence] built with the official prompt-ensemble recipe (state
phrases x 35 templates, averaged), pixel softmax over the 5 classes at temperature 0.01, loss = (focal + binary dice on the summed
defect probability) / 2 averaged over levels, Adam lr 1e-3 betas (0.5, 0.999), batch 4, 10 epochs, last epoch used (the official
code has no validation-based selection).  The single-label target is the flattened RGB mask (red crack, green spalling, blue
corrosion, yellow efflorescence), nearest to 518.  No mosaic augmentation (the official VisA / MPDD loaders have none either).

Evaluation follows the official test.py (zero-shot mode): logits x 100, image score = sum of the defect-class probabilities of
the global embedding, binary map = sum over levels of the summed defect probabilities (divided by 4 here to stay in [0, 1]), no
smoothing.  Per-class map = mean over levels of that class's softmax probability.  Output layout matches eval_nuisance.py
(maps/, typed/ [4,518,518] in the order crack/corrosion/spalling/efflorescence, residual/ = binary map, predictions.csv).

  python multiads_bridge.py train --out runs/ext-multiads
  python multiads_bridge.py eval --checkpoint runs/ext-multiads/epoch_10.pth --out runs/ext-multiads/val [--data D --split test]
"""
import argparse,csv,hashlib,json,random,sys
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from tqdm import tqdm
HERE=Path(__file__).resolve().parent; THIRD=str(HERE/'third_party'/'MultiADS'); sys.path.insert(0,THIRD)
import open_clip
from model import LinearLayer
from loss import FocalLoss,BinaryDiceLoss
sys.path.remove(THIRD)

OBJ='concrete bridge surface'; SIZE=518; LAYERS=[6,12,18,24]
PALETTE={(255,0,0):1,(0,0,255):2,(0,255,0):3,(255,255,0):4}   # crack, corrosion, spalling, efflorescence (index 0 = good)
STATES=[
 ['{}','flawless {}','perfect {}','unblemished {}','{} without flaw','{} without defect','{} without damage','{} in pristine condition','{} with no imperfections','{} of ideal quality'],
 ['{} with a crack defect','a crack on {}','visible crack in {}','{} with thin crack lines','crack detected in {}','{} has cracks'],
 ['{} with a corrosion defect','{} has rust stains','rust spots on {}','visible rust on {}','{} shows exposed corroded rebar','{} affected by corrosion'],
 ['{} with a spalling defect','spalling on {}','{} with broken off concrete','{} has spalled areas','concrete loss detected on {}','{} shows spalling damage'],
 ['{} with an efflorescence defect','efflorescence on {}','{} with white salt deposits','{} has efflorescence stains','white mineral deposits on {}','{} shows efflorescence'],
]
TEMPLATES=['a bad photo of a {}.','a low resolution photo of the {}.','a bad photo of the {}.','a cropped photo of the {}.','a bright photo of a {}.','a dark photo of the {}.','a photo of my {}.','a photo of the cool {}.','a close-up photo of a {}.','a black and white photo of the {}.','a bright photo of the {}.','a cropped photo of a {}.','a jpeg corrupted photo of a {}.','a blurry photo of the {}.','a photo of the {}.','a good photo of the {}.','a photo of one {}.','a close-up photo of the {}.','a photo of a {}.','a low resolution photo of a {}.','a photo of a large {}.','a blurry photo of a {}.','a jpeg corrupted photo of the {}.','a good photo of a {}.','a photo of the small {}.','a photo of the large {}.','a black and white photo of a {}.','a dark photo of a {}.','a photo of a cool {}.','a photo of a small {}.','there is a {} in the scene.','there is the {} in the scene.','this is a {} in the scene.','this is the {} in the scene.','this is one {} in the scene.']

def text_features(model,tokenizer,device):
 """[D, 5] as prompts/new_prompt_ensemble_mpdd.py: per state, mean of the normalised embeddings of all phrase x template sentences."""
 feats=[]
 for state in STATES:
  sent=tokenizer([t.format(s.format(OBJ)) for s in state for t in TEMPLATES]).to(device); e=model.encode_text(sent); e=e/e.norm(dim=-1,keepdim=True); e=e.mean(0); feats.append(e/e.norm())
 return torch.stack(feats,dim=1)

class Tiles(torch.utils.data.Dataset):
 def __init__(self,root,split,transform,masks=True):
  self.root=Path(root)/split; self.transform=transform; self.masks=masks
  with (Path(root)/(split+'_manifest.csv')).open() as f: self.rows=list(csv.DictReader(f))
 def __len__(self): return len(self.rows)
 def __getitem__(self,i):
  r=self.rows[i]; im=self.transform(Image.open(self.root/r['image_path']).convert('RGB')); m=torch.zeros(SIZE,SIZE,dtype=torch.long)
  if self.masks and r['category']=='annotated':
   rgb=np.asarray(Image.open(self.root/r['mask_path']).convert('RGB').resize((SIZE,SIZE),Image.Resampling.NEAREST)); idx=np.zeros((SIZE,SIZE),np.int64)
   for c,k in PALETTE.items(): idx[(rgb==np.array(c,np.uint8)).all(-1)]=k
   m=torch.from_numpy(idx)
  return im,m,i

def build(device):
 model,_,preprocess=open_clip.create_model_and_transforms('ViT-L-14-336',SIZE,pretrained='openai'); model.to(device).eval(); cfg=json.load(open(THIRD+'/open_clip/model_configs/ViT-L-14-336.json'))
 return model,preprocess,open_clip.get_tokenizer('ViT-L-14-336'),LinearLayer(cfg['vision_cfg']['width'],cfg['embed_dim'],len(LAYERS),'ViT-L-14-336').to(device)

def level_maps(model,layer,img,text,scale):
 """Per-level 5-class softmax maps [B,5,518,518] and the global embedding."""
 with torch.no_grad(): g,tokens=model.encode_image(img,LAYERS)
 tokens=layer(tokens); maps=[]
 for t in tokens:
  t=t/t.norm(dim=-1,keepdim=True); a=(t@text)*scale; B,L,C=a.shape; H=int(np.sqrt(L))
  maps.append(torch.softmax(F.interpolate(a.permute(0,2,1).view(B,C,H,H),size=SIZE,mode='bilinear',align_corners=True),dim=1))
 return maps,g

def train(a):
 torch.manual_seed(a.seed); torch.cuda.manual_seed_all(a.seed); np.random.seed(a.seed); random.seed(a.seed)
 device='cuda'; out=Path(a.out); out.mkdir(parents=True,exist_ok=True); model,preprocess,tokenizer,layer=build(device)
 data=Tiles(a.data,'train',preprocess)
 if a.annotated_only: data.rows=[r for r in data.rows if r['category']=='annotated']
 loader=torch.utils.data.DataLoader(data,batch_size=a.batch_size,shuffle=True,num_workers=4,drop_last=False)
 opt=torch.optim.Adam(layer.parameters(),lr=a.lr,betas=(.5,.999)); focal=FocalLoss(); dice=BinaryDiceLoss()
 with torch.amp.autocast('cuda'),torch.no_grad(): text=text_features(model,tokenizer,device)
 print('trainable parameters: %.3f M, train images %d'%(sum(p.numel() for p in layer.parameters())/1e6,len(data)),flush=True)
 (out/'config.json').write_text(json.dumps({**vars(a),'object':OBJ,'states':STATES,'layers':LAYERS},indent=2))
 for epoch in range(a.epochs):
  losses=[]
  for img,mask,_ in tqdm(loader,desc=f'epoch {epoch+1}/{a.epochs}'):
   img=img.to(device); mask=mask.to(device)
   with torch.amp.autocast('cuda'): maps,_=level_maps(model,layer,img,text,1/.01)
   loss=sum((focal(m,mask)+dice(m[:,1:].sum(1),(mask>0).float()))/2. for m in maps)/len(maps)
   opt.zero_grad(); loss.backward(); opt.step(); losses.append(loss.item())
  print('epoch %d/%d loss=%.4f'%(epoch+1,a.epochs,float(np.mean(losses))),flush=True); torch.save({'trainable_linearlayer':layer.state_dict()},out/f'epoch_{epoch+1}.pth')

def evaluate(a):
 device='cuda'; out=Path(a.out)
 for d in ('maps','typed','residual'): (out/d).mkdir(parents=True,exist_ok=True)
 model,preprocess,tokenizer,layer=build(device); layer.load_state_dict(torch.load(a.checkpoint,map_location=device)['trainable_linearlayer']); layer.eval()
 data=Tiles(a.data,a.split,preprocess,masks=False); records=[]
 with torch.no_grad(),torch.amp.autocast('cuda'):
  text=text_features(model,tokenizer,device)
  for i in tqdm(range(len(data)),desc=a.split):
   r=data.rows[i]; img=data[i][0].unsqueeze(0).to(device); maps,g=level_maps(model,layer,img,text,100.); g=g/g.norm(dim=-1,keepdim=True)
   score=float(((g@text)*100.).softmax(-1)[0,1:].sum()); m=torch.stack(maps).float().mean(0)[0]; b=m[1:].sum(0)
   np.save(out/'maps'/(r['sample']+'.npy'),b.cpu().numpy().astype(np.float32)); np.save(out/'typed'/(r['sample']+'.npy'),m[1:].half().cpu().numpy()); np.save(out/'residual'/(r['sample']+'.npy'),b.half().cpu().numpy())
   records.append({'sample':r['sample'],'label':int(r['category']=='annotated'),'score':score})
 with (out/'predictions.csv').open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=records[0]); w.writeheader(); w.writerows(records)
 (out/'provenance.json').write_text(json.dumps({'method':'MultiADS (official code, linear layers trained on CODEBRIM train, 10 epochs, last epoch)','checkpoint':a.checkpoint,'sha256':hashlib.sha256(Path(a.checkpoint).read_bytes()).hexdigest(),'data':a.data,'split':a.split,'count':len(records)},indent=2))
 print('INFERENCE_COMPLETE',len(records),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('mode',choices=['train','eval']); p.add_argument('--out',required=True); p.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); p.add_argument('--split',default='val')
 p.add_argument('--checkpoint'); p.add_argument('--epochs',type=int,default=10); p.add_argument('--batch-size',type=int,default=4); p.add_argument('--lr',type=float,default=1e-3); p.add_argument('--seed',type=int,default=42); p.add_argument('--annotated-only',action='store_true',help='train on defect images only')
 a=p.parse_args(); train(a) if a.mode=='train' else evaluate(a)
