"""Precompute frozen CLIP features for a split so training/evaluation need no backbone forward per step.

Per sample: <cache>/<split>/tokens/<sample>.npy  float16 [4,1369,1024]  (layers 6/12/18/24 patch tokens, no CLS, un-projected)
            <cache>/<split>/globals.pt            float32 [N,768] L2-normalised global embeddings in manifest order
Features are exactly what train_nuisance.py computes on the fly (518 input, DPAM layer 20), stored in fp16.
Usage: python build_feature_cache.py --split train --cache /home/skye/data/Skye/feature_cache
"""
import argparse,json
from pathlib import Path
import numpy as np
import torch,torch.nn.functional as F
from PIL import Image
from tqdm import tqdm
import adaptcliplib
from train_nuisance import Bridge
from tools import get_transform

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--split',required=True); ap.add_argument('--cache',default='/home/skye/data/Skye/feature_cache'); ap.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); a=ap.parse_args()
 out=Path(a.cache)/a.split; (out/'tokens').mkdir(parents=True,exist_ok=True); device='cuda'
 clip,_=adaptcliplib.load('ViT-L/14@336px',device=device); clip.visual.DAPM_replace(DPAM_layer=20); clip.eval()
 trans,_=get_transform(518); ds=Bridge(a.data,a.split,trans); globals_=[]
 with torch.inference_mode():
  for r in tqdm(ds.rows,desc=a.split):
   p=out/'tokens'/(r['sample']+'.npy')
   x=trans(Image.open(ds.root/r['image_path']).convert('RGB')).unsqueeze(0).to(device)
   g,q=clip.encode_image(x,[6,12,18,24],proj_use=False,DPAM_layer=20)
   globals_.append(F.normalize(g.float(),dim=-1).cpu())
   if not p.exists(): np.save(p,torch.stack([t[0,1:] for t in q]).half().cpu().numpy())
 torch.save(torch.cat(globals_),out/'globals.pt')
 (out/'manifest.json').write_text(json.dumps({'samples':[r['sample'] for r in ds.rows],'layers':[6,12,18,24],'input':518,'dpam':20,'dtype':'float16'}))
 print('CACHE_DONE',a.split,len(ds.rows),flush=True)
if __name__=='__main__': main()
