"""Fully supervised reference baseline: SegFormer-B2 (MiT-B2 ImageNet-1k backbone + all-MLP head) trained on the same
CODEBRIM tiles and the same four independent class masks as the nuisance-aware heads (multi-label, per-class sigmoid).

Run in the MixerCSeg conda env (mmseg 0.30 / mmcv 1.7 provide the modules; nothing is downloaded):
  python train_segformer.py --out runs/segformer-b2 [--epochs 40]
  python train_segformer.py --out runs/segformer-b2 --eval-only --split val --eval-out runs/segformer-b2/val-epoch40
Evaluation writes the same layout as eval_nuisance.py (maps/, typed/, residual/, predictions.csv, provenance.json) so
metrics_nuisance.py / metrics_multiclass.py / compare_fp.py apply unchanged:
  binary map = max_c sigmoid(logit_c) at 518; typed = per-class sigmoid; residual = binary map (so 'gated' = typed*binary);
  image score = mean of the top 1% binary-map pixels.
"""
import argparse,csv,json,random
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import Dataset,DataLoader
from PIL import Image
from mmseg.models.backbones import MixVisionTransformer
from mmseg.models.decode_heads import SegformerHead

CLASSES=['Crack','Corrosion','Spalling','Efflorescence']
MEAN=np.array([123.675,116.28,103.53],np.float32); STD=np.array([58.395,57.12,57.375],np.float32)
PRETRAIN='/home/skye/.cache/torch/hub/checkpoints/mit_b2_20220624-66e8bf70.pth'

class Tiles(Dataset):
 def __init__(self,root,split,train):
  self.root=Path(root)/split; self.train=train
  with (Path(root)/(split+'_manifest.csv')).open() as f: self.rows=list(csv.DictReader(f))
 def __len__(self): return len(self.rows)
 def __getitem__(self,i):
  r=self.rows[i]; im=np.asarray(Image.open(self.root/r['image_path']).convert('RGB').resize((512,512),Image.BILINEAR),np.float32)
  m=np.zeros((4,512,512),np.float32)
  if r['category']=='annotated':
   for c,name in enumerate(CLASSES):
    p=self.root/'multiclass_annotations'/'masks'/(r['sample']+'__'+name+'.png')
    if p.exists(): m[c]=(np.asarray(Image.open(p).convert('L').resize((512,512),Image.NEAREST))>0)
  if self.train:
   if random.random()<.5: im=im[:,::-1]; m=m[:,:,::-1]
   if random.random()<.5: im=im[::-1]; m=m[:,::-1]
   k=random.randint(0,3); im=np.rot90(im,k,(0,1)); m=np.rot90(m,k,(1,2))
   im=im*random.uniform(.8,1.2)+random.uniform(-20,20)       # brightness / contrast jitter
  im=((np.clip(im,0,255)-MEAN)/STD).transpose(2,0,1)
  return torch.from_numpy(np.ascontiguousarray(im)),torch.from_numpy(np.ascontiguousarray(m)),i

class SegFormerB2(nn.Module):
 def __init__(self):
  super().__init__()
  self.backbone=MixVisionTransformer(in_channels=3,embed_dims=64,num_stages=4,num_layers=[3,4,6,3],num_heads=[1,2,5,8],patch_sizes=[7,3,3,3],sr_ratios=[8,4,2,1],out_indices=(0,1,2,3),mlp_ratio=4,qkv_bias=True,drop_rate=0.,attn_drop_rate=0.,drop_path_rate=.1)
  self.head=SegformerHead(in_channels=[64,128,320,512],in_index=[0,1,2,3],channels=256,dropout_ratio=.1,num_classes=4,norm_cfg=dict(type='BN',requires_grad=True),align_corners=False)
 def load_pretrained(self,path):
  sd=torch.load(path,map_location='cpu'); sd=sd.get('state_dict',sd); sd={k[len('backbone.'):] if k.startswith('backbone.') else k:v for k,v in sd.items()}
  res=self.backbone.load_state_dict(sd,strict=False); return len(res.missing_keys),len(res.unexpected_keys)
 def forward(self,x):
  return F.interpolate(self.head(self.backbone(x)),size=x.shape[-2:],mode='bilinear',align_corners=False)

def loss_fn(logits,y):
 bce=F.binary_cross_entropy_with_logits(logits,y); p=logits.sigmoid()
 inter=(p*y).sum((0,2,3)); dice=1-(2*inter+1)/(p.sum((0,2,3))+y.sum((0,2,3))+1)
 return bce+dice.mean()

@torch.inference_mode()
def evaluate(model,data_root,split,out,device,ckpt_note):
 out=Path(out)
 for d in ('maps','typed','residual','nuisance'): (out/d).mkdir(parents=True,exist_ok=True)
 ds=Tiles(data_root,split,False); dl=DataLoader(ds,batch_size=8,num_workers=4); model.eval(); rec=[]
 for x,_,idx in dl:
  p=F.interpolate(model(x.to(device)),size=(518,518),mode='bilinear',align_corners=False).sigmoid()
  b=p.amax(1)
  for j,i in enumerate(idx.tolist()):
   r=ds.rows[i]; bj=b[j]; np.save(out/'maps'/(r['sample']+'.npy'),bj.cpu().numpy()); np.save(out/'typed'/(r['sample']+'.npy'),p[j].half().cpu().numpy())
   np.save(out/'residual'/(r['sample']+'.npy'),bj.half().cpu().numpy()); np.save(out/'nuisance'/(r['sample']+'.npy'),np.zeros((518,518),np.float16))
   rec.append({'sample':r['sample'],'label':int(r['category']=='annotated'),'score':float(bj.flatten().topk(max(1,int(bj.numel()*.01))).values.mean()),'references':''})
 with (out/'predictions.csv').open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=rec[0]); w.writeheader(); w.writerows(rec)
 (out/'provenance.json').write_text(json.dumps({'model':'SegFormer-B2 (mmseg 0.30 modules), multi-label sigmoid','checkpoint':ckpt_note,'data':str(data_root),'split':split,'count':len(rec),'image_score':'top 1% binary map mean','map_size':518,'binary':'max over 4 class sigmoids'},indent=2))
 print('INFERENCE_COMPLETE',len(rec),flush=True)

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); ap.add_argument('--out',default='runs/segformer-b2'); ap.add_argument('--epochs',type=int,default=40); ap.add_argument('--bs',type=int,default=8); ap.add_argument('--lr',type=float,default=6e-5); ap.add_argument('--seed',type=int,default=10)
 ap.add_argument('--max-steps',type=int,default=0); ap.add_argument('--eval-only',action='store_true'); ap.add_argument('--split',default='val'); ap.add_argument('--eval-data',default=None); ap.add_argument('--eval-out',default=None)
 a=ap.parse_args(); random.seed(a.seed); np.random.seed(a.seed); torch.manual_seed(a.seed); device='cuda'; out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
 model=SegFormerB2().to(device)
 if a.eval_only:
  ck=torch.load(out/'last.pth',map_location='cpu'); model.load_state_dict(ck['model']); evaluate(model,a.eval_data or a.data,a.split,a.eval_out or out/f'{a.split}-epoch{ck["epoch"]}',device,str(out/'last.pth')); return
 print('pretrained backbone missing/unexpected keys:',model.load_pretrained(PRETRAIN),flush=True)
 (out/'config.json').write_text(json.dumps(vars(a),indent=2))
 ds=Tiles(a.data,'train',True); dl=DataLoader(ds,batch_size=a.bs,shuffle=True,num_workers=6,drop_last=True,pin_memory=True)
 # standard SegFormer recipe: AdamW, head lr x10, linear warm-up then poly decay
 opt=torch.optim.AdamW([{'params':model.backbone.parameters(),'lr':a.lr},{'params':model.head.parameters(),'lr':a.lr*10}],weight_decay=.01)
 total=a.epochs*len(dl); warm=min(1500,total//10); step=0; scaler=torch.cuda.amp.GradScaler()
 for ep in range(1,a.epochs+1):
  model.train(); losses=[]
  for x,y,_ in dl:
   f=(step+1)/warm if step<warm else (1-(step-warm)/max(1,total-warm))**1.0
   for g,base in zip(opt.param_groups,(a.lr,a.lr*10)): g['lr']=base*max(f,1e-3)
   with torch.cuda.amp.autocast(): loss=loss_fn(model(x.to(device,non_blocking=True)).float(),y.to(device,non_blocking=True))
   opt.zero_grad(set_to_none=True); scaler.scale(loss).backward(); scaler.step(opt); scaler.update(); losses.append(loss.item()); step+=1
   if a.max_steps and step>=a.max_steps: break
  torch.save({'model':model.state_dict(),'epoch':ep,'config':vars(a)},out/'last.pth')
  with (out/'train_log.jsonl').open('a') as fh: fh.write(json.dumps({'epoch':ep,'loss':float(np.mean(losses)),'steps':step})+'\n')
  print(f'epoch {ep}/{a.epochs} loss={np.mean(losses):.4f} steps={step}',flush=True)
  if a.max_steps and step>=a.max_steps: break
 evaluate(model,a.data,'val',out/f'val-epoch{ep}',device,str(out/'last.pth'))
if __name__=='__main__': main()
