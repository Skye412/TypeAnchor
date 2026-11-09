## runs/v2-more10/s2ds-test per-class (test, 447 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 107645 | typed | 0.879 | 0.113 | 0.108 | 0.109 (0.35) | 0.000 |
| Crack | 107645 | gated | 0.878 | 0.140 | 0.114 | 0.137 (0.05) | 0.000 |
| Crack | 107645 | nugated | 0.879 | 0.118 | 0.103 | 0.115 (0.10) | 0.000 |
| Corrosion | 2041564 | typed | 0.967 | 0.580 | 0.309 | 0.355 (0.05) | 0.000 |
| Corrosion | 2041564 | gated | 0.965 | 0.581 | 0.309 | 0.359 (0.05) | 0.000 |
| Corrosion | 2041564 | nugated | 0.965 | 0.562 | 0.292 | 0.338 (0.05) | 0.000 |
| Spalling | 9401631 | typed | 0.966 | 0.684 | 0.539 | 0.569 (0.05) | 0.007 |
| Spalling | 9401631 | gated | 0.967 | 0.691 | 0.528 | 0.569 (0.05) | 0.007 |
| Spalling | 9401631 | nugated | 0.966 | 0.666 | 0.503 | 0.561 (0.05) | 0.006 |
| Efflorescence | 2162061 | typed | 0.914 | 0.543 | 0.197 | 0.322 (0.05) | 0.001 |
| Efflorescence | 2162061 | gated | 0.908 | 0.541 | 0.179 | 0.296 (0.05) | 0.000 |
| Efflorescence | 2162061 | nugated | 0.913 | 0.539 | 0.160 | 0.267 (0.05) | 0.001 |

typed: mIoU@0.3 0.288, mIoU_best 0.339, mAP 0.480; gated: mIoU@0.3 0.282, mIoU_best 0.340, mAP 0.488; nugated: mIoU@0.3 0.264, mIoU_best 0.320, mAP 0.471
P-AUPRO (binary map) 0.4330
