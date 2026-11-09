## runs/abl-v2-no-nu-gate/val-epoch20 per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.978 | 0.383 | 0.266 | 0.267 (0.25) | 0.000 |
| Crack | 165419 | gated | 0.942 | 0.456 | 0.244 | 0.344 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.976 | 0.393 | 0.202 | 0.279 (0.10) | 0.000 |
| Corrosion | 402682 | typed | 0.991 | 0.896 | 0.720 | 0.722 (0.40) | 0.000 |
| Corrosion | 402682 | gated | 0.974 | 0.859 | 0.686 | 0.688 (0.20) | 0.000 |
| Corrosion | 402682 | nugated | 0.991 | 0.883 | 0.712 | 0.713 (0.25) | 0.000 |
| Spalling | 1593045 | typed | 0.998 | 0.945 | 0.712 | 0.786 (0.05) | 0.000 |
| Spalling | 1593045 | gated | 0.997 | 0.963 | 0.689 | 0.796 (0.05) | 0.000 |
| Spalling | 1593045 | nugated | 0.998 | 0.945 | 0.659 | 0.758 (0.05) | 0.000 |
| Efflorescence | 4995329 | typed | 0.993 | 0.853 | 0.582 | 0.646 (0.05) | 0.001 |
| Efflorescence | 4995329 | gated | 0.984 | 0.825 | 0.469 | 0.546 (0.05) | 0.000 |
| Efflorescence | 4995329 | nugated | 0.993 | 0.852 | 0.530 | 0.618 (0.05) | 0.000 |

typed: mIoU@0.3 0.570, mIoU_best 0.605, mAP 0.769; gated: mIoU@0.3 0.522, mIoU_best 0.593, mAP 0.776; nugated: mIoU@0.3 0.526, mIoU_best 0.592, mAP 0.768
P-AUPRO (binary map) 0.8157
