## runs/deeplabv3-r50/val-epoch40 per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.869 | 0.274 | 0.246 | 0.253 (0.85) | 0.001 |
| Crack | 165419 | gated | 0.869 | 0.274 | 0.250 | 0.253 (0.70) | 0.001 |
| Corrosion | 402682 | typed | 0.964 | 0.814 | 0.600 | 0.668 (0.90) | 0.000 |
| Corrosion | 402682 | gated | 0.964 | 0.808 | 0.633 | 0.672 (0.85) | 0.000 |
| Spalling | 1593045 | typed | 0.996 | 0.983 | 0.912 | 0.917 (0.05) | 0.000 |
| Spalling | 1593045 | gated | 0.996 | 0.983 | 0.907 | 0.913 (0.05) | 0.000 |
| Efflorescence | 4995329 | typed | 0.989 | 0.921 | 0.740 | 0.741 (0.55) | 0.000 |
| Efflorescence | 4995329 | gated | 0.989 | 0.921 | 0.741 | 0.741 (0.30) | 0.000 |

typed: mIoU@0.3 0.624, mIoU_best 0.645, mAP 0.748; gated: mIoU@0.3 0.633, mIoU_best 0.645, mAP 0.746
P-AUPRO (binary map) 0.6512
