## runs/abl-v2-no-residual/val-epoch20 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.973 | 0.343 | 0.244 | 0.257 (0.45) | 0.000 |
| Crack | 165419 | gated | 0.920 | 0.415 | 0.259 | 0.334 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.972 | 0.349 | 0.256 | 0.261 (0.20) | 0.000 |
| Corrosion | 402682 | typed | 0.994 | 0.824 | 0.470 | 0.582 (0.95) | 0.003 |
| Corrosion | 402682 | gated | 0.960 | 0.734 | 0.504 | 0.558 (0.75) | 0.002 |
| Corrosion | 402682 | nugated | 0.994 | 0.822 | 0.499 | 0.590 (0.90) | 0.003 |
| Spalling | 1593045 | typed | 0.996 | 0.845 | 0.581 | 0.584 (0.40) | 0.009 |
| Spalling | 1593045 | gated | 0.995 | 0.875 | 0.626 | 0.629 (0.20) | 0.005 |
| Spalling | 1593045 | nugated | 0.996 | 0.848 | 0.580 | 0.581 (0.25) | 0.007 |
| Efflorescence | 4995329 | typed | 0.968 | 0.730 | 0.414 | 0.480 (0.05) | 0.002 |
| Efflorescence | 4995329 | gated | 0.927 | 0.659 | 0.355 | 0.404 (0.05) | 0.001 |
| Efflorescence | 4995329 | nugated | 0.966 | 0.724 | 0.377 | 0.450 (0.05) | 0.002 |

typed: mIoU@0.3 0.427, mIoU_best 0.476, mAP 0.686; gated: mIoU@0.3 0.436, mIoU_best 0.481, mAP 0.670; nugated: mIoU@0.3 0.428, mIoU_best 0.470, mAP 0.686
P-AUPRO (binary map) 0.7894
