## runs/nuisance-v2-s12/val-epoch20 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.986 | 0.391 | 0.260 | 0.303 (0.55) | 0.000 |
| Crack | 165419 | gated | 0.964 | 0.424 | 0.319 | 0.338 (0.10) | 0.000 |
| Crack | 165419 | nugated | 0.986 | 0.405 | 0.308 | 0.308 (0.30) | 0.000 |
| Corrosion | 402682 | typed | 0.983 | 0.785 | 0.451 | 0.555 (0.90) | 0.004 |
| Corrosion | 402682 | gated | 0.972 | 0.742 | 0.449 | 0.529 (0.80) | 0.003 |
| Corrosion | 402682 | nugated | 0.983 | 0.785 | 0.474 | 0.559 (0.75) | 0.003 |
| Spalling | 1593045 | typed | 0.995 | 0.798 | 0.509 | 0.555 (0.80) | 0.016 |
| Spalling | 1593045 | gated | 0.994 | 0.804 | 0.554 | 0.590 (0.60) | 0.012 |
| Spalling | 1593045 | nugated | 0.995 | 0.816 | 0.531 | 0.555 (0.65) | 0.014 |
| Efflorescence | 4995329 | typed | 0.992 | 0.820 | 0.475 | 0.583 (0.05) | 0.002 |
| Efflorescence | 4995329 | gated | 0.987 | 0.791 | 0.385 | 0.509 (0.05) | 0.002 |
| Efflorescence | 4995329 | nugated | 0.992 | 0.820 | 0.407 | 0.537 (0.05) | 0.002 |

typed: mIoU@0.3 0.424, mIoU_best 0.499, mAP 0.699; gated: mIoU@0.3 0.427, mIoU_best 0.491, mAP 0.690; nugated: mIoU@0.3 0.430, mIoU_best 0.490, mAP 0.706
P-AUPRO (binary map) 0.7793
