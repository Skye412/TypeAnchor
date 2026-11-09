## runs/ablation-v2-no-nuisance/val-tiled2 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.944 | 0.423 | 0.205 | 0.283 (0.05) | 0.000 |
| Crack | 165419 | gated | 0.924 | 0.524 | 0.127 | 0.270 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.943 | 0.432 | 0.115 | 0.262 (0.05) | 0.000 |
| Corrosion | 402682 | typed | 0.992 | 0.764 | 0.445 | 0.529 (0.05) | 0.000 |
| Corrosion | 402682 | gated | 0.986 | 0.685 | 0.318 | 0.419 (0.05) | 0.000 |
| Corrosion | 402682 | nugated | 0.991 | 0.747 | 0.366 | 0.494 (0.05) | 0.000 |
| Spalling | 1593045 | typed | 0.965 | 0.676 | 0.375 | 0.428 (0.05) | 0.001 |
| Spalling | 1593045 | gated | 0.961 | 0.705 | 0.332 | 0.427 (0.05) | 0.001 |
| Spalling | 1593045 | nugated | 0.965 | 0.683 | 0.328 | 0.418 (0.05) | 0.001 |
| Efflorescence | 4995329 | typed | 0.942 | 0.598 | 0.155 | 0.276 (0.05) | 0.002 |
| Efflorescence | 4995329 | gated | 0.939 | 0.601 | 0.104 | 0.209 (0.05) | 0.001 |
| Efflorescence | 4995329 | nugated | 0.941 | 0.594 | 0.102 | 0.210 (0.05) | 0.001 |

typed: mIoU@0.3 0.295, mIoU_best 0.379, mAP 0.615; gated: mIoU@0.3 0.220, mIoU_best 0.331, mAP 0.629; nugated: mIoU@0.3 0.228, mIoU_best 0.346, mAP 0.614
P-AUPRO (binary map) 0.8027
