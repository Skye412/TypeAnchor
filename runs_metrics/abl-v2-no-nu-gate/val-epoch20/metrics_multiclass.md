## runs/abl-v2-no-nu-gate/val-epoch20 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.978 | 0.355 | 0.251 | 0.251 (0.30) | 0.000 |
| Crack | 165419 | gated | 0.942 | 0.423 | 0.236 | 0.325 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.976 | 0.364 | 0.196 | 0.263 (0.10) | 0.000 |
| Corrosion | 402682 | typed | 0.990 | 0.813 | 0.498 | 0.599 (0.85) | 0.003 |
| Corrosion | 402682 | gated | 0.972 | 0.793 | 0.556 | 0.613 (0.60) | 0.001 |
| Corrosion | 402682 | nugated | 0.989 | 0.808 | 0.529 | 0.603 (0.75) | 0.002 |
| Spalling | 1593045 | typed | 0.995 | 0.791 | 0.509 | 0.511 (0.20) | 0.009 |
| Spalling | 1593045 | gated | 0.995 | 0.832 | 0.544 | 0.563 (0.05) | 0.006 |
| Spalling | 1593045 | nugated | 0.995 | 0.796 | 0.499 | 0.507 (0.10) | 0.007 |
| Efflorescence | 4995329 | typed | 0.992 | 0.833 | 0.570 | 0.624 (0.05) | 0.002 |
| Efflorescence | 4995329 | gated | 0.983 | 0.800 | 0.462 | 0.533 (0.05) | 0.002 |
| Efflorescence | 4995329 | nugated | 0.992 | 0.832 | 0.522 | 0.602 (0.05) | 0.002 |

typed: mIoU@0.3 0.457, mIoU_best 0.496, mAP 0.698; gated: mIoU@0.3 0.450, mIoU_best 0.509, mAP 0.712; nugated: mIoU@0.3 0.437, mIoU_best 0.494, mAP 0.700
P-AUPRO (binary map) 0.7793
