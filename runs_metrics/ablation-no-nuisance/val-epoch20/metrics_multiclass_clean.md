## runs/ablation-no-nuisance/val-epoch20 per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.978 | 0.091 | 0.092 | 0.093 (0.35) | 0.000 |
| Crack | 165419 | gated | 0.925 | 0.352 | 0.184 | 0.311 (0.05) | 0.000 |
| Corrosion | 402682 | typed | 0.992 | 0.605 | 0.458 | 0.586 (0.20) | 0.000 |
| Corrosion | 402682 | gated | 0.936 | 0.777 | 0.406 | 0.662 (0.10) | 0.000 |
| Spalling | 1593045 | typed | 0.998 | 0.910 | 0.773 | 0.776 (0.25) | 0.001 |
| Spalling | 1593045 | gated | 0.996 | 0.960 | 0.797 | 0.863 (0.10) | 0.000 |
| Efflorescence | 4995329 | typed | 0.984 | 0.779 | 0.570 | 0.599 (0.20) | 0.002 |
| Efflorescence | 4995329 | gated | 0.958 | 0.725 | 0.381 | 0.492 (0.05) | 0.001 |

typed: mIoU@0.3 0.473, mIoU_best 0.513, mAP 0.596; gated: mIoU@0.3 0.442, mIoU_best 0.582, mAP 0.704
P-AUPRO (binary map) 0.7374
