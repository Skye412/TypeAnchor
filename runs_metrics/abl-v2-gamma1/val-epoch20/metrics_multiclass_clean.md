## runs/abl-v2-gamma1/val-epoch20 per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.980 | 0.410 | 0.286 | 0.304 (0.45) | 0.000 |
| Crack | 165419 | gated | 0.946 | 0.469 | 0.317 | 0.356 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.980 | 0.422 | 0.299 | 0.313 (0.20) | 0.000 |
| Corrosion | 402682 | typed | 0.997 | 0.897 | 0.696 | 0.696 (0.35) | 0.000 |
| Corrosion | 402682 | gated | 0.934 | 0.755 | 0.595 | 0.601 (0.20) | 0.000 |
| Corrosion | 402682 | nugated | 0.997 | 0.884 | 0.683 | 0.684 (0.25) | 0.000 |
| Spalling | 1593045 | typed | 0.999 | 0.960 | 0.803 | 0.819 (0.15) | 0.000 |
| Spalling | 1593045 | gated | 0.980 | 0.936 | 0.728 | 0.803 (0.05) | 0.000 |
| Spalling | 1593045 | nugated | 0.999 | 0.959 | 0.748 | 0.814 (0.05) | 0.000 |
| Efflorescence | 4995329 | typed | 0.993 | 0.858 | 0.564 | 0.666 (0.05) | 0.001 |
| Efflorescence | 4995329 | gated | 0.964 | 0.821 | 0.406 | 0.522 (0.05) | 0.000 |
| Efflorescence | 4995329 | nugated | 0.993 | 0.859 | 0.490 | 0.621 (0.05) | 0.000 |

typed: mIoU@0.3 0.587, mIoU_best 0.621, mAP 0.781; gated: mIoU@0.3 0.512, mIoU_best 0.571, mAP 0.746; nugated: mIoU@0.3 0.555, mIoU_best 0.608, mAP 0.781
P-AUPRO (binary map) 0.8738
