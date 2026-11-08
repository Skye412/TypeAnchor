"""Zero-shot per-type baseline: frozen CLIP ViT-L/14@336 (518 input, DPAM at layer 20 as in AdaptCLIP), the same four hand-written
prompt templates and anchor names as TypeAnchor, no training.  For every cell the 4-layer mean cosine between the CLIP-projected
patch token and each anchor embedding is computed (train_nuisance.zero_shot_sims).  Per-type probability = softmax over
[intact, type_c] with scale 100 (WinCLIP-style two-way softmax); binary map = max over the four types; maps are bilinearly
upsampled from 37x37 to 518 and smoothed (sigma 4), image score = mean of the top 1% binary pixels.  Output layout as
eval_nuisance.py --save-typed (residual = binary map, nuisance = 0), so metrics_nuisance.py / metrics_multiclass.py apply.
Run in the adaptclip env:  python eval_zeroshot.py --out runs/zeroshot-clip/val [--data ... --split test]
"""
import argparse,csv,json
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from tqdm import tqdm
from scipy.ndimage import gaussian_filter
import adaptcliplib
from train_nuisance import Anchors,Bridge,zero_shot_sims
from tools import get_transform,setup_seed

def main():
 p=argparse.ArgumentParser(); p.add_argument('--out',required=True); p.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); p.add_argument('--split',default='val')
 p.add_argument('--checkpoint',default='runs/ablation-v2-no-nuisance/epoch_20.pth',help='only its anchor names are read (intact + 4 types)'); p.add_argument('--scale',type=float,default=100.); p.add_argument('--sigma',type=float,default=4.)
 a=p.parse_args(); setup_seed(10); device='cuda'; out=Path(a.out)
 for d in ('maps','typed','residual','nuisance'): (out/d).mkdir(parents=True,exist_ok=True)
 names=torch.load(a.checkpoint,map_location='cpu',weights_only=True)['config']['anchors'][:5]
 assert all(k in ' '.join(names[1:5]).lower() for k in ('crack','rust','spall','efflor')),names
 clip,_=adaptcliplib.load('ViT-L/14@336px',device=device); clip.visual.DAPM_replace(DPAM_layer=20); clip.eval()
 trans,_=get_transform(518); data=Bridge(a.data,a.split,trans)
 with torch.inference_mode():
  hand=Anchors(clip,names).hand.to(device)   # [5,768] template-ensemble prompt embeddings, no learned part
  records=[]
  for r in tqdm(data.rows,desc=a.split):
   img=trans(Image.open(data.root/r['image_path']).convert('RGB')).unsqueeze(0).to(device)
   _,q=clip.encode_image(img,[6,12,18,24],proj_use=False,DPAM_layer=20); q=[x[:,1:].float() for x in q]
   sims=zero_shot_sims(q,clip,hand)                      # [N,5]
   two=torch.stack([sims[:,0:1].expand(-1,4),sims[:,1:5]],-1)   # [N,4,2]: (intact, type)
   typed=(a.scale*two).softmax(-1)[...,1].T.reshape(1,4,37,37)
   typed=F.interpolate(typed,size=(518,518),mode='bilinear',align_corners=False)[0].cpu().numpy()
   typed=np.stack([gaussian_filter(t,a.sigma) for t in typed]).astype(np.float32); binary=typed.max(0)
   np.save(out/'maps'/(r['sample']+'.npy'),binary); np.save(out/'typed'/(r['sample']+'.npy'),typed.astype(np.float16))
   np.save(out/'residual'/(r['sample']+'.npy'),binary.astype(np.float16)); np.save(out/'nuisance'/(r['sample']+'.npy'),np.zeros((518,518),np.float16))
   flat=np.sort(binary.ravel())[::-1]; records.append({'sample':r['sample'],'label':int(r['category']=='annotated'),'score':float(flat[:max(1,flat.size//100)].mean()),'references':''})
 with (out/'predictions.csv').open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=records[0]); w.writeheader(); w.writerows(records)
 (out/'provenance.json').write_text(json.dumps({'model':'zero-shot frozen CLIP ViT-L/14@336, hand prompts (4 templates), two-way softmax per type, scale %.0f, sigma %.1f'%(a.scale,a.sigma),'anchors':names,'data':a.data,'split':a.split,'count':len(records),'image_score':'top 1% binary map mean','map_size':518,'binary':'max over 4 type probabilities'},indent=2))
 print('INFERENCE_COMPLETE',len(records),flush=True)
if __name__=='__main__': main()
