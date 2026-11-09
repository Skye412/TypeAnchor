## runs/abl-v2-gamma1/val-epoch20 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.980 | 0.376 | 0.263 | 0.283 (0.45) | 0.001 |
| Crack | 165419 | gated | 0.946 | 0.430 | 0.300 | 0.331 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.980 | 0.389 | 0.281 | 0.290 (0.20) | 0.000 |
| Corrosion | 402682 | typed | 0.996 | 0.804 | 0.505 | 0.556 (0.65) | 0.002 |
| Corrosion | 402682 | gated | 0.933 | 0.740 | 0.574 | 0.575 (0.25) | 0.000 |
| Corrosion | 402682 | nugated | 0.996 | 0.801 | 0.529 | 0.557 (0.55) | 0.002 |
| Spalling | 1593045 | typed | 0.996 | 0.840 | 0.579 | 0.583 (0.40) | 0.009 |
| Spalling | 1593045 | gated | 0.979 | 0.877 | 0.641 | 0.675 (0.05) | 0.003 |
| Spalling | 1593045 | nugated | 0.996 | 0.841 | 0.574 | 0.576 (0.25) | 0.007 |
| Efflorescence | 4995329 | typed | 0.992 | 0.823 | 0.543 | 0.630 (0.05) | 0.004 |
| Efflorescence | 4995329 | gated | 0.964 | 0.801 | 0.402 | 0.512 (0.05) | 0.001 |
| Efflorescence | 4995329 | nugated | 0.992 | 0.824 | 0.477 | 0.593 (0.05) | 0.002 |

typed: mIoU@0.3 0.473, mIoU_best 0.513, mAP 0.711; gated: mIoU@0.3 0.480, mIoU_best 0.523, mAP 0.712; nugated: mIoU@0.3 0.465, mIoU_best 0.504, mAP 0.714
P-AUPRO (binary map) 0.8369
