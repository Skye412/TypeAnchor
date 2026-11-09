## runs/v2-detail-joint/dacl10k-test per-class (test, 262 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 218895 | typed | 0.686 | 0.105 | 0.012 | 0.034 (0.05) | 0.000 |
| Crack | 218895 | gated | 0.681 | 0.101 | 0.009 | 0.026 (0.05) | 0.000 |
| Crack | 218895 | nugated | 0.685 | 0.099 | 0.009 | 0.028 (0.05) | 0.000 |
| Corrosion | 2107074 | typed | 0.875 | 0.404 | 0.108 | 0.173 (0.05) | 0.000 |
| Corrosion | 2107074 | gated | 0.869 | 0.406 | 0.108 | 0.173 (0.05) | 0.000 |
| Corrosion | 2107074 | nugated | 0.873 | 0.398 | 0.102 | 0.164 (0.05) | 0.000 |
| Spalling | 1158079 | typed | 0.836 | 0.128 | 0.108 | 0.112 (0.10) | 0.004 |
| Spalling | 1158079 | gated | 0.843 | 0.126 | 0.109 | 0.114 (0.10) | 0.003 |
| Spalling | 1158079 | nugated | 0.840 | 0.128 | 0.106 | 0.113 (0.05) | 0.003 |
| Efflorescence | 1113733 | typed | 0.620 | 0.058 | 0.007 | 0.017 (0.05) | 0.000 |
| Efflorescence | 1113733 | gated | 0.625 | 0.060 | 0.006 | 0.014 (0.05) | 0.000 |
| Efflorescence | 1113733 | nugated | 0.622 | 0.062 | 0.005 | 0.013 (0.05) | 0.000 |

typed: mIoU@0.3 0.059, mIoU_best 0.084, mAP 0.174; gated: mIoU@0.3 0.058, mIoU_best 0.082, mAP 0.173; nugated: mIoU@0.3 0.056, mIoU_best 0.079, mAP 0.172
P-AUPRO (binary map) 0.4299
