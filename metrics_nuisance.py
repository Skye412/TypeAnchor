"""Exact rank-based AUROC, AP and max F1 for saved validation maps.

Usage: python metrics_nuisance.py [run_dir] [split] [--exclude list.txt --suffix _clean]
"""
import argparse,csv,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
from sklearn.metrics import roc_auc_score,average_precision_score,precision_recall_curve
from eval_filter import load_exclude,filter_rows
ap=argparse.ArgumentParser(); ap.add_argument('run',nargs='?',default='runs/nuisance-v0/val-epoch20'); ap.add_argument('split',nargs='?',default='val'); ap.add_argument('--exclude',default=None); ap.add_argument('--suffix',default=''); ap.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); a=ap.parse_args()
r=Path(a.run); split=a.split
data=Path(a.data)/split
rows=filter_rows(list(csv.DictReader((r/'predictions.csv').open())),load_exclude(a.exclude)); labels=np.array([int(x['label']) for x in rows]); scores=np.array([float(x['score']) for x in rows])
pr,rc,_=precision_recall_curve(labels,scores); image={'I-AUROC':roc_auc_score(labels,scores),'I-AP':average_precision_score(labels,scores),'I-F1max':float(np.max(2*pr*rc/np.maximum(pr+rc,1e-30)))}
# Original binary labels are resized by the official baseline preprocessing.
y=[]; pred=[]
for row in rows:
 sample=row['sample']; p=data/'annotated'/f'{sample}.png'
 if row['label']=='1':
  im=Image.open(p).convert('L').resize((518,518),Image.Resampling.BILINEAR); target=np.asarray(im)>127
 else:target=np.zeros((518,518),bool)
 y.append(target.reshape(-1)); pred.append(np.load(r/'maps'/f'{sample}.npy').reshape(-1))
y=np.concatenate(y);pred=np.concatenate(pred); order=np.argsort(pred,kind='stable')[::-1]; sorted_y=y[order]; sorted_p=pred[order]; ends=np.r_[np.flatnonzero(np.diff(sorted_p)!=0),len(y)-1]; tp=np.cumsum(sorted_y,dtype=np.int64)[ends]; fp=ends+1-tp; total=tp[-1]; neg=len(y)-total
rec=tp/total; precision=tp/(tp+fp); fpr=fp/neg; tpr=rec
pixel={'P-AUROC':float(np.trapz(np.r_[0,tpr],np.r_[0,fpr])),'P-AP':float(np.sum(np.diff(np.r_[0,rec])*precision)),'P-F1max':float(np.max(2*precision*rec/np.maximum(precision+rec,1e-30)))}
result={'images':len(rows),'split':split,'exclude':a.exclude,'image_metrics':image,'pixel_metrics':pixel,'pixel_ground_truth':'original flattened union mask resized to 518','P-AUPRO':'see metrics_multiclass.json'}
(r/f'metrics{a.suffix}.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True)
