"""Evaluate nuisance-v0 on validation; save per-image maps and predictions."""
import argparse,csv,json,hashlib
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from tqdm import tqdm
import adaptcliplib
from train_nuisance import Anchors,Bridge
from nuisance_model import NuisanceHead
from tools import get_transform,setup_seed

def main():
 p=argparse.ArgumentParser();p.add_argument('--checkpoint',default='runs/nuisance-v0/epoch_20.pth');p.add_argument('--out',default='runs/nuisance-v0/val-epoch20');p.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM');a=p.parse_args();setup_seed(10)
 out=Path(a.out);(out/'maps').mkdir(parents=True,exist_ok=True);device='cuda'
 clip,_=adaptcliplib.load('ViT-L/14@336px',device=device);clip.visual.DAPM_replace(DPAM_layer=20);clip.eval()
 trans,_=get_transform(518); train=Bridge(a.data,'train',trans); data=Bridge(a.data,'val',trans); normals=[r for r in train.rows if r['category']=='normal']
 bank=torch.load('runs/nuisance-v0/normal_globals.pt',map_location=device,weights_only=True)
 ckpt=torch.load(a.checkpoint,map_location='cpu',weights_only=True);head=NuisanceHead().to(device).eval();head.load_state_dict(ckpt['head']);anchors=Anchors(clip).to(device).eval();anchors.load_state_dict(ckpt['anchors'])
 cache={}; records=[]
 with torch.inference_mode():
  text=anchors(clip)
  for r in tqdm(data.rows,desc='validation'):
   img=trans(Image.open(data.root/r['image_path']).convert('RGB')).unsqueeze(0).to(device)
   g,q=clip.encode_image(img,[6,12,18,24],proj_use=False,DPAM_layer=20);q=[x[:,1:].float() for x in q];sim=F.normalize(g.float(),dim=-1)@bank.T
   ids=sim[0].topk(4).indices.tolist(); feats=[]
   for idx in ids:
    if idx not in cache:
     ref=trans(Image.open(train.root/normals[idx]['image_path']).convert('RGB')).unsqueeze(0).to(device);_,rf=clip.encode_image(ref,[6,12,18,24],proj_use=False,DPAM_layer=20);cache[idx]=[z[:,1:].half().cpu() for z in rf]
    feats.append(cache[idx])
   refs=[torch.cat([x[l] for x in feats],0).unsqueeze(0).to(device).float() for l in range(4)]
   result=head(q,refs,text);b=result['binary'][0,0];score=.5*result['image_logits'].softmax(-1)[0,1]+.5*b.flatten().topk(max(1,int(b.numel()*.01))).values.mean()
   arr=b.cpu().numpy();np.save(out/'maps'/(r['sample']+'.npy'),arr)
   records.append({'sample':r['sample'],'label':int(r['category']=='annotated'),'score':float(score),'references':'|'.join(normals[i]['sample'] for i in ids)})
 with (out/'predictions.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=records[0]);w.writeheader();w.writerows(records)
 (out/'provenance.json').write_text(json.dumps({'checkpoint':a.checkpoint,'sha256':hashlib.sha256(Path(a.checkpoint).read_bytes()).hexdigest(),'split':'val','count':len(records),'references':'top4 training normal globals','image_score':'0.5 image softmax + 0.5 top 1% binary map mean','map_size':518},indent=2))
 print('INFERENCE_COMPLETE',len(records),flush=True)
if __name__=='__main__':main()
