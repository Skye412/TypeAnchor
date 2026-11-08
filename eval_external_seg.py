"""Evaluate the WPFormer / MixerCSeg checkpoints (fully supervised binary defect segmentation) with this repository's protocol.

Checkpoints come from /home/skye/data/Skye/visualad/run_comp_{wpformer,mixercseg}.py: official code, trained on the
Bridge512_balance_CODEBRIM train split with the union defect mask (WPFormer pvt_v2_b2, 60 epochs, AdamW 8e-5, seed 111;
MixerCSeg 50 epochs, AdamW 5e-4, seed 42), checkpoint chosen on the val split.  Inference: 512x512 input with the method's
normalisation, sigmoid of the final logit, bilinear to 518, no smoothing; image score = mean of the top 1% pixels, as for the
SegFormer-B2 baseline (train_segformer.py).  Output layout matches eval_nuisance.py (maps/<sample>.npy, predictions.csv), so
metrics_nuisance.py and metrics_multiclass.py (P-AUPRO part) apply unchanged.  Neither method has per-class output.

Run WPFormer in the `wpformer` conda env and MixerCSeg in the `MixerCSeg` env (see scripts/queue_external_seg.sh).
"""
import argparse,csv,hashlib,json,os,sys
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from tqdm import tqdm
import torchvision.transforms as T
ROOTS={'wpformer':'/home/skye/data/Skye/WPFormer','mixercseg':'/home/skye/data/Skye/MixerCSeg'}
CKPTS={'wpformer':'/home/skye/data/Skye/visualad/outputs/comp_wpformer_CODEBRIM/best_model.pth','mixercseg':'/home/skye/data/Skye/visualad/outputs/comp_mixercseg_CODEBRIM/best_model.pth'}

def main():
 p=argparse.ArgumentParser(); p.add_argument('method',choices=list(ROOTS)); p.add_argument('--checkpoint',default=None); p.add_argument('--out',required=True)
 p.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); p.add_argument('--split',default='val')
 a=p.parse_args(); out=Path(a.out).resolve(); (out/'maps').mkdir(parents=True,exist_ok=True); data=Path(a.data).resolve(); ck=Path(a.checkpoint or CKPTS[a.method]).resolve(); device='cuda'
 os.chdir(ROOTS[a.method]); sys.path.insert(0,ROOTS[a.method])   # the official code resolves its pretrained weights relative to its own directory
 if a.method=='wpformer':
  from model.WPFormer import WPFormer
  model=WPFormer(method='pvt_v2_b2',channel=64); trans=T.Compose([T.Resize((512,512)),T.ToTensor(),T.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])])
  fwd=lambda x:model(x)[-1]
 else:
  from models import build_MixerCSeg
  model,_=build_MixerCSeg(argparse.Namespace(BCELoss_ratio=0.87,DiceLoss_ratio=0.13,Norm_Type='GN',device='cuda',load_width=512,load_height=512)); trans=T.Compose([T.Resize((512,512)),T.ToTensor(),T.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))])
  fwd=lambda x:model(x)
 model.load_state_dict(torch.load(ck,map_location='cpu')); model.to(device).eval()
 with (data/(a.split+'_manifest.csv')).open() as f: rows=list(csv.DictReader(f))
 records=[]
 with torch.no_grad():
  for r in tqdm(rows,desc=a.split):
   x=trans(Image.open(data/a.split/r['image_path']).convert('RGB')).unsqueeze(0).to(device)
   with torch.autocast('cuda',enabled=a.method=='wpformer'): logit=fwd(x)   # VMamba's index_put in MixerCSeg rejects half inputs: fp32 there
   m=F.interpolate(torch.sigmoid(logit.float()),size=(518,518),mode='bilinear',align_corners=False)[0,0]
   np.save(out/'maps'/(r['sample']+'.npy'),m.cpu().numpy().astype(np.float32))
   records.append({'sample':r['sample'],'label':int(r['category']=='annotated'),'score':float(m.flatten().topk(max(1,int(m.numel()*.01))).values.mean())})
 with (out/'predictions.csv').open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=records[0]); w.writeheader(); w.writerows(records)
 (out/'provenance.json').write_text(json.dumps({'method':a.method+' (official code, trained on CODEBRIM train with the union mask, val-best checkpoint from the visualad project)','checkpoint':str(ck),'sha256':hashlib.sha256(ck.read_bytes()).hexdigest(),'data':str(data),'split':a.split,'count':len(records),'image_score':'top 1% mean'},indent=2))
 print('INFERENCE_COMPLETE',len(records),flush=True)
if __name__=='__main__': main()
