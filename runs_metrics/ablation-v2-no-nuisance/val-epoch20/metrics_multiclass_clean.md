## runs/ablation-v2-no-nuisance/val-epoch20 per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.963 | 0.374 | 0.273 | 0.286 (0.40) | 0.000 |
| Crack | 165419 | gated | 0.937 | 0.434 | 0.284 | 0.344 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.962 | 0.380 | 0.281 | 0.292 (0.20) | 0.000 |
| Corrosion | 402682 | typed | 0.998 | 0.907 | 0.706 | 0.722 (0.55) | 0.000 |
| Corrosion | 402682 | gated | 0.985 | 0.848 | 0.674 | 0.675 (0.35) | 0.000 |
| Corrosion | 402682 | nugated | 0.998 | 0.895 | 0.708 | 0.712 (0.40) | 0.000 |
| Spalling | 1593045 | typed | 0.997 | 0.963 | 0.814 | 0.838 (0.10) | 0.000 |
| Spalling | 1593045 | gated | 0.997 | 0.972 | 0.795 | 0.854 (0.05) | 0.000 |
| Spalling | 1593045 | nugated | 0.997 | 0.964 | 0.782 | 0.837 (0.05) | 0.000 |
| Efflorescence | 4995329 | typed | 0.995 | 0.884 | 0.585 | 0.675 (0.05) | 0.000 |
| Efflorescence | 4995329 | gated | 0.994 | 0.878 | 0.524 | 0.620 (0.05) | 0.000 |
| Efflorescence | 4995329 | nugated | 0.995 | 0.884 | 0.530 | 0.636 (0.05) | 0.000 |

typed: mIoU@0.3 0.594, mIoU_best 0.630, mAP 0.782; gated: mIoU@0.3 0.569, mIoU_best 0.623, mAP 0.783; nugated: mIoU@0.3 0.575, mIoU_best 0.619, mAP 0.781
P-AUPRO (binary map) 0.8314
