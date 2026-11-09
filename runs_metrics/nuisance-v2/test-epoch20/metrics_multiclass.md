## runs/nuisance-v2/test-epoch20 per-class (test, 809 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 366536 | typed | 0.858 | 0.092 | 0.030 | 0.055 (0.05) | 0.000 |
| Crack | 366536 | gated | 0.841 | 0.120 | 0.025 | 0.048 (0.05) | 0.000 |
| Crack | 366536 | nugated | 0.856 | 0.086 | 0.022 | 0.042 (0.05) | 0.000 |
| Corrosion | 2066692 | typed | 0.981 | 0.812 | 0.593 | 0.598 (0.15) | 0.002 |
| Corrosion | 2066692 | gated | 0.979 | 0.818 | 0.573 | 0.620 (0.05) | 0.001 |
| Corrosion | 2066692 | nugated | 0.981 | 0.821 | 0.586 | 0.599 (0.10) | 0.002 |
| Spalling | 10007679 | typed | 0.931 | 0.747 | 0.437 | 0.486 (0.05) | 0.002 |
| Spalling | 10007679 | gated | 0.907 | 0.710 | 0.407 | 0.466 (0.05) | 0.001 |
| Spalling | 10007679 | nugated | 0.931 | 0.744 | 0.416 | 0.469 (0.05) | 0.002 |
| Efflorescence | 9640891 | typed | 0.968 | 0.625 | 0.371 | 0.403 (0.05) | 0.004 |
| Efflorescence | 9640891 | gated | 0.923 | 0.575 | 0.319 | 0.355 (0.05) | 0.002 |
| Efflorescence | 9640891 | nugated | 0.966 | 0.624 | 0.351 | 0.389 (0.05) | 0.003 |

typed: mIoU@0.3 0.357, mIoU_best 0.386, mAP 0.569; gated: mIoU@0.3 0.331, mIoU_best 0.372, mAP 0.556; nugated: mIoU@0.3 0.344, mIoU_best 0.375, mAP 0.569
P-AUPRO (binary map) 0.7351
