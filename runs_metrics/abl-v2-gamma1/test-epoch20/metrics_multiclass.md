## runs/abl-v2-gamma1/test-epoch20 per-class (test, 809 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 366536 | typed | 0.841 | 0.110 | 0.044 | 0.076 (0.05) | 0.000 |
| Crack | 366536 | gated | 0.723 | 0.118 | 0.044 | 0.086 (0.05) | 0.000 |
| Crack | 366536 | nugated | 0.840 | 0.109 | 0.030 | 0.059 (0.05) | 0.000 |
| Corrosion | 2066692 | typed | 0.972 | 0.806 | 0.574 | 0.576 (0.20) | 0.002 |
| Corrosion | 2066692 | gated | 0.922 | 0.698 | 0.494 | 0.503 (0.15) | 0.000 |
| Corrosion | 2066692 | nugated | 0.972 | 0.805 | 0.564 | 0.571 (0.15) | 0.001 |
| Spalling | 10007679 | typed | 0.925 | 0.766 | 0.453 | 0.546 (0.05) | 0.003 |
| Spalling | 10007679 | gated | 0.804 | 0.593 | 0.370 | 0.428 (0.05) | 0.001 |
| Spalling | 10007679 | nugated | 0.925 | 0.766 | 0.413 | 0.505 (0.05) | 0.002 |
| Efflorescence | 9640891 | typed | 0.973 | 0.694 | 0.437 | 0.480 (0.05) | 0.003 |
| Efflorescence | 9640891 | gated | 0.836 | 0.551 | 0.323 | 0.382 (0.05) | 0.001 |
| Efflorescence | 9640891 | nugated | 0.972 | 0.692 | 0.393 | 0.466 (0.05) | 0.002 |

typed: mIoU@0.3 0.377, mIoU_best 0.420, mAP 0.594; gated: mIoU@0.3 0.308, mIoU_best 0.350, mAP 0.490; nugated: mIoU@0.3 0.350, mIoU_best 0.400, mAP 0.593
P-AUPRO (binary map) 0.7199
