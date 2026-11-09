## runs/ablation-v2-no-nuisance/dacl10k-test per-class (test, 262 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 218895 | typed | 0.650 | 0.049 | 0.011 | 0.040 (0.05) | 0.000 |
| Crack | 218895 | gated | 0.647 | 0.047 | 0.004 | 0.022 (0.05) | 0.000 |
| Crack | 218895 | nugated | 0.649 | 0.045 | 0.003 | 0.022 (0.05) | 0.000 |
| Corrosion | 2107074 | typed | 0.907 | 0.440 | 0.275 | 0.286 (0.05) | 0.000 |
| Corrosion | 2107074 | gated | 0.885 | 0.430 | 0.248 | 0.288 (0.05) | 0.000 |
| Corrosion | 2107074 | nugated | 0.901 | 0.430 | 0.262 | 0.288 (0.05) | 0.000 |
| Spalling | 1158079 | typed | 0.837 | 0.129 | 0.112 | 0.123 (0.75) | 0.026 |
| Spalling | 1158079 | gated | 0.845 | 0.134 | 0.136 | 0.137 (0.35) | 0.007 |
| Spalling | 1158079 | nugated | 0.838 | 0.124 | 0.119 | 0.124 (0.60) | 0.017 |
| Efflorescence | 1113733 | typed | 0.562 | 0.026 | 0.000 | 0.000 (0.05) | 0.000 |
| Efflorescence | 1113733 | gated | 0.563 | 0.035 | 0.000 | 0.000 (0.05) | 0.000 |
| Efflorescence | 1113733 | nugated | 0.563 | 0.030 | 0.000 | 0.000 (0.05) | 0.000 |

typed: mIoU@0.3 0.100, mIoU_best 0.112, mAP 0.161; gated: mIoU@0.3 0.097, mIoU_best 0.112, mAP 0.161; nugated: mIoU@0.3 0.096, mIoU_best 0.108, mAP 0.157
P-AUPRO (binary map) 0.4010
