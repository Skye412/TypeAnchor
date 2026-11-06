"""Evaluate a nuisance-aware checkpoint on a split; save per-image maps and predictions.

Saved maps (518x518): maps/<sample>.npy binary map (float32).
With --save-typed also typed/<sample>.npy [4,518,518] float16 (pi for crack/corrosion/spalling/efflorescence),
residual/<sample>.npy float16 and nuisance/<sample>.npy float16 (nuisance anchor mass, zero without such anchors).
"""
import argparse,csv,json,hashlib
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from tqdm import tqdm
import adaptcliplib
from train_nuisance import Anchors,AnchorsV2,Bridge,NAMES
from nuisance_model import NuisanceHead,NuisanceHeadV2

def build(clip,cfg,names,device):
 """Head + anchors for a checkpoint config (v0 or v2 architecture)."""
 if cfg.get('arch','v0')=='v2': return NuisanceHeadV2(n_anchors=len(names),nu_gate=not cfg.get('no_nu_gate',False),gamma_fixed=cfg.get('gamma_fixed',None),use_residual=not cfg.get('no_residual',False),detail=cfg.get('detail',False)).to(device).eval(),AnchorsV2(clip,names,eps=cfg.get('eps',.5)).to(device).eval()
 return NuisanceHead(n_anchors=len(names)).to(device).eval(),Anchors(clip,names,freeze_nuisance=cfg.get('freeze_nuisance',False)).to(device).eval()
from tools import get_transform,setup_seed

def main():
 p=argparse.ArgumentParser();p.add_argument('--checkpoint',default='runs/nuisance-v0/epoch_20.pth');p.add_argument('--out',default='runs/nuisance-v0/val-epoch20');p.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM')
 p.add_argument('--split',default='val');p.add_argument('--bank',default='runs/nuisance-v0/normal_globals.pt');p.add_argument('--save-typed',action='store_true')
 p.add_argument('--ref-data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM',help='dataset whose train normals form the reference bank (must match --bank); --data may be another dataset for cross-dataset evaluation')
 p.add_argument('--ref-subset',type=int,default=0,help='use only this many randomly chosen reference normals (few-shot protocol); 0 = whole bank')
 p.add_argument('--ref-seed',type=int,default=10)
 a=p.parse_args();setup_seed(10)
 out=Path(a.out);(out/'maps').mkdir(parents=True,exist_ok=True);device='cuda'
 if a.save_typed:
  for d in ('typed','residual','nuisance'):(out/d).mkdir(exist_ok=True)
 clip,_=adaptcliplib.load('ViT-L/14@336px',device=device);clip.visual.DAPM_replace(DPAM_layer=20);clip.eval()
 trans,_=get_transform(518); train=Bridge(a.ref_data,'train',trans); data=Bridge(a.data,a.split,trans); normals=[r for r in train.rows if r['category']=='normal']
 if not Path(a.bank).exists():
  # build the global-embedding bank for the reference dataset (same recipe as train_nuisance.py)
  Path(a.bank).parent.mkdir(parents=True,exist_ok=True); rows_=[]
  with torch.inference_mode():
   for r in tqdm(normals,desc='reference bank'):
    x=trans(Image.open(train.root/r['image_path']).convert('RGB')).unsqueeze(0).to(device); g,_=clip.encode_image(x,[6,12,18,24],proj_use=False,DPAM_layer=20); rows_.append(F.normalize(g.float(),dim=-1).cpu())
  torch.save(torch.cat(rows_),a.bank)
 bank=torch.load(a.bank,map_location=device,weights_only=True)
 if bank.shape[0]!=len(normals): raise SystemExit(f'bank rows {bank.shape[0]} != train normals of --ref-data {len(normals)}')
 if a.ref_subset:
  import random as _r; keep=sorted(_r.Random(a.ref_seed).sample(range(len(normals)),a.ref_subset)); normals=[normals[i] for i in keep]; bank=bank[keep]
 ckpt=torch.load(a.checkpoint,map_location='cpu',weights_only=True); cfg=ckpt.get('config',{}); names=cfg.get('anchors',NAMES)
 head,anchors=build(clip,cfg,names,device);head.load_state_dict(ckpt['head']);anchors.load_state_dict(ckpt['anchors'])
 cache={}; records=[]
 with torch.inference_mode():
  text=anchors(clip)
  for r in tqdm(data.rows,desc=a.split):
   img=trans(Image.open(data.root/r['image_path']).convert('RGB')).unsqueeze(0).to(device)
   g,q=clip.encode_image(img,[6,12,18,24],proj_use=False,DPAM_layer=20);q=[x[:,1:].float() for x in q];sim=F.normalize(g.float(),dim=-1)@bank.T
   ids=sim[0].topk(min(4,bank.shape[0])).indices.tolist(); feats=[]
   for idx in ids:
    if idx not in cache:
     ref=trans(Image.open(train.root/normals[idx]['image_path']).convert('RGB')).unsqueeze(0).to(device);_,rf=clip.encode_image(ref,[6,12,18,24],proj_use=False,DPAM_layer=20);cache[idx]=[z[:,1:].half().cpu() for z in rf]
    feats.append(cache[idx])
   refs=[torch.cat([x[l] for x in feats],0).unsqueeze(0).to(device).float() for l in range(4)]
   result=head(q,refs,text,image=img) if getattr(head,'detail',False) else head(q,refs,text);b=result['binary'][0,0];score=.5*result['image_logits'].softmax(-1)[0,1]+.5*b.flatten().topk(max(1,int(b.numel()*.01))).values.mean()
   arr=b.cpu().numpy();np.save(out/'maps'/(r['sample']+'.npy'),arr)
   if a.save_typed:
    np.save(out/'typed'/(r['sample']+'.npy'),result['typed'][0].half().cpu().numpy())
    np.save(out/'residual'/(r['sample']+'.npy'),result['residual'][0,0].half().cpu().numpy())
    np.save(out/'nuisance'/(r['sample']+'.npy'),result['nuisance'][0,0].half().cpu().numpy())
    if 'nu_up' in result: (out/'nu').mkdir(exist_ok=True); np.save(out/'nu'/(r['sample']+'.npy'),result['nu_up'][0,0].half().cpu().numpy())
   records.append({'sample':r['sample'],'label':int(r['category']=='annotated'),'score':float(score),'references':'|'.join(normals[i]['sample'] for i in ids)})
 with (out/'predictions.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=records[0]);w.writeheader();w.writerows(records)
 (out/'provenance.json').write_text(json.dumps({'checkpoint':a.checkpoint,'sha256':hashlib.sha256(Path(a.checkpoint).read_bytes()).hexdigest(),'anchors':names,'data':a.data,'ref_data':a.ref_data,'split':a.split,'count':len(records),'references':'top4 training normal globals','bank':a.bank,'ref_subset':a.ref_subset,'ref_seed':a.ref_seed,'reference_samples':[n['sample'] for n in normals] if a.ref_subset else 'all','image_score':'0.5 image softmax + 0.5 top 1% binary map mean','map_size':518,'typed_maps_saved':a.save_typed},indent=2))
 print('INFERENCE_COMPLETE',len(records),flush=True)
if __name__=='__main__':main()
