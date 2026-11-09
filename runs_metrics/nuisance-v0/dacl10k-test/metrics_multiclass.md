## runs/nuisance-v0/dacl10k-test per-class (test, 262 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 218895 | typed | 0.696 | 0.020 | 0.013 | 0.043 (0.10) | 0.000 |
| Crack | 218895 | gated | 0.622 | 0.009 | 0.000 | 0.007 (0.05) | 0.000 |
| Corrosion | 2107074 | typed | 0.872 | 0.309 | 0.218 | 0.262 (0.10) | 0.000 |
| Corrosion | 2107074 | gated | 0.764 | 0.344 | 0.167 | 0.262 (0.05) | 0.000 |
| Spalling | 1158079 | typed | 0.831 | 0.124 | 0.098 | 0.118 (0.65) | 0.051 |
| Spalling | 1158079 | gated | 0.830 | 0.155 | 0.140 | 0.140 (0.30) | 0.007 |
| Efflorescence | 1113733 | typed | 0.682 | 0.055 | 0.012 | 0.037 (0.10) | 0.000 |
| Efflorescence | 1113733 | gated | 0.715 | 0.093 | 0.004 | 0.036 (0.05) | 0.000 |

typed: mIoU@0.3 0.085, mIoU_best 0.115, mAP 0.127; gated: mIoU@0.3 0.078, mIoU_best 0.111, mAP 0.150
P-AUPRO (binary map) 0.3125
