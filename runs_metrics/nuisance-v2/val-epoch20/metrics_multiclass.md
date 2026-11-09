## runs/nuisance-v2/val-epoch20 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.977 | 0.405 | 0.246 | 0.318 (0.65) | 0.001 |
| Crack | 165419 | gated | 0.960 | 0.442 | 0.342 | 0.354 (0.15) | 0.000 |
| Crack | 165419 | nugated | 0.977 | 0.415 | 0.314 | 0.320 (0.40) | 0.000 |
| Corrosion | 402682 | typed | 0.991 | 0.795 | 0.472 | 0.543 (0.90) | 0.004 |
| Corrosion | 402682 | gated | 0.954 | 0.741 | 0.505 | 0.545 (0.75) | 0.002 |
| Corrosion | 402682 | nugated | 0.990 | 0.807 | 0.495 | 0.566 (0.85) | 0.003 |
| Spalling | 1593045 | typed | 0.996 | 0.855 | 0.578 | 0.594 (0.70) | 0.010 |
| Spalling | 1593045 | gated | 0.995 | 0.872 | 0.650 | 0.650 (0.35) | 0.005 |
| Spalling | 1593045 | nugated | 0.996 | 0.861 | 0.585 | 0.593 (0.55) | 0.008 |
| Efflorescence | 4995329 | typed | 0.992 | 0.831 | 0.526 | 0.612 (0.05) | 0.002 |
| Efflorescence | 4995329 | gated | 0.983 | 0.786 | 0.383 | 0.495 (0.05) | 0.001 |
| Efflorescence | 4995329 | nugated | 0.992 | 0.831 | 0.474 | 0.574 (0.05) | 0.002 |

typed: mIoU@0.3 0.455, mIoU_best 0.517, mAP 0.722; gated: mIoU@0.3 0.470, mIoU_best 0.511, mAP 0.710; nugated: mIoU@0.3 0.467, mIoU_best 0.513, mAP 0.728
P-AUPRO (binary map) 0.8058
