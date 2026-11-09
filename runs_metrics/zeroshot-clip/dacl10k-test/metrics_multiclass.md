## runs/zeroshot-clip/dacl10k-test per-class (test, 262 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 218895 | typed | 0.610 | 0.005 | 0.003 | 0.005 (0.95) | 0.999 |
| Crack | 218895 | gated | 0.611 | 0.005 | 0.003 | 0.005 (0.90) | 0.968 |
| Corrosion | 2107074 | typed | 0.791 | 0.211 | 0.056 | 0.170 (0.70) | 0.348 |
| Corrosion | 2107074 | gated | 0.765 | 0.176 | 0.066 | 0.143 (0.55) | 0.242 |
| Spalling | 1158079 | typed | 0.736 | 0.062 | 0.020 | 0.069 (0.75) | 0.721 |
| Spalling | 1158079 | gated | 0.678 | 0.043 | 0.022 | 0.051 (0.65) | 0.545 |
| Efflorescence | 1113733 | typed | 0.602 | 0.027 | 0.031 | 0.031 (0.35) | 0.077 |
| Efflorescence | 1113733 | gated | 0.583 | 0.025 | 0.030 | 0.030 (0.30) | 0.048 |

typed: mIoU@0.3 0.028, mIoU_best 0.069, mAP 0.076; gated: mIoU@0.3 0.030, mIoU_best 0.057, mAP 0.062
P-AUPRO (binary map) 0.1115
