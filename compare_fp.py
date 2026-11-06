"""False-positive comparison at matched TPR for saved binary maps (audit-design protocol, label-free part).
Usage: python compare_fp.py RUN [RUN ...] [--exclude eval_exclude_normals.txt --suffix _clean]
Writes runs/compare_fp<suffix>.json keyed by run directory."""
import argparse,csv,json
from pathlib import Path
import numpy as np
from PIL import Image
from eval_filter import load_exclude,filter_rows,union_mask
ap=argparse.ArgumentParser(); ap.add_argument('runs',nargs='+'); ap.add_argument('--exclude',default=None); ap.add_argument('--suffix',default=''); ap.add_argument('--data',default='/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM'); ap.add_argument('--split',default='val'); a=ap.parse_args()
data=Path(a.data)/a.split; excl=load_exclude(a.exclude)
out={}
for run in a.runs:
 r=Path(run); rows=filter_rows(list(csv.DictReader((r/"predictions.csv").open())),excl); pos=[];neg=[];nm=[]
 for row in rows:
  s=np.load(r/"maps"/(row["sample"]+".npy")).astype(np.float32)
  if row["label"]=="1":
   g=union_mask(data/"annotated"/(row["sample"]+".png"))
   pos.append(s[g]); neg.append(s[~g])
  else: nm.append(s.ravel())
 pos=np.concatenate(pos); neg=np.concatenate(neg); nm=np.concatenate(nm); res={'n_normal':len(nm)//(518*518),'n_anomaly':len(rows)-len(nm)//(518*518),'exclude':a.exclude}
 for tpr in (.5,.8,.9):
  thr=float(np.quantile(pos,1-tpr)); res[f"tpr{tpr}"]={"threshold":thr,"normal_img_flagged_area":float((nm>=thr).mean()),"anomaly_img_bg_fpr":float((neg>=thr).mean())}
 res["normal_img_flagged_area@0.5"]=float((nm>=.5).mean()); res["normal_img_max_mean"]=float(np.mean([x.max() for x in np.split(nm,len(nm)//(518*518))]))
 out[run]=res; print(run,json.dumps(res,indent=1),flush=True)
Path(f"runs/compare_fp{a.suffix}.json").write_text(json.dumps(out,indent=2))
