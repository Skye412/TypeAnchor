## runs/segformer-b2/dacl10k-test per-class (test, 262 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 218895 | typed | 0.588 | 0.113 | 0.072 | 0.082 (0.05) | 0.000 |
| Crack | 218895 | gated | 0.588 | 0.113 | 0.067 | 0.074 (0.05) | 0.000 |
| Corrosion | 2107074 | typed | 0.622 | 0.166 | 0.112 | 0.121 (0.05) | 0.008 |
| Corrosion | 2107074 | gated | 0.622 | 0.167 | 0.110 | 0.119 (0.05) | 0.008 |
| Spalling | 1158079 | typed | 0.597 | 0.051 | 0.065 | 0.068 (0.05) | 0.030 |
| Spalling | 1158079 | gated | 0.597 | 0.051 | 0.064 | 0.066 (0.05) | 0.028 |
| Efflorescence | 1113733 | typed | 0.500 | 0.016 | 0.000 | 0.000 (0.05) | 0.000 |
| Efflorescence | 1113733 | gated | 0.500 | 0.016 | 0.000 | 0.000 (0.05) | 0.000 |

typed: mIoU@0.3 0.062, mIoU_best 0.068, mAP 0.086; gated: mIoU@0.3 0.060, mIoU_best 0.065, mAP 0.086
P-AUPRO (binary map) 0.3658
