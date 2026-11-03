"""P-AUPRO for the binary map and per-class (multi-label) metrics for the typed maps of a saved evaluation.

Usage: python metrics_multiclass.py --run runs/nuisance-v0/val-epoch20 [--split val]
Binary ground truth: original flattened union mask resized to 518 (bilinear, >127), as in metrics_nuisance.py
and the official baseline. P-AUPRO uses metrics.AUPRO (fpr_limit 0.3) at 518, the evaluator used by runs/baseline-v1.
Per-class ground truth: multiclass_annotations/masks/<sample>__<Class>.png resized to 518 (nearest); classes may overlap
(dacl10k-style multi-label protocol). Two prediction variants per class: typed = pi_c, gated = pi_c * residual.
Per class: pixel AUROC/AP (threshold-free), IoU at fixed threshold 0.3, IoU at the best threshold on this split
(oracle, optimistic), and flagged area on normal images at threshold 0.3.
"""
import argparse,csv,json,sys
from pathlib import Path
import numpy as np
import torch
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from metrics import AUPRO
CLASSES=['Crack','Corrosion','Spalling','Efflorescence']
THRS=np.round(np.linspace(.05,.95,19),2)

def rank_metrics(y,s):
 """Exact AUROC/AP via a full sort (same procedure as metrics_nuisance.py)."""
 order=np.argsort(s,kind='stable')[::-1]; sy=y[order]; sp=s[order]; ends=np.r_[np.flatnonzero(np.diff(sp)!=0),len(y)-1]
 tp=np.cumsum(sy,dtype=np.int64)[ends]; fp=ends+1-tp; total=tp[-1]; neg=len(y)-total
 rec=tp/total; prec=tp/(tp+fp); fpr=fp/neg
 return float(np.trapz(np.r_[0,rec],np.r_[0,fpr])),float(np.sum(np.diff(np.r_[0,rec])*prec))

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--run',default='runs/nuisance-v0/val-epoch20'); ap.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); ap.add_argument('--split',default='val'); ap.add_argument('--skip-aupro',action='store_true'); ap.add_argument('--aupro-device',default='cpu'); ap.add_argument('--exclude',default=None); ap.add_argument('--suffix',default=''); a=ap.parse_args()
 from eval_filter import load_exclude,filter_rows
 r=Path(a.run); data=Path(a.data)/a.split; rows=filter_rows(list(csv.DictReader((r/'predictions.csv').open())),load_exclude(a.exclude))
 out={'images':len(rows),'split':a.split,'exclude':a.exclude}
 # ---- P-AUPRO on binary maps (same evaluator and resolution as baseline-v1) ----
 if not a.skip_aupro:
  gts=[]; prs=[]
  for row in rows:
   if row['label']=='1': g=np.asarray(Image.open(data/'annotated'/(row['sample']+'.png')).convert('L').resize((518,518),Image.Resampling.BILINEAR))>127
   else: g=np.zeros((518,518),bool)
   gts.append(torch.from_numpy(g.astype(np.int32))); prs.append(torch.from_numpy(np.load(r/'maps'/(row['sample']+'.npy')).astype(np.float32)))
  device=a.aupro_device
  aupro=AUPRO().to(device); out['P-AUPRO']=float(aupro(torch.stack(prs).to(device),torch.stack(gts).to(device)).item())
  out['P-AUPRO_note']='metrics.AUPRO fpr_limit=0.3 at 518, union GT bilinear>127, identical to the baseline-v1 evaluator'
  del gts,prs; torch.cuda.empty_cache(); print('P-AUPRO',out['P-AUPRO'],flush=True)
 # ---- per-class multi-label metrics on typed maps ----
 if not (r/'typed').exists():
  out['per_class']='typed maps not saved'; (r/('metrics_multiclass'+a.suffix+'.json')).write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2)); return
 per={}; has_nu=(r/'nu').exists(); variants=['typed','gated']+(['nugated'] if has_nu else [])
 for ci,c in enumerate(CLASSES):
  ys=[]; preds={v:[] for v in variants}; nms={v:[] for v in variants}
  for row in rows:
   t=np.load(r/'typed'/(row['sample']+'.npy'))[ci].astype(np.float32); res=np.load(r/'residual'/(row['sample']+'.npy')).astype(np.float32)
   cur={'typed':t,'gated':t*res}
   if has_nu: cur['nugated']=t*np.load(r/'nu'/(row['sample']+'.npy')).astype(np.float32)
   if row['label']=='1': g=np.asarray(Image.open(data/'multiclass_annotations'/'masks'/(row['sample']+'__'+c+'.png')).convert('L').resize((518,518),Image.Resampling.NEAREST))>0
   else:
    g=np.zeros((518,518),bool)
    for v in variants: nms[v].append(cur[v].ravel())
   ys.append(g.ravel())
   for v in variants: preds[v].append(cur[v].ravel())
  y=np.concatenate(ys); per[c]={'gt_pixels':int(y.sum())}
  for name in variants:
   pred=preds[name]; nm=nms[name]
   s=np.concatenate(pred); auroc,apv=rank_metrics(y,s)
   ious=[]
   for th in THRS:
    pb=s>=th; inter=int((pb&y).sum()); union=int((pb|y).sum()); ious.append(inter/max(union,1))
   ious=np.array(ious); best=int(ious.argmax()); nmc=np.concatenate(nm)
   per[c][name]={'P-AUROC':auroc,'P-AP':apv,'IoU@0.3':float(ious[np.isclose(THRS,.3)][0]),'IoU_best':float(ious[best]),'thr_best':float(THRS[best]),'normal_flagged_area@0.3':float((nmc>=.3).mean())}
  print(c,json.dumps(per[c]),flush=True)
 out['per_class']=per; out['variants']=variants
 for name in variants:
  out['mIoU@0.3_'+name]=float(np.mean([per[c][name]['IoU@0.3'] for c in CLASSES])); out['mIoU_best_'+name]=float(np.mean([per[c][name]['IoU_best'] for c in CLASSES])); out['mAP_'+name]=float(np.mean([per[c][name]['P-AP'] for c in CLASSES]))
 out['per_class_note']='GT from multiclass_annotations (overlap allowed, nearest 518); IoU_best is selected on this split and is optimistic. typed = raw type probability (v0: pi_c; v2: sigmoid head), gated = typed*residual, nugated = typed*nu (v2 only, the model output)'
 (r/('metrics_multiclass'+a.suffix+'.json')).write_text(json.dumps(out,indent=2),encoding='utf-8')
 lines=['## '+str(r)+' per-class ('+a.split+', '+str(len(rows))+' images)','','| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |','|---|---|---|---|---|---|---|---|']
 for c in CLASSES:
  for name in variants:
   m=per[c][name]; lines.append('| %s | %d | %s | %.3f | %.3f | %.3f | %.3f (%.2f) | %.3f |'%(c,per[c]['gt_pixels'],name,m['P-AUROC'],m['P-AP'],m['IoU@0.3'],m['IoU_best'],m['thr_best'],m['normal_flagged_area@0.3']))
 lines+=['','; '.join('%s: mIoU@0.3 %.3f, mIoU_best %.3f, mAP %.3f'%(v,out['mIoU@0.3_'+v],out['mIoU_best_'+v],out['mAP_'+v]) for v in variants)]
 if 'P-AUPRO' in out: lines.append('P-AUPRO (binary map) %.4f'%out['P-AUPRO'])
 (r/('metrics_multiclass'+a.suffix+'.md')).write_text('\n'.join(lines)+'\n',encoding='utf-8'); print('\n'.join(lines),flush=True)
if __name__=='__main__': main()
