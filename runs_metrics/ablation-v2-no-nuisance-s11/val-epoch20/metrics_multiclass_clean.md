## runs/ablation-v2-no-nuisance-s11/val-epoch20 per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.966 | 0.307 | 0.184 | 0.207 (0.05) | 0.000 |
| Crack | 165419 | gated | 0.967 | 0.407 | 0.185 | 0.266 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.966 | 0.323 | 0.124 | 0.214 (0.05) | 0.000 |
| Corrosion | 402682 | typed | 0.990 | 0.859 | 0.668 | 0.671 (0.35) | 0.000 |
| Corrosion | 402682 | gated | 0.990 | 0.854 | 0.664 | 0.665 (0.35) | 0.000 |
| Corrosion | 402682 | nugated | 0.990 | 0.840 | 0.653 | 0.654 (0.35) | 0.000 |
| Spalling | 1593045 | typed | 0.999 | 0.965 | 0.844 | 0.844 (0.35) | 0.001 |
| Spalling | 1593045 | gated | 0.999 | 0.971 | 0.852 | 0.853 (0.25) | 0.001 |
| Spalling | 1593045 | nugated | 0.999 | 0.965 | 0.837 | 0.843 (0.20) | 0.001 |
| Efflorescence | 4995329 | typed | 0.996 | 0.914 | 0.570 | 0.713 (0.05) | 0.000 |
| Efflorescence | 4995329 | gated | 0.996 | 0.916 | 0.554 | 0.704 (0.05) | 0.000 |
| Efflorescence | 4995329 | nugated | 0.995 | 0.914 | 0.482 | 0.655 (0.05) | 0.000 |

typed: mIoU@0.3 0.566, mIoU_best 0.609, mAP 0.761; gated: mIoU@0.3 0.564, mIoU_best 0.622, mAP 0.787; nugated: mIoU@0.3 0.524, mIoU_best 0.591, mAP 0.760
P-AUPRO (binary map) 0.8366
