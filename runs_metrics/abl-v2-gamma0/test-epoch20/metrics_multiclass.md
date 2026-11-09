## runs/abl-v2-gamma0/test-epoch20 per-class (test, 809 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 366536 | typed | 0.847 | 0.052 | 0.022 | 0.036 (0.05) | 0.000 |
| Crack | 366536 | gated | 0.821 | 0.077 | 0.013 | 0.026 (0.05) | 0.000 |
| Crack | 366536 | nugated | 0.842 | 0.040 | 0.016 | 0.030 (0.05) | 0.000 |
| Corrosion | 2066692 | typed | 0.971 | 0.786 | 0.543 | 0.545 (0.15) | 0.002 |
| Corrosion | 2066692 | gated | 0.971 | 0.790 | 0.536 | 0.557 (0.10) | 0.001 |
| Corrosion | 2066692 | nugated | 0.971 | 0.788 | 0.537 | 0.542 (0.10) | 0.001 |
| Spalling | 10007679 | typed | 0.930 | 0.752 | 0.422 | 0.483 (0.05) | 0.002 |
| Spalling | 10007679 | gated | 0.918 | 0.732 | 0.383 | 0.444 (0.05) | 0.001 |
| Spalling | 10007679 | nugated | 0.930 | 0.752 | 0.400 | 0.464 (0.05) | 0.002 |
| Efflorescence | 9640891 | typed | 0.973 | 0.700 | 0.411 | 0.461 (0.05) | 0.002 |
| Efflorescence | 9640891 | gated | 0.958 | 0.688 | 0.338 | 0.414 (0.05) | 0.001 |
| Efflorescence | 9640891 | nugated | 0.972 | 0.697 | 0.384 | 0.438 (0.05) | 0.002 |

typed: mIoU@0.3 0.350, mIoU_best 0.381, mAP 0.573; gated: mIoU@0.3 0.318, mIoU_best 0.360, mAP 0.572; nugated: mIoU@0.3 0.334, mIoU_best 0.368, mAP 0.569
P-AUPRO (binary map) 0.6994
