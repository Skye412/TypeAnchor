"""Evaluate an AnomalyCLIP prompt-learner checkpoint with this repository's protocol.

The checkpoint comes from /home/skye/data/Skye/visualad/run_comp_anomalyclip.py (official AnomalyCLIP code, ViT-L/14@336px,
518 input, layers 6/12/18/24, DPAM from layer 20, 15 epochs on Bridge512_balance_CODEBRIM train, val-best).  Inference follows
that script (sum of the four layer maps, Gaussian sigma 4, image score = softmax text probability); the summed map is divided
by 4 to stay in [0, 1].  Output layout matches eval_nuisance.py (maps/<sample>.npy float32 518x518, predictions.csv), so
metrics_nuisance.py and metrics_multiclass.py (P-AUPRO part) apply unchanged.  AnomalyCLIP has no per-class output.
"""
import argparse,csv,hashlib,json,sys
from pathlib import Path
THIRD='/home/skye/data/Skye/third_party/AnomalyCLIP'
sys.path.insert(0,THIRD)
import numpy as np
import torch
from PIL import Image
from scipy.ndimage import gaussian_filter
from tqdm import tqdm
try: import thop
except ImportError:   # AnomalyCLIP_lib imports thop.profile only for a FLOPs printout
 import types; _t=types.ModuleType('thop'); _t.profile=lambda *x,**k:(0,0); sys.modules['thop']=_t
import AnomalyCLIP_lib
from prompt_ensemble import AnomalyCLIP_PromptLearner
from utils import get_transform
sys.path.remove(THIRD)
from train_nuisance import Bridge

def main():
 p=argparse.ArgumentParser(); p.add_argument('--checkpoint',default='/home/skye/data/Skye/visualad/outputs/comp_anomalyclip_CODEBRIM/best_model.pth'); p.add_argument('--out',required=True)
 p.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); p.add_argument('--split',default='val'); p.add_argument('--sigma',type=float,default=4.)
 a=p.parse_args(); out=Path(a.out); (out/'maps').mkdir(parents=True,exist_ok=True); device='cuda'; size=518; layers=[6,12,18,24]
 details={'Prompt_length':12,'learnabel_text_embedding_depth':9,'learnabel_text_embedding_length':4}
 model,_=AnomalyCLIP_lib.load('ViT-L/14@336px',device=device,design_details=details,download_root='/home/skye/data/Skye/Bayes-PFL-main/pretrained_weight'); model.eval()
 learner=AnomalyCLIP_PromptLearner(model.to('cpu'),details); learner.load_state_dict(torch.load(a.checkpoint,map_location='cpu')['prompt_learner']); learner.to(device).eval(); model.to(device); model.visual.DAPM_replace(DPAM_layer=20)
 trans,_=get_transform(argparse.Namespace(image_size=size)); data=Bridge(a.data,a.split,trans); records=[]
 with torch.no_grad():
  prompts,tokens,compound=learner(cls_id=None); text=model.encode_text_learn(prompts,tokens,compound).float()
  text=torch.stack(torch.chunk(text,dim=0,chunks=2),dim=1); text=text/text.norm(dim=-1,keepdim=True)
  for r in tqdm(data.rows,desc=a.split):
   img=trans(Image.open(data.root/r['image_path']).convert('RGB')).unsqueeze(0).to(device)
   with torch.cuda.amp.autocast(): g,patches=model.encode_image(img,layers,DPAM_layer=20)
   g=g.float(); g=g/g.norm(dim=-1,keepdim=True); score=((g.unsqueeze(1)@text.permute(0,2,1))/.07).softmax(-1)[0,0,1]
   maps=[]
   for pf in patches:
    pf=pf.float(); pf=pf/pf.norm(dim=-1,keepdim=True); sim,_=AnomalyCLIP_lib.compute_similarity(pf,text[0]); sm=AnomalyCLIP_lib.get_similarity_map(sim[:,1:,:],size)
    maps.append((sm[...,1]+1.-sm[...,0])/2.)
   m=gaussian_filter(torch.stack(maps).sum(0)[0].float().cpu().numpy(),sigma=a.sigma)/len(layers)
   np.save(out/'maps'/(r['sample']+'.npy'),m.astype(np.float32)); records.append({'sample':r['sample'],'label':int(r['category']=='annotated'),'score':float(score)})
 with (out/'predictions.csv').open('w',newline='') as f: w=csv.DictWriter(f,fieldnames=records[0]); w.writeheader(); w.writerows(records)
 (out/'provenance.json').write_text(json.dumps({'method':'AnomalyCLIP (official code, prompt learner trained on CODEBRIM train, 15 epochs, val-best, seed 111)','checkpoint':a.checkpoint,'sha256':hashlib.sha256(Path(a.checkpoint).read_bytes()).hexdigest(),'data':a.data,'split':a.split,'count':len(records),'sigma':a.sigma},indent=2))
 print('INFERENCE_COMPLETE',len(records),flush=True)
if __name__=='__main__': main()
