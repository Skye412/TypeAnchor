## runs/ablation-v2-no-nuisance/val-tiled2-blend per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.969 | 0.413 | 0.287 | 0.288 (0.25) | 0.000 |
| Crack | 165419 | gated | 0.948 | 0.502 | 0.212 | 0.352 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.968 | 0.424 | 0.197 | 0.298 (0.10) | 0.000 |
| Corrosion | 402682 | typed | 0.998 | 0.845 | 0.610 | 0.661 (0.45) | 0.001 |
| Corrosion | 402682 | gated | 0.995 | 0.791 | 0.481 | 0.625 (0.20) | 0.000 |
| Corrosion | 402682 | nugated | 0.998 | 0.823 | 0.585 | 0.635 (0.25) | 0.000 |
| Spalling | 1593045 | typed | 0.996 | 0.807 | 0.590 | 0.592 (0.25) | 0.006 |
| Spalling | 1593045 | gated | 0.996 | 0.854 | 0.519 | 0.637 (0.10) | 0.001 |
| Spalling | 1593045 | nugated | 0.996 | 0.819 | 0.499 | 0.588 (0.10) | 0.002 |
| Efflorescence | 4995329 | typed | 0.992 | 0.810 | 0.501 | 0.617 (0.05) | 0.003 |
| Efflorescence | 4995329 | gated | 0.991 | 0.805 | 0.245 | 0.553 (0.05) | 0.001 |
| Efflorescence | 4995329 | nugated | 0.991 | 0.809 | 0.227 | 0.563 (0.05) | 0.001 |

typed: mIoU@0.3 0.497, mIoU_best 0.540, mAP 0.719; gated: mIoU@0.3 0.364, mIoU_best 0.542, mAP 0.738; nugated: mIoU@0.3 0.377, mIoU_best 0.521, mAP 0.718
P-AUPRO (binary map) 0.8132
