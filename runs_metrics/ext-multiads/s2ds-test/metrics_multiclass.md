## runs/ext-multiads/s2ds-test per-class (test, 447 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 107645 | typed | 0.982 | 0.139 | 0.113 | 0.142 (0.55) | 0.001 |
| Crack | 107645 | gated | 0.972 | 0.134 | 0.136 | 0.141 (0.40) | 0.000 |
| Corrosion | 2041564 | typed | 0.983 | 0.591 | 0.405 | 0.405 (0.30) | 0.002 |
| Corrosion | 2041564 | gated | 0.975 | 0.546 | 0.348 | 0.361 (0.25) | 0.000 |
| Spalling | 9401631 | typed | 0.976 | 0.726 | 0.538 | 0.570 (0.35) | 0.036 |
| Spalling | 9401631 | gated | 0.974 | 0.704 | 0.506 | 0.548 (0.20) | 0.015 |
| Efflorescence | 2162061 | typed | 0.967 | 0.656 | 0.478 | 0.478 (0.30) | 0.005 |
| Efflorescence | 2162061 | gated | 0.969 | 0.650 | 0.409 | 0.470 (0.20) | 0.001 |

typed: mIoU@0.3 0.384, mIoU_best 0.399, mAP 0.528; gated: mIoU@0.3 0.350, mIoU_best 0.380, mAP 0.509
P-AUPRO (binary map) 0.6142
