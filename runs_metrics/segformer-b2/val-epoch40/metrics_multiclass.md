## runs/segformer-b2/val-epoch40 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.895 | 0.545 | 0.412 | 0.420 (0.85) | 0.001 |
| Crack | 165419 | gated | 0.895 | 0.545 | 0.417 | 0.420 (0.65) | 0.000 |
| Corrosion | 402682 | typed | 0.967 | 0.806 | 0.516 | 0.590 (0.95) | 0.003 |
| Corrosion | 402682 | gated | 0.967 | 0.802 | 0.514 | 0.592 (0.95) | 0.003 |
| Spalling | 1593045 | typed | 0.997 | 0.943 | 0.500 | 0.580 (0.95) | 0.019 |
| Spalling | 1593045 | gated | 0.996 | 0.942 | 0.514 | 0.613 (0.95) | 0.018 |
| Efflorescence | 4995329 | typed | 0.994 | 0.965 | 0.872 | 0.872 (0.35) | 0.001 |
| Efflorescence | 4995329 | gated | 0.994 | 0.965 | 0.868 | 0.872 (0.15) | 0.001 |

typed: mIoU@0.3 0.575, mIoU_best 0.616, mAP 0.815; gated: mIoU@0.3 0.578, mIoU_best 0.624, mAP 0.814
P-AUPRO (binary map) 0.7837
