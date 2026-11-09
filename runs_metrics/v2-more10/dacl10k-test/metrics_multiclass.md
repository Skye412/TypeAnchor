## runs/v2-more10/dacl10k-test per-class (test, 262 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 218895 | typed | 0.628 | 0.073 | 0.020 | 0.049 (0.05) | 0.000 |
| Crack | 218895 | gated | 0.625 | 0.076 | 0.010 | 0.026 (0.05) | 0.000 |
| Crack | 218895 | nugated | 0.628 | 0.072 | 0.008 | 0.033 (0.05) | 0.000 |
| Corrosion | 2107074 | typed | 0.795 | 0.354 | 0.117 | 0.176 (0.05) | 0.000 |
| Corrosion | 2107074 | gated | 0.795 | 0.360 | 0.115 | 0.175 (0.05) | 0.000 |
| Corrosion | 2107074 | nugated | 0.794 | 0.344 | 0.101 | 0.160 (0.05) | 0.000 |
| Spalling | 1158079 | typed | 0.805 | 0.134 | 0.131 | 0.139 (0.60) | 0.008 |
| Spalling | 1158079 | gated | 0.813 | 0.134 | 0.134 | 0.141 (0.65) | 0.007 |
| Spalling | 1158079 | nugated | 0.806 | 0.137 | 0.138 | 0.139 (0.40) | 0.005 |
| Efflorescence | 1113733 | typed | 0.598 | 0.049 | 0.003 | 0.010 (0.05) | 0.000 |
| Efflorescence | 1113733 | gated | 0.600 | 0.058 | 0.003 | 0.009 (0.05) | 0.000 |
| Efflorescence | 1113733 | nugated | 0.599 | 0.055 | 0.002 | 0.008 (0.05) | 0.000 |

typed: mIoU@0.3 0.068, mIoU_best 0.093, mAP 0.152; gated: mIoU@0.3 0.065, mIoU_best 0.088, mAP 0.157; nugated: mIoU@0.3 0.062, mIoU_best 0.085, mAP 0.152
P-AUPRO (binary map) 0.3542
