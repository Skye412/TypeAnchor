## runs/abl-v2-gamma0/val-epoch20 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.965 | 0.082 | 0.071 | 0.078 (0.10) | 0.000 |
| Crack | 165419 | gated | 0.946 | 0.341 | 0.087 | 0.202 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.964 | 0.082 | 0.058 | 0.079 (0.05) | 0.000 |
| Corrosion | 402682 | typed | 0.980 | 0.771 | 0.518 | 0.620 (0.90) | 0.002 |
| Corrosion | 402682 | gated | 0.964 | 0.811 | 0.598 | 0.641 (0.55) | 0.001 |
| Corrosion | 402682 | nugated | 0.980 | 0.810 | 0.540 | 0.628 (0.80) | 0.001 |
| Spalling | 1593045 | typed | 0.996 | 0.841 | 0.623 | 0.635 (0.55) | 0.008 |
| Spalling | 1593045 | gated | 0.996 | 0.866 | 0.654 | 0.654 (0.25) | 0.005 |
| Spalling | 1593045 | nugated | 0.996 | 0.853 | 0.633 | 0.634 (0.35) | 0.007 |
| Efflorescence | 4995329 | typed | 0.993 | 0.852 | 0.540 | 0.627 (0.05) | 0.002 |
| Efflorescence | 4995329 | gated | 0.990 | 0.830 | 0.401 | 0.531 (0.05) | 0.001 |
| Efflorescence | 4995329 | nugated | 0.993 | 0.850 | 0.490 | 0.592 (0.05) | 0.002 |

typed: mIoU@0.3 0.438, mIoU_best 0.490, mAP 0.637; gated: mIoU@0.3 0.435, mIoU_best 0.507, mAP 0.712; nugated: mIoU@0.3 0.430, mIoU_best 0.483, mAP 0.649
P-AUPRO (binary map) 0.7522
