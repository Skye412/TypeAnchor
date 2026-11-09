## runs/ext-multiads/dacl10k-test per-class (test, 262 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 218895 | typed | 0.835 | 0.123 | 0.127 | 0.127 (0.30) | 0.002 |
| Crack | 218895 | gated | 0.817 | 0.114 | 0.093 | 0.112 (0.20) | 0.000 |
| Corrosion | 2107074 | typed | 0.895 | 0.405 | 0.295 | 0.295 (0.30) | 0.007 |
| Corrosion | 2107074 | gated | 0.886 | 0.401 | 0.264 | 0.290 (0.20) | 0.002 |
| Spalling | 1158079 | typed | 0.858 | 0.151 | 0.061 | 0.135 (0.60) | 0.181 |
| Spalling | 1158079 | gated | 0.876 | 0.182 | 0.128 | 0.154 (0.45) | 0.050 |
| Efflorescence | 1113733 | typed | 0.713 | 0.061 | 0.038 | 0.067 (0.15) | 0.001 |
| Efflorescence | 1113733 | gated | 0.762 | 0.073 | 0.018 | 0.072 (0.05) | 0.000 |

typed: mIoU@0.3 0.130, mIoU_best 0.156, mAP 0.185; gated: mIoU@0.3 0.126, mIoU_best 0.157, mAP 0.193
P-AUPRO (binary map) 0.4963
