## runs/ablation-v2-no-nuisance-s11/val-epoch20 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.966 | 0.301 | 0.184 | 0.204 (0.05) | 0.000 |
| Crack | 165419 | gated | 0.967 | 0.395 | 0.185 | 0.263 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.966 | 0.316 | 0.124 | 0.213 (0.05) | 0.000 |
| Corrosion | 402682 | typed | 0.988 | 0.804 | 0.525 | 0.616 (0.70) | 0.002 |
| Corrosion | 402682 | gated | 0.988 | 0.806 | 0.551 | 0.624 (0.65) | 0.001 |
| Corrosion | 402682 | nugated | 0.987 | 0.790 | 0.546 | 0.607 (0.60) | 0.001 |
| Spalling | 1593045 | typed | 0.995 | 0.806 | 0.515 | 0.569 (0.80) | 0.016 |
| Spalling | 1593045 | gated | 0.996 | 0.878 | 0.568 | 0.647 (0.80) | 0.012 |
| Spalling | 1593045 | nugated | 0.995 | 0.820 | 0.543 | 0.574 (0.65) | 0.013 |
| Efflorescence | 4995329 | typed | 0.995 | 0.890 | 0.560 | 0.693 (0.05) | 0.001 |
| Efflorescence | 4995329 | gated | 0.995 | 0.892 | 0.545 | 0.685 (0.05) | 0.001 |
| Efflorescence | 4995329 | nugated | 0.994 | 0.889 | 0.476 | 0.641 (0.05) | 0.001 |

typed: mIoU@0.3 0.446, mIoU_best 0.520, mAP 0.700; gated: mIoU@0.3 0.462, mIoU_best 0.555, mAP 0.743; nugated: mIoU@0.3 0.422, mIoU_best 0.509, mAP 0.704
P-AUPRO (binary map) 0.7738
