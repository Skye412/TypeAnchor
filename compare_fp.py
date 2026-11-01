"""False-positive comparison at matched TPR for saved binary maps (audit-design protocol, label-free part).
Usage: python compare_fp.py runs/nuisance-v0/val-epoch20 runs/ablation-no-nuisance/val-epoch20 ..."""
import csv,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
data=Path("/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM/val")
out={}
for run in sys.argv[1:]:
 r=Path(run); rows=list(csv.DictReader((r/"predictions.csv").open())); pos=[];neg=[];nm=[]
 for row in rows:
  s=np.load(r/"maps"/(row["sample"]+".npy")).astype(np.float32)
  if row["label"]=="1":
   g=np.asarray(Image.open(data/"annotated"/(row["sample"]+".png")).convert("L").resize((518,518),Image.Resampling.BILINEAR))>127
   pos.append(s[g]); neg.append(s[~g])
  else: nm.append(s.ravel())
 pos=np.concatenate(pos); neg=np.concatenate(neg); nm=np.concatenate(nm); res={}
 for tpr in (.5,.8,.9):
  thr=float(np.quantile(pos,1-tpr)); res[f"tpr{tpr}"]={"threshold":thr,"normal_img_flagged_area":float((nm>=thr).mean()),"anomaly_img_bg_fpr":float((neg>=thr).mean())}
 res["normal_img_flagged_area@0.5"]=float((nm>=.5).mean()); res["normal_img_max_mean"]=float(np.mean([x.max() for x in np.split(nm,len(nm)//(518*518))]))
 out[run]=res; print(run,json.dumps(res,indent=1),flush=True)
Path("runs/compare_fp.json").write_text(json.dumps(out,indent=2))
