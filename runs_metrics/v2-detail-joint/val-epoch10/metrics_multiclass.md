## runs/v2-detail-joint/val-epoch10 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.964 | 0.378 | 0.180 | 0.254 (0.05) | 0.000 |
| Crack | 165419 | gated | 0.961 | 0.413 | 0.171 | 0.258 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.964 | 0.375 | 0.155 | 0.243 (0.05) | 0.000 |
| Corrosion | 402682 | typed | 0.990 | 0.798 | 0.586 | 0.587 (0.35) | 0.001 |
| Corrosion | 402682 | gated | 0.977 | 0.792 | 0.590 | 0.590 (0.30) | 0.001 |
| Corrosion | 402682 | nugated | 0.990 | 0.796 | 0.586 | 0.586 (0.30) | 0.001 |
| Spalling | 1593045 | typed | 0.995 | 0.824 | 0.549 | 0.623 (0.75) | 0.014 |
| Spalling | 1593045 | gated | 0.995 | 0.861 | 0.577 | 0.659 (0.70) | 0.012 |
| Spalling | 1593045 | nugated | 0.995 | 0.833 | 0.580 | 0.633 (0.65) | 0.011 |
| Efflorescence | 4995329 | typed | 0.993 | 0.849 | 0.623 | 0.663 (0.05) | 0.004 |
| Efflorescence | 4995329 | gated | 0.993 | 0.855 | 0.596 | 0.669 (0.05) | 0.003 |
| Efflorescence | 4995329 | nugated | 0.993 | 0.849 | 0.582 | 0.657 (0.05) | 0.003 |

typed: mIoU@0.3 0.485, mIoU_best 0.532, mAP 0.712; gated: mIoU@0.3 0.483, mIoU_best 0.544, mAP 0.730; nugated: mIoU@0.3 0.476, mIoU_best 0.530, mAP 0.713
P-AUPRO (binary map) 0.7485
