## runs/zeroshot-clip/s2ds-test per-class (test, 447 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 107645 | typed | 0.802 | 0.010 | 0.001 | 0.004 (0.95) | 1.000 |
| Crack | 107645 | gated | 0.802 | 0.010 | 0.001 | 0.013 (0.95) | 0.991 |
| Corrosion | 2041564 | typed | 0.840 | 0.258 | 0.029 | 0.196 (0.75) | 0.478 |
| Corrosion | 2041564 | gated | 0.813 | 0.198 | 0.034 | 0.155 (0.65) | 0.364 |
| Spalling | 9401631 | typed | 0.476 | 0.075 | 0.074 | 0.078 (0.05) | 0.836 |
| Spalling | 9401631 | gated | 0.432 | 0.066 | 0.067 | 0.078 (0.05) | 0.691 |
| Efflorescence | 2162061 | typed | 0.669 | 0.037 | 0.042 | 0.042 (0.30) | 0.049 |
| Efflorescence | 2162061 | gated | 0.657 | 0.035 | 0.039 | 0.039 (0.25) | 0.032 |

typed: mIoU@0.3 0.037, mIoU_best 0.080, mAP 0.095; gated: mIoU@0.3 0.035, mIoU_best 0.071, mAP 0.077
P-AUPRO (binary map) 0.2602
