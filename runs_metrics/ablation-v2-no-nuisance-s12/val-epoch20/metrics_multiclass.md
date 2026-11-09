## runs/ablation-v2-no-nuisance-s12/val-epoch20 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.982 | 0.345 | 0.244 | 0.247 (0.40) | 0.000 |
| Crack | 165419 | gated | 0.973 | 0.422 | 0.274 | 0.325 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.982 | 0.354 | 0.232 | 0.255 (0.15) | 0.000 |
| Corrosion | 402682 | typed | 0.995 | 0.757 | 0.441 | 0.519 (0.85) | 0.004 |
| Corrosion | 402682 | gated | 0.991 | 0.769 | 0.459 | 0.547 (0.75) | 0.003 |
| Corrosion | 402682 | nugated | 0.995 | 0.773 | 0.460 | 0.529 (0.80) | 0.003 |
| Spalling | 1593045 | typed | 0.997 | 0.842 | 0.540 | 0.639 (0.85) | 0.014 |
| Spalling | 1593045 | gated | 0.997 | 0.885 | 0.602 | 0.678 (0.75) | 0.010 |
| Spalling | 1593045 | nugated | 0.997 | 0.854 | 0.574 | 0.635 (0.70) | 0.012 |
| Efflorescence | 4995329 | typed | 0.995 | 0.881 | 0.577 | 0.681 (0.05) | 0.002 |
| Efflorescence | 4995329 | gated | 0.990 | 0.855 | 0.506 | 0.617 (0.05) | 0.001 |
| Efflorescence | 4995329 | nugated | 0.995 | 0.880 | 0.508 | 0.641 (0.05) | 0.001 |

typed: mIoU@0.3 0.450, mIoU_best 0.522, mAP 0.706; gated: mIoU@0.3 0.460, mIoU_best 0.542, mAP 0.733; nugated: mIoU@0.3 0.444, mIoU_best 0.515, mAP 0.715
P-AUPRO (binary map) 0.8120
