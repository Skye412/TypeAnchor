## runs/nuisance-v2-s11/val-epoch20 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.983 | 0.366 | 0.249 | 0.270 (0.50) | 0.000 |
| Crack | 165419 | gated | 0.983 | 0.433 | 0.305 | 0.321 (0.10) | 0.000 |
| Crack | 165419 | nugated | 0.983 | 0.375 | 0.268 | 0.271 (0.25) | 0.000 |
| Corrosion | 402682 | typed | 0.996 | 0.820 | 0.457 | 0.586 (0.90) | 0.004 |
| Corrosion | 402682 | gated | 0.992 | 0.817 | 0.485 | 0.613 (0.85) | 0.003 |
| Corrosion | 402682 | nugated | 0.996 | 0.822 | 0.489 | 0.608 (0.80) | 0.003 |
| Spalling | 1593045 | typed | 0.997 | 0.821 | 0.548 | 0.610 (0.80) | 0.014 |
| Spalling | 1593045 | gated | 0.997 | 0.871 | 0.604 | 0.668 (0.75) | 0.010 |
| Spalling | 1593045 | nugated | 0.997 | 0.837 | 0.583 | 0.610 (0.60) | 0.011 |
| Efflorescence | 4995329 | typed | 0.995 | 0.883 | 0.659 | 0.729 (0.05) | 0.002 |
| Efflorescence | 4995329 | gated | 0.995 | 0.890 | 0.651 | 0.728 (0.05) | 0.002 |
| Efflorescence | 4995329 | nugated | 0.995 | 0.889 | 0.593 | 0.702 (0.05) | 0.002 |

typed: mIoU@0.3 0.478, mIoU_best 0.548, mAP 0.723; gated: mIoU@0.3 0.511, mIoU_best 0.582, mAP 0.753; nugated: mIoU@0.3 0.483, mIoU_best 0.548, mAP 0.731
P-AUPRO (binary map) 0.8120
