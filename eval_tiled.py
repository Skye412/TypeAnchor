"""Tiled (sliding-window) inference for a nuisance-aware checkpoint: a resolution diagnostic for thin cracks.

The image is upsampled to S*518 and cut into overlapping 518 windows (stride 259); each window goes through the frozen
CLIP + head exactly like a full image (same retrieved references, chosen from the full image), window outputs are
averaged on the S*518 canvas and area-downsampled to 518. The effective patch grid is (S*37)^2 instead of 37^2.
No retraining: the head only ever saw full tiles, so this also measures how scale-robust it is.
  --blend 0   : tiled maps only            --blend 0.5 : mean of tiled and full-image maps
Image score = 0.5 * image softmax of the full-image pass + 0.5 * top 1% mean of the final binary map (as eval_nuisance.py).
Output layout is identical to eval_nuisance.py --save-typed, so the metric scripts apply unchanged.
"""
import argparse,csv,json
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from tqdm import tqdm
import adaptcliplib
from train_nuisance import Bridge,NAMES
from eval_nuisance import build
from tools import get_transform,setup_seed

def main():
 p=argparse.ArgumentParser();p.add_argument('--checkpoint',required=True);p.add_argument('--out',required=True);p.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM');p.add_argument('--split',default='val')
 p.add_argument('--bank',default='runs/nuisance-v0/normal_globals.pt');p.add_argument('--ref-data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM')
 p.add_argument('--scale',type=int,default=2);p.add_argument('--blend',type=float,default=0.);p.add_argument('--tile-refs',action='store_true',help='upsample and tile the references the same way (reference patches at the same scale as query windows); default: full-view references')
 a=p.parse_args();setup_seed(10);out=Path(a.out);device='cuda'
 for d in ('maps','typed','residual','nuisance','nu'):(out/d).mkdir(parents=True,exist_ok=True)
 clip,_=adaptcliplib.load('ViT-L/14@336px',device=device);clip.visual.DAPM_replace(DPAM_layer=20);clip.eval()
 trans,_=get_transform(518);train=Bridge(a.ref_data,'train',trans);data=Bridge(a.data,a.split,trans);normals=[r for r in train.rows if r['category']=='normal']
 bank=torch.load(a.bank,map_location=device,weights_only=True)
 if bank.shape[0]!=len(normals): raise SystemExit('bank / reference list mismatch')
 ckpt=torch.load(a.checkpoint,map_location='cpu',weights_only=True);cfg=ckpt.get('config',{});names=cfg.get('anchors',NAMES)
 head,anchors=build(clip,cfg,names,device);head.load_state_dict(ckpt['head']);anchors.load_state_dict(ckpt['anchors'])
 S=a.scale;full=S*518;starts=list(range(0,full-518+1,259));boxes=[(x,y) for y in starts for x in starts]
 def windows(img):
  big=img.resize((full,full),Image.Resampling.BICUBIC);return torch.stack([trans(big.crop((x,y,x+518,y+518))) for x,y in boxes]).to(device)
 def enc(x):
  g,q=clip.encode_image(x,[6,12,18,24],proj_use=False,DPAM_layer=20);return g,[z[:,1:].float() for z in q]
 cache={};records=[];keys=('binary','typed','residual','nuisance','nu_up')
 with torch.inference_mode():
  text=anchors(clip)
  for r in tqdm(data.rows,desc=a.split):
   img=Image.open(data.root/r['image_path']).convert('RGB');g,q=enc(trans(img).unsqueeze(0).to(device))
   ids=(F.normalize(g.float(),dim=-1)@bank.T)[0].topk(min(4,bank.shape[0])).indices.tolist();feats=[]
   for idx in ids:
    if idx not in cache:
     rimg=Image.open(train.root/normals[idx]['image_path']).convert('RGB')
     if a.tile_refs:
      _,rf=enc(windows(rimg));cache[idx]=[z.reshape(1,-1,z.shape[-1]).half().cpu() for z in rf]     # all windows' patches pooled into one reference set
     else:
      _,rf=enc(trans(rimg).unsqueeze(0).to(device));cache[idx]=[z.half().cpu() for z in rf]
    feats.append(cache[idx])
   refs=[torch.cat([x[l] for x in feats],1).to(device).float() for l in range(4)]       # [1, n_ref_patches, d]
   res_full=head(q,refs,text)
   acc={k:None for k in keys};cnt=torch.zeros(1,1,full,full,device=device)
   w=windows(img)
   for i in range(0,len(boxes),3):
    _,qw=enc(w[i:i+3]);b=qw[0].shape[0];res=head(qw,[x.expand(b,*x.shape[1:]) for x in refs],text)
    for j in range(b):
     x,y=boxes[i+j];cnt[...,y:y+518,x:x+518]+=1
     for k in keys:
      if k not in res: continue
      v=res[k][j:j+1]
      if acc[k] is None: acc[k]=torch.zeros(1,v.shape[1],full,full,device=device)
      acc[k][...,y:y+518,x:x+518]+=v
   final={}
   for k in keys:
    if acc[k] is None: continue
    t=F.adaptive_avg_pool2d(acc[k]/cnt,518)
    final[k]=(1-a.blend)*t+a.blend*res_full[k] if a.blend>0 else t
   b=final['binary'][0,0];score=.5*res_full['image_logits'].softmax(-1)[0,1]+.5*b.flatten().topk(max(1,int(b.numel()*.01))).values.mean()
   s=r['sample'];np.save(out/'maps'/(s+'.npy'),b.cpu().numpy());np.save(out/'typed'/(s+'.npy'),final['typed'][0].half().cpu().numpy())
   np.save(out/'residual'/(s+'.npy'),final['residual'][0,0].half().cpu().numpy());np.save(out/'nuisance'/(s+'.npy'),final['nuisance'][0,0].half().cpu().numpy())
   if 'nu_up' in final: np.save(out/'nu'/(s+'.npy'),final['nu_up'][0,0].half().cpu().numpy())
   records.append({'sample':s,'label':int(r['category']=='annotated'),'score':float(score),'references':'|'.join(normals[i]['sample'] for i in ids)})
 with (out/'predictions.csv').open('w',newline='') as f:w_=csv.DictWriter(f,fieldnames=records[0]);w_.writeheader();w_.writerows(records)
 (out/'provenance.json').write_text(json.dumps({'checkpoint':a.checkpoint,'data':a.data,'ref_data':a.ref_data,'split':a.split,'count':len(records),'tiled':{'scale':S,'windows':len(boxes),'stride':259,'blend':a.blend,'tile_refs':a.tile_refs},'image_score':'0.5 full-image softmax + 0.5 top 1% of final binary map','map_size':518},indent=2))
 print('INFERENCE_COMPLETE',len(records),flush=True)
if __name__=='__main__':main()
