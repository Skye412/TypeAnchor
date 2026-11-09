## runs/ablation-no-nuisance/val-epoch20 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.977 | 0.086 | 0.087 | 0.089 (0.35) | 0.001 |
| Crack | 165419 | gated | 0.920 | 0.339 | 0.183 | 0.296 (0.10) | 0.000 |
| Corrosion | 402682 | typed | 0.990 | 0.442 | 0.355 | 0.413 (0.20) | 0.002 |
| Corrosion | 402682 | gated | 0.933 | 0.621 | 0.365 | 0.505 (0.15) | 0.001 |
| Spalling | 1593045 | typed | 0.996 | 0.821 | 0.574 | 0.598 (0.45) | 0.010 |
| Spalling | 1593045 | gated | 0.995 | 0.900 | 0.707 | 0.717 (0.20) | 0.003 |
| Efflorescence | 4995329 | typed | 0.980 | 0.725 | 0.533 | 0.553 (0.20) | 0.007 |
| Efflorescence | 4995329 | gated | 0.951 | 0.667 | 0.371 | 0.463 (0.05) | 0.003 |

typed: mIoU@0.3 0.387, mIoU_best 0.413, mAP 0.519; gated: mIoU@0.3 0.406, mIoU_best 0.495, mAP 0.632
P-AUPRO (binary map) 0.7262
