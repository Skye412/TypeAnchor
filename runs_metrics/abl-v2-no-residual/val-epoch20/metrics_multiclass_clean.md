## runs/abl-v2-no-residual/val-epoch20 per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.973 | 0.355 | 0.254 | 0.266 (0.40) | 0.000 |
| Crack | 165419 | gated | 0.920 | 0.434 | 0.265 | 0.348 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.972 | 0.360 | 0.263 | 0.270 (0.20) | 0.000 |
| Corrosion | 402682 | typed | 0.995 | 0.905 | 0.707 | 0.725 (0.55) | 0.000 |
| Corrosion | 402682 | gated | 0.963 | 0.783 | 0.629 | 0.633 (0.40) | 0.000 |
| Corrosion | 402682 | nugated | 0.995 | 0.892 | 0.708 | 0.716 (0.50) | 0.000 |
| Spalling | 1593045 | typed | 0.998 | 0.958 | 0.790 | 0.808 (0.10) | 0.000 |
| Spalling | 1593045 | gated | 0.997 | 0.966 | 0.777 | 0.831 (0.05) | 0.000 |
| Spalling | 1593045 | nugated | 0.998 | 0.958 | 0.758 | 0.808 (0.05) | 0.000 |
| Efflorescence | 4995329 | typed | 0.970 | 0.759 | 0.423 | 0.498 (0.05) | 0.001 |
| Efflorescence | 4995329 | gated | 0.930 | 0.684 | 0.358 | 0.412 (0.05) | 0.000 |
| Efflorescence | 4995329 | nugated | 0.968 | 0.753 | 0.384 | 0.464 (0.05) | 0.000 |

typed: mIoU@0.3 0.544, mIoU_best 0.574, mAP 0.744; gated: mIoU@0.3 0.507, mIoU_best 0.556, mAP 0.717; nugated: mIoU@0.3 0.528, mIoU_best 0.564, mAP 0.741
P-AUPRO (binary map) 0.8306
