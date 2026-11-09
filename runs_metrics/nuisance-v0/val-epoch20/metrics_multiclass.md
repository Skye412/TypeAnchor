## runs/nuisance-v0/val-epoch20 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.950 | 0.068 | 0.081 | 0.083 (0.35) | 0.000 |
| Crack | 165419 | gated | 0.803 | 0.182 | 0.154 | 0.195 (0.10) | 0.000 |
| Corrosion | 402682 | typed | 0.988 | 0.551 | 0.364 | 0.467 (0.20) | 0.001 |
| Corrosion | 402682 | gated | 0.936 | 0.743 | 0.355 | 0.615 (0.15) | 0.000 |
| Spalling | 1593045 | typed | 0.996 | 0.801 | 0.584 | 0.590 (0.35) | 0.008 |
| Spalling | 1593045 | gated | 0.991 | 0.865 | 0.640 | 0.670 (0.15) | 0.003 |
| Efflorescence | 4995329 | typed | 0.987 | 0.785 | 0.574 | 0.592 (0.15) | 0.005 |
| Efflorescence | 4995329 | gated | 0.974 | 0.732 | 0.423 | 0.517 (0.05) | 0.002 |

typed: mIoU@0.3 0.401, mIoU_best 0.433, mAP 0.551; gated: mIoU@0.3 0.393, mIoU_best 0.499, mAP 0.630
P-AUPRO (binary map) 0.7078
