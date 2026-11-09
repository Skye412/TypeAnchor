## runs/ablation-v2-no-nuisance-s12/val-epoch20 per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.982 | 0.354 | 0.249 | 0.250 (0.35) | 0.000 |
| Crack | 165419 | gated | 0.973 | 0.438 | 0.279 | 0.341 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.982 | 0.363 | 0.233 | 0.260 (0.15) | 0.000 |
| Corrosion | 402682 | typed | 0.997 | 0.910 | 0.716 | 0.717 (0.25) | 0.000 |
| Corrosion | 402682 | gated | 0.993 | 0.880 | 0.701 | 0.706 (0.15) | 0.000 |
| Corrosion | 402682 | nugated | 0.996 | 0.899 | 0.708 | 0.711 (0.20) | 0.000 |
| Spalling | 1593045 | typed | 0.999 | 0.966 | 0.829 | 0.839 (0.50) | 0.001 |
| Spalling | 1593045 | gated | 0.999 | 0.977 | 0.852 | 0.852 (0.25) | 0.001 |
| Spalling | 1593045 | nugated | 0.999 | 0.966 | 0.835 | 0.835 (0.30) | 0.001 |
| Efflorescence | 4995329 | typed | 0.995 | 0.899 | 0.586 | 0.699 (0.05) | 0.000 |
| Efflorescence | 4995329 | gated | 0.991 | 0.878 | 0.513 | 0.631 (0.05) | 0.000 |
| Efflorescence | 4995329 | nugated | 0.995 | 0.899 | 0.515 | 0.655 (0.05) | 0.000 |

typed: mIoU@0.3 0.595, mIoU_best 0.626, mAP 0.782; gated: mIoU@0.3 0.586, mIoU_best 0.633, mAP 0.793; nugated: mIoU@0.3 0.573, mIoU_best 0.615, mAP 0.782
P-AUPRO (binary map) 0.8591
