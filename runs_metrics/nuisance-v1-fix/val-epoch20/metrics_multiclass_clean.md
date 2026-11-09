## runs/nuisance-v1-fix/val-epoch20 per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.983 | 0.091 | 0.089 | 0.091 (0.20) | 0.000 |
| Crack | 165419 | gated | 0.951 | 0.345 | 0.217 | 0.340 (0.10) | 0.000 |
| Corrosion | 402682 | typed | 0.996 | 0.704 | 0.419 | 0.607 (0.15) | 0.000 |
| Corrosion | 402682 | gated | 0.961 | 0.802 | 0.307 | 0.673 (0.10) | 0.000 |
| Spalling | 1593045 | typed | 0.998 | 0.943 | 0.814 | 0.814 (0.30) | 0.001 |
| Spalling | 1593045 | gated | 0.994 | 0.956 | 0.777 | 0.856 (0.10) | 0.000 |
| Efflorescence | 4995329 | typed | 0.991 | 0.823 | 0.619 | 0.646 (0.15) | 0.002 |
| Efflorescence | 4995329 | gated | 0.981 | 0.768 | 0.476 | 0.539 (0.10) | 0.001 |

typed: mIoU@0.3 0.485, mIoU_best 0.540, mAP 0.640; gated: mIoU@0.3 0.444, mIoU_best 0.602, mAP 0.717
P-AUPRO (binary map) 0.8022
