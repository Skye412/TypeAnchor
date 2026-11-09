## runs/segformer-b2/val-epoch40 per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.895 | 0.578 | 0.434 | 0.440 (0.75) | 0.000 |
| Crack | 165419 | gated | 0.895 | 0.578 | 0.439 | 0.440 (0.55) | 0.000 |
| Corrosion | 402682 | typed | 0.968 | 0.883 | 0.770 | 0.770 (0.50) | 0.000 |
| Corrosion | 402682 | gated | 0.968 | 0.874 | 0.767 | 0.768 (0.45) | 0.000 |
| Spalling | 1593045 | typed | 0.998 | 0.988 | 0.927 | 0.930 (0.80) | 0.000 |
| Spalling | 1593045 | gated | 0.998 | 0.988 | 0.929 | 0.930 (0.65) | 0.000 |
| Efflorescence | 4995329 | typed | 0.994 | 0.965 | 0.872 | 0.872 (0.35) | 0.001 |
| Efflorescence | 4995329 | gated | 0.994 | 0.965 | 0.868 | 0.872 (0.15) | 0.001 |

typed: mIoU@0.3 0.751, mIoU_best 0.753, mAP 0.854; gated: mIoU@0.3 0.751, mIoU_best 0.752, mAP 0.851
P-AUPRO (binary map) 0.8190
