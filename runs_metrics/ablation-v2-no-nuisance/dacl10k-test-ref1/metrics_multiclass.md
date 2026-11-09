## runs/ablation-v2-no-nuisance/dacl10k-test-ref1 per-class (test, 262 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 218895 | typed | 0.651 | 0.050 | 0.011 | 0.039 (0.05) | 0.000 |
| Crack | 218895 | gated | 0.650 | 0.048 | 0.005 | 0.023 (0.05) | 0.000 |
| Crack | 218895 | nugated | 0.650 | 0.046 | 0.003 | 0.022 (0.05) | 0.000 |
| Corrosion | 2107074 | typed | 0.908 | 0.441 | 0.274 | 0.288 (0.05) | 0.000 |
| Corrosion | 2107074 | gated | 0.883 | 0.437 | 0.254 | 0.294 (0.05) | 0.000 |
| Corrosion | 2107074 | nugated | 0.902 | 0.431 | 0.261 | 0.289 (0.05) | 0.000 |
| Spalling | 1158079 | typed | 0.837 | 0.129 | 0.113 | 0.124 (0.75) | 0.026 |
| Spalling | 1158079 | gated | 0.848 | 0.132 | 0.135 | 0.138 (0.45) | 0.009 |
| Spalling | 1158079 | nugated | 0.838 | 0.125 | 0.119 | 0.124 (0.60) | 0.017 |
| Efflorescence | 1113733 | typed | 0.562 | 0.026 | 0.000 | 0.000 (0.05) | 0.000 |
| Efflorescence | 1113733 | gated | 0.562 | 0.034 | 0.000 | 0.000 (0.05) | 0.000 |
| Efflorescence | 1113733 | nugated | 0.563 | 0.030 | 0.000 | 0.000 (0.05) | 0.000 |

typed: mIoU@0.3 0.099, mIoU_best 0.113, mAP 0.162; gated: mIoU@0.3 0.098, mIoU_best 0.114, mAP 0.163; nugated: mIoU@0.3 0.096, mIoU_best 0.109, mAP 0.158
P-AUPRO (binary map) 0.4097
