"""Aggregate metrics over seeds for named run groups (raw and Cleaned-Val), including matched-TPR false positives.
Usage: python summarize_seeds.py --group v2=runs/nuisance-v2,runs/nuisance-v2-s11,runs/nuisance-v2-s12 \
         --group v2-no-nuisance=runs/ablation-v2-no-nuisance,... [--out runs/summary_v2.md]
compare_fp.py is run for all listed runs (raw and clean) before aggregation."""
import argparse,json,subprocess,sys
from pathlib import Path
import numpy as np
ap=argparse.ArgumentParser(); ap.add_argument('--group',action='append',required=True); ap.add_argument('--out',default='runs/summary_seeds.md'); ap.add_argument('--exclude',default='eval_exclude_normals.txt'); a=ap.parse_args()
groups={g.split('=')[0]:g.split('=')[1].split(',') for g in a.group}
vals=[r+'/val-epoch20' for rs in groups.values() for r in rs]
subprocess.run([sys.executable,'compare_fp.py',*vals,'--suffix','_seeds'],check=True,capture_output=True)
subprocess.run([sys.executable,'compare_fp.py',*vals,'--exclude',a.exclude,'--suffix','_seeds_clean'],check=True,capture_output=True)
fp={'':json.loads(Path('runs/compare_fp_seeds.json').read_text()),'_clean':json.loads(Path('runs/compare_fp_seeds_clean.json').read_text())}
def load(run,suf):
 v=Path(run)/'val-epoch20'; m=json.loads((v/f'metrics{suf}.json').read_text()); mm=json.loads((v/f'metrics_multiclass{suf}.json').read_text()); f=fp[suf][str(v)]
 return {'I-AUROC':100*m['image_metrics']['I-AUROC'],'I-AP':100*m['image_metrics']['I-AP'],'P-AUROC':100*m['pixel_metrics']['P-AUROC'],'P-AP':100*m['pixel_metrics']['P-AP'],'P-F1max':100*m['pixel_metrics']['P-F1max'],'P-AUPRO':100*mm['P-AUPRO'],
         'mAP_typed':100*mm['mAP_typed'],'mIoU@0.3_typed':100*mm['mIoU@0.3_typed'],'Crack_AP_typed':100*mm['per_class']['Crack']['typed']['P-AP'],
         'FP@TPR0.8(%)':100*f['tpr0.8']['normal_img_flagged_area'],'FP@TPR0.9(%)':100*f['tpr0.9']['normal_img_flagged_area'],'bgFPR@TPR0.8(%)':100*f['tpr0.8']['anomaly_img_bg_fpr']}
keys=['I-AUROC','I-AP','P-AUROC','P-AP','P-F1max','P-AUPRO','mAP_typed','mIoU@0.3_typed','Crack_AP_typed','FP@TPR0.8(%)','FP@TPR0.9(%)','bgFPR@TPR0.8(%)']
lines=[]; summary={}
for suf,title in (('','原集 val 400'),('_clean','Cleaned-Val 379')):
 lines+=[f'## {title}（均值 ± 标准差，n = 种子数）','','| 指标 | '+' | '.join(f'{g} (n={len(rs)})' for g,rs in groups.items())+' |','|---|'+'---|'*len(groups)]
 per={g:[load(r,suf) for r in rs] for g,rs in groups.items()}
 summary[suf]={g:{k:(float(np.mean([d[k] for d in ds])),float(np.std([d[k] for d in ds]))) for k in keys} for g,ds in per.items()}
 for k in keys: lines.append(f'| {k} | '+' | '.join('%.2f ± %.2f'%summary[suf][g][k] for g in groups)+' |')
 lines.append('')
 lines.append('逐种子：');
 for g,ds in per.items():
  for r,d in zip(groups[g],ds): lines.append(f'- {r}: '+', '.join(f'{k} {d[k]:.2f}' for k in keys))
 lines.append('')
Path(a.out).write_text('\n'.join(lines)+'\n',encoding='utf-8'); Path(a.out).with_suffix('.json').write_text(json.dumps({'groups':groups,'summary':summary},indent=2),encoding='utf-8')
print('\n'.join(lines))
