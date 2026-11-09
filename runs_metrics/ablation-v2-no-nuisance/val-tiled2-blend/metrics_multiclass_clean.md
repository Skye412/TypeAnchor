## runs/ablation-v2-no-nuisance/val-tiled2-blend per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.969 | 0.426 | 0.295 | 0.299 (0.25) | 0.000 |
| Crack | 165419 | gated | 0.948 | 0.517 | 0.213 | 0.363 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.969 | 0.435 | 0.198 | 0.306 (0.10) | 0.000 |
| Corrosion | 402682 | typed | 0.999 | 0.901 | 0.729 | 0.729 (0.30) | 0.000 |
| Corrosion | 402682 | gated | 0.996 | 0.835 | 0.486 | 0.674 (0.10) | 0.000 |
| Corrosion | 402682 | nugated | 0.999 | 0.875 | 0.605 | 0.705 (0.15) | 0.000 |
| Spalling | 1593045 | typed | 0.999 | 0.957 | 0.758 | 0.833 (0.05) | 0.000 |
| Spalling | 1593045 | gated | 0.998 | 0.968 | 0.552 | 0.827 (0.05) | 0.000 |
| Spalling | 1593045 | nugated | 0.999 | 0.957 | 0.541 | 0.807 (0.05) | 0.000 |
| Efflorescence | 4995329 | typed | 0.993 | 0.862 | 0.514 | 0.648 (0.05) | 0.001 |
| Efflorescence | 4995329 | gated | 0.993 | 0.857 | 0.249 | 0.572 (0.05) | 0.000 |
| Efflorescence | 4995329 | nugated | 0.993 | 0.861 | 0.231 | 0.584 (0.05) | 0.000 |

typed: mIoU@0.3 0.574, mIoU_best 0.627, mAP 0.787; gated: mIoU@0.3 0.375, mIoU_best 0.609, mAP 0.795; nugated: mIoU@0.3 0.394, mIoU_best 0.601, mAP 0.782
P-AUPRO (binary map) 0.8547
