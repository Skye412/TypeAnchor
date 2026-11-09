## runs/v2-more10/val-epoch10 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.955 | 0.354 | 0.248 | 0.279 (0.50) | 0.000 |
| Crack | 165419 | gated | 0.948 | 0.425 | 0.297 | 0.328 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.954 | 0.365 | 0.282 | 0.282 (0.30) | 0.000 |
| Corrosion | 402682 | typed | 0.995 | 0.857 | 0.557 | 0.647 (0.80) | 0.002 |
| Corrosion | 402682 | gated | 0.993 | 0.854 | 0.572 | 0.651 (0.75) | 0.002 |
| Corrosion | 402682 | nugated | 0.995 | 0.855 | 0.582 | 0.649 (0.65) | 0.002 |
| Spalling | 1593045 | typed | 0.996 | 0.874 | 0.527 | 0.654 (0.95) | 0.015 |
| Spalling | 1593045 | gated | 0.996 | 0.887 | 0.565 | 0.668 (0.85) | 0.013 |
| Spalling | 1593045 | nugated | 0.996 | 0.880 | 0.562 | 0.661 (0.75) | 0.012 |
| Efflorescence | 4995329 | typed | 0.994 | 0.859 | 0.649 | 0.685 (0.05) | 0.004 |
| Efflorescence | 4995329 | gated | 0.994 | 0.868 | 0.620 | 0.692 (0.05) | 0.003 |
| Efflorescence | 4995329 | nugated | 0.994 | 0.858 | 0.610 | 0.679 (0.05) | 0.003 |

typed: mIoU@0.3 0.495, mIoU_best 0.566, mAP 0.736; gated: mIoU@0.3 0.513, mIoU_best 0.585, mAP 0.759; nugated: mIoU@0.3 0.509, mIoU_best 0.568, mAP 0.740
P-AUPRO (binary map) 0.7657
