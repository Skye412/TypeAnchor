## runs/v2-detail/dacl10k-test per-class (test, 262 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 218895 | typed | 0.592 | 0.054 | 0.018 | 0.033 (0.05) | 0.000 |
| Crack | 218895 | gated | 0.592 | 0.051 | 0.009 | 0.020 (0.05) | 0.000 |
| Crack | 218895 | nugated | 0.592 | 0.052 | 0.007 | 0.022 (0.05) | 0.000 |
| Corrosion | 2107074 | typed | 0.801 | 0.374 | 0.193 | 0.235 (0.05) | 0.000 |
| Corrosion | 2107074 | gated | 0.801 | 0.392 | 0.177 | 0.225 (0.05) | 0.000 |
| Corrosion | 2107074 | nugated | 0.801 | 0.378 | 0.188 | 0.231 (0.05) | 0.000 |
| Spalling | 1158079 | typed | 0.816 | 0.139 | 0.133 | 0.142 (0.70) | 0.009 |
| Spalling | 1158079 | gated | 0.821 | 0.146 | 0.150 | 0.151 (0.35) | 0.004 |
| Spalling | 1158079 | nugated | 0.817 | 0.130 | 0.135 | 0.137 (0.50) | 0.007 |
| Efflorescence | 1113733 | typed | 0.536 | 0.022 | 0.000 | 0.000 (0.05) | 0.000 |
| Efflorescence | 1113733 | gated | 0.536 | 0.027 | 0.000 | 0.000 (0.05) | 0.000 |
| Efflorescence | 1113733 | nugated | 0.536 | 0.024 | 0.000 | 0.000 (0.05) | 0.000 |

typed: mIoU@0.3 0.086, mIoU_best 0.102, mAP 0.147; gated: mIoU@0.3 0.084, mIoU_best 0.099, mAP 0.154; nugated: mIoU@0.3 0.083, mIoU_best 0.097, mAP 0.146
P-AUPRO (binary map) 0.3991
