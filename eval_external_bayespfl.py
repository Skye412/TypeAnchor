"""Evaluate a Bayes-PFL checkpoint with this repository's protocol.

The checkpoint comes from /home/skye/data/Skye/visualad/run_comp_bayespfl.py (official Bayes-PFL code, ViT-L/14@336px, 518 input,
layers 6/12/18/24, two-stage training up to 30 epochs on Bridge512_balance_CODEBRIM train, val-best, seed 333).  Inference follows
that script: per-layer softmax maps averaged over prompts and layers, Gaussian sigma 8; image score = 0.5 * min-max(class
probability) + 0.5 * min-max(mean of the top-2000 pixels of the min-max normalised map), both normalised over the evaluated set.
Output layout matches eval_nuisance.py (maps/<sample>.npy float32 518x518, predictions.csv), so metrics_nuisance.py and
metrics_multiclass.py (P-AUPRO part) apply unchanged.  Bayes-PFL has no per-class output.
"""
import argparse,csv,hashlib,json,os,sys
from pathlib import Path
import numpy as np
import torch
from PIL import Image
from scipy.ndimage import gaussian_filter
from tqdm import tqdm
from torchvision.transforms import Compose,Resize,CenterCrop,ToTensor,Normalize,InterpolationMode
BAYES='/home/skye/data/Skye/Bayes-PFL-main'

def main():
 p=argparse.ArgumentParser(); p.add_argument('--checkpoint',default='/home/skye/data/Skye/visualad/outputs/comp_bayespfl_CODEBRIM/best_model.pth'); p.add_argument('--out',required=True)
 p.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); p.add_argument('--split',default='val'); p.add_argument('--sigma',type=float,default=8.)
 a=p.parse_args(); out=Path(a.out).resolve(); (out/'maps').mkdir(parents=True,exist_ok=True); data=Path(a.data).resolve(); ckpt_path=Path(a.checkpoint).resolve(); device=torch.device('cuda:0')
 os.chdir(BAYES); sys.path.insert(0,BAYES)   # the official code uses paths relative to its own directory
 from models.VPB import Context_Prompting,TextEncoder
 from models.model_CLIP import Load_CLIP,tokenize
 args=argparse.Namespace(dataset='CODEBRIM',model='ViT-L-14-336',pretrained='openai',features_list=[6,12,18,24],config_path=BAYES+'/open_clip_local/model_configs/ViT-L-14-336.json',pretrained_path=BAYES+'/pretrained_weight/ViT-L-14-336px.pt',
  num_flows=10,prompt_context_len=5,prompt_num=3,prompt_state_len=5,learning_rate=1e-4,learning_rate_PFL=1e-3,learning_rate_prompt=1e-3,learning_rate_linear=1e-4,sample_num=5,batch_size=16,image_size=518,epochs=30,device_id=0,seed=333)
 cfg=json.load(open(args.config_path)); args.vision_width=cfg['vision_cfg']['width']; args.text_width=cfg['text_cfg']['width']; args.embed_dim=cfg['embed_dim']
 clip,_,_=Load_CLIP(args.image_size,args.pretrained_path,device=device); clip.to(device).eval(); text_encoder=TextEncoder(clip,args); model=Context_Prompting(args=args).to(device)
 ck=torch.load(ckpt_path,map_location=device); model.load_state_dict(ck['MyModel']); stage=ck.get('stage',1); model.eval(); model.zk_n=None; model.zk_a=None
 trans=Compose([Resize((518,518),interpolation=InterpolationMode.BICUBIC),CenterCrop((518,518)),lambda im:im.convert('RGB'),ToTensor(),Normalize((0.48145466,0.4578275,0.40821073),(0.26862954,0.26130258,0.27577711))])
 with (data/(a.split+'_manifest.csv')).open() as f: rows=list(csv.DictReader(f))
 R=args.prompt_num*args.sample_num; cls_scores=[]; maps=[]
 with torch.no_grad():
  for r in tqdm(rows,desc=a.split):
   img=trans(Image.open(data/a.split/r['image_path']).convert('RGB')).unsqueeze(0).to(device)
   with torch.cuda.amp.autocast(): g,_,patches=clip.encode_image(img,args.features_list)
   g=g.float(); patches=[x.float() for x in patches]
   text,_=model.forward_ensemble(text_encoder,g,patches,['bridge'],device,tokenize,mode='test'); pro,layer_maps=model(text,g,patches,stage=stage,mode='test'); pro=pro.squeeze(2)
   cls_scores.append(float(torch.stack([pro[:,:R],pro[:,R:]],dim=-1).softmax(-1)[0,:,1].mean()))
   m=np.mean([torch.stack([x[:,:R],x[:,R:]],dim=2).softmax(2)[:,:,1].mean(1).float().cpu().numpy()[0] for x in layer_maps],axis=0)
   maps.append(gaussian_filter(m,sigma=a.sigma).astype(np.float32))
 maps=np.stack(maps); lo,hi=float(maps.min()),float(maps.max()); norm=(maps-lo)/(hi-lo+1e-8)   # global min-max, as norm01_f32_list
 mm=lambda v:(v-v.min())/(v.max()-v.min()+1e-8)
 flat=norm.reshape(len(rows),-1); top=np.partition(flat,-2000,axis=1)[:,-2000:].mean(1); scores=.5*mm(np.array(cls_scores,dtype=np.float32))+.5*mm(top)
 records=[]
 for r,m,s in zip(rows,norm,scores): np.save(out/'maps'/(r['sample']+'.npy'),m.astype(np.float32)); records.append({'sample':r['sample'],'label':int(r['category']=='annotated'),'score':float(s)})
 with (out/'predictions.csv').open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=records[0]); w.writeheader(); w.writerows(records)
 (out/'provenance.json').write_text(json.dumps({'method':'Bayes-PFL (official code, trained on CODEBRIM train, two-stage up to 30 epochs, val-best, seed 333)','checkpoint':str(ckpt_path),'sha256':hashlib.sha256(ckpt_path.read_bytes()).hexdigest(),'stage':stage,'data':str(data),'split':a.split,'count':len(records),'sigma':a.sigma},indent=2))
 print('INFERENCE_COMPLETE',len(records),flush=True)
if __name__=='__main__': main()
