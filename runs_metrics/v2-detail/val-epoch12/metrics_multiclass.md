## runs/v2-detail/val-epoch12 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.922 | 0.424 | 0.317 | 0.328 (0.60) | 0.000 |
| Crack | 165419 | gated | 0.922 | 0.441 | 0.317 | 0.345 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.922 | 0.409 | 0.319 | 0.321 (0.25) | 0.000 |
| Corrosion | 402682 | typed | 0.980 | 0.741 | 0.470 | 0.538 (0.95) | 0.003 |
| Corrosion | 402682 | gated | 0.977 | 0.805 | 0.540 | 0.643 (0.70) | 0.002 |
| Corrosion | 402682 | nugated | 0.981 | 0.820 | 0.508 | 0.621 (0.85) | 0.003 |
| Spalling | 1593045 | typed | 0.993 | 0.815 | 0.579 | 0.595 (0.75) | 0.011 |
| Spalling | 1593045 | gated | 0.994 | 0.888 | 0.642 | 0.677 (0.55) | 0.007 |
| Spalling | 1593045 | nugated | 0.994 | 0.850 | 0.590 | 0.594 (0.40) | 0.010 |
| Efflorescence | 4995329 | typed | 0.993 | 0.848 | 0.611 | 0.673 (0.05) | 0.003 |
| Efflorescence | 4995329 | gated | 0.993 | 0.851 | 0.530 | 0.630 (0.05) | 0.002 |
| Efflorescence | 4995329 | nugated | 0.993 | 0.854 | 0.537 | 0.643 (0.05) | 0.002 |

typed: mIoU@0.3 0.494, mIoU_best 0.534, mAP 0.707; gated: mIoU@0.3 0.507, mIoU_best 0.574, mAP 0.746; nugated: mIoU@0.3 0.489, mIoU_best 0.545, mAP 0.733
P-AUPRO (binary map) 0.7624
