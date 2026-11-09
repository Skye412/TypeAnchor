## runs/deeplabv3-r50/dacl10k-test per-class (test, 262 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 218895 | typed | 0.601 | 0.076 | 0.059 | 0.071 (0.05) | 0.000 |
| Crack | 218895 | gated | 0.601 | 0.072 | 0.053 | 0.062 (0.05) | 0.000 |
| Corrosion | 2107074 | typed | 0.664 | 0.163 | 0.117 | 0.128 (0.05) | 0.000 |
| Corrosion | 2107074 | gated | 0.664 | 0.163 | 0.111 | 0.121 (0.05) | 0.000 |
| Spalling | 1158079 | typed | 0.568 | 0.064 | 0.061 | 0.062 (0.05) | 0.000 |
| Spalling | 1158079 | gated | 0.568 | 0.064 | 0.061 | 0.062 (0.15) | 0.000 |
| Efflorescence | 1113733 | typed | 0.557 | 0.035 | 0.000 | 0.000 (0.05) | 0.000 |
| Efflorescence | 1113733 | gated | 0.557 | 0.036 | 0.000 | 0.000 (0.05) | 0.000 |

typed: mIoU@0.3 0.059, mIoU_best 0.065, mAP 0.084; gated: mIoU@0.3 0.056, mIoU_best 0.061, mAP 0.084
P-AUPRO (binary map) 0.2472
