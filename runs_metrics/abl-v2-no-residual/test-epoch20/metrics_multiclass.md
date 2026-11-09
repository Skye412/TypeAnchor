## runs/abl-v2-no-residual/test-epoch20 per-class (test, 809 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 366536 | typed | 0.778 | 0.075 | 0.032 | 0.060 (0.05) | 0.000 |
| Crack | 366536 | gated | 0.721 | 0.096 | 0.028 | 0.059 (0.05) | 0.000 |
| Crack | 366536 | nugated | 0.777 | 0.071 | 0.024 | 0.047 (0.05) | 0.000 |
| Corrosion | 2066692 | typed | 0.977 | 0.835 | 0.610 | 0.611 (0.40) | 0.002 |
| Corrosion | 2066692 | gated | 0.974 | 0.803 | 0.594 | 0.597 (0.20) | 0.001 |
| Corrosion | 2066692 | nugated | 0.977 | 0.828 | 0.604 | 0.604 (0.25) | 0.001 |
| Spalling | 10007679 | typed | 0.923 | 0.761 | 0.450 | 0.518 (0.05) | 0.002 |
| Spalling | 10007679 | gated | 0.906 | 0.740 | 0.423 | 0.491 (0.05) | 0.001 |
| Spalling | 10007679 | nugated | 0.923 | 0.761 | 0.424 | 0.494 (0.05) | 0.002 |
| Efflorescence | 9640891 | typed | 0.948 | 0.615 | 0.358 | 0.392 (0.05) | 0.004 |
| Efflorescence | 9640891 | gated | 0.882 | 0.538 | 0.298 | 0.337 (0.05) | 0.002 |
| Efflorescence | 9640891 | nugated | 0.946 | 0.610 | 0.332 | 0.379 (0.05) | 0.003 |

typed: mIoU@0.3 0.362, mIoU_best 0.395, mAP 0.572; gated: mIoU@0.3 0.335, mIoU_best 0.371, mAP 0.544; nugated: mIoU@0.3 0.346, mIoU_best 0.381, mAP 0.568
P-AUPRO (binary map) 0.7116
