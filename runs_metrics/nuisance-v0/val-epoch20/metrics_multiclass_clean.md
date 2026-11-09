## runs/nuisance-v0/val-epoch20 per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.952 | 0.069 | 0.083 | 0.084 (0.35) | 0.000 |
| Crack | 165419 | gated | 0.812 | 0.186 | 0.155 | 0.199 (0.10) | 0.000 |
| Corrosion | 402682 | typed | 0.990 | 0.656 | 0.412 | 0.625 (0.15) | 0.000 |
| Corrosion | 402682 | gated | 0.939 | 0.778 | 0.357 | 0.674 (0.10) | 0.000 |
| Spalling | 1593045 | typed | 0.998 | 0.929 | 0.776 | 0.781 (0.25) | 0.000 |
| Spalling | 1593045 | gated | 0.993 | 0.940 | 0.733 | 0.819 (0.10) | 0.000 |
| Efflorescence | 4995329 | typed | 0.988 | 0.817 | 0.605 | 0.636 (0.10) | 0.001 |
| Efflorescence | 4995329 | gated | 0.979 | 0.774 | 0.431 | 0.536 (0.05) | 0.000 |

typed: mIoU@0.3 0.469, mIoU_best 0.531, mAP 0.618; gated: mIoU@0.3 0.419, mIoU_best 0.557, mAP 0.669
P-AUPRO (binary map) 0.7480
