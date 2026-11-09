## runs/abl-v2-gamma0/val-epoch20 per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.965 | 0.084 | 0.071 | 0.078 (0.10) | 0.000 |
| Crack | 165419 | gated | 0.946 | 0.346 | 0.087 | 0.202 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.964 | 0.083 | 0.058 | 0.079 (0.05) | 0.000 |
| Corrosion | 402682 | typed | 0.981 | 0.800 | 0.636 | 0.656 (0.70) | 0.000 |
| Corrosion | 402682 | gated | 0.966 | 0.845 | 0.668 | 0.668 (0.25) | 0.000 |
| Corrosion | 402682 | nugated | 0.981 | 0.836 | 0.645 | 0.655 (0.55) | 0.000 |
| Spalling | 1593045 | typed | 0.998 | 0.959 | 0.834 | 0.835 (0.35) | 0.000 |
| Spalling | 1593045 | gated | 0.998 | 0.974 | 0.807 | 0.850 (0.05) | 0.000 |
| Spalling | 1593045 | nugated | 0.998 | 0.959 | 0.825 | 0.833 (0.20) | 0.000 |
| Efflorescence | 4995329 | typed | 0.994 | 0.879 | 0.554 | 0.651 (0.05) | 0.001 |
| Efflorescence | 4995329 | gated | 0.991 | 0.860 | 0.407 | 0.543 (0.05) | 0.000 |
| Efflorescence | 4995329 | nugated | 0.994 | 0.877 | 0.499 | 0.610 (0.05) | 0.000 |

typed: mIoU@0.3 0.524, mIoU_best 0.555, mAP 0.681; gated: mIoU@0.3 0.492, mIoU_best 0.566, mAP 0.756; nugated: mIoU@0.3 0.507, mIoU_best 0.544, mAP 0.689
P-AUPRO (binary map) 0.7903
