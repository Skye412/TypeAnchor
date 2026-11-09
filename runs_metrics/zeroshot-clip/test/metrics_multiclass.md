## runs/zeroshot-clip/test per-class (test, 809 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 366536 | typed | 0.689 | 0.005 | 0.002 | 0.006 (0.95) | 1.000 |
| Crack | 366536 | gated | 0.689 | 0.005 | 0.002 | 0.011 (0.95) | 0.988 |
| Corrosion | 2066692 | typed | 0.913 | 0.338 | 0.030 | 0.259 (0.70) | 0.260 |
| Corrosion | 2066692 | gated | 0.887 | 0.243 | 0.039 | 0.191 (0.60) | 0.181 |
| Spalling | 10007679 | typed | 0.644 | 0.089 | 0.055 | 0.084 (0.55) | 0.620 |
| Spalling | 10007679 | gated | 0.579 | 0.068 | 0.053 | 0.064 (0.45) | 0.458 |
| Efflorescence | 9640891 | typed | 0.631 | 0.062 | 0.011 | 0.060 (0.05) | 0.011 |
| Efflorescence | 9640891 | gated | 0.615 | 0.059 | 0.007 | 0.059 (0.05) | 0.007 |

typed: mIoU@0.3 0.025, mIoU_best 0.102, mAP 0.124; gated: mIoU@0.3 0.025, mIoU_best 0.081, mAP 0.094
P-AUPRO (binary map) 0.1888
