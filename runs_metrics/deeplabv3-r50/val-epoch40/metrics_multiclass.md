## runs/deeplabv3-r50/val-epoch40 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.868 | 0.246 | 0.231 | 0.239 (0.90) | 0.001 |
| Crack | 165419 | gated | 0.868 | 0.246 | 0.236 | 0.239 (0.80) | 0.001 |
| Corrosion | 402682 | typed | 0.963 | 0.787 | 0.559 | 0.666 (0.95) | 0.000 |
| Corrosion | 402682 | gated | 0.962 | 0.779 | 0.588 | 0.667 (0.90) | 0.000 |
| Spalling | 1593045 | typed | 0.994 | 0.777 | 0.566 | 0.593 (0.95) | 0.013 |
| Spalling | 1593045 | gated | 0.994 | 0.780 | 0.573 | 0.604 (0.95) | 0.013 |
| Efflorescence | 4995329 | typed | 0.989 | 0.921 | 0.740 | 0.741 (0.55) | 0.000 |
| Efflorescence | 4995329 | gated | 0.989 | 0.921 | 0.741 | 0.741 (0.30) | 0.000 |

typed: mIoU@0.3 0.524, mIoU_best 0.560, mAP 0.683; gated: mIoU@0.3 0.534, mIoU_best 0.563, mAP 0.682
P-AUPRO (binary map) 0.6215
