## runs/nuisance-v1-fix/val-epoch20 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.981 | 0.087 | 0.085 | 0.085 (0.20) | 0.000 |
| Crack | 165419 | gated | 0.944 | 0.335 | 0.214 | 0.326 (0.10) | 0.000 |
| Corrosion | 402682 | typed | 0.994 | 0.577 | 0.370 | 0.440 (0.20) | 0.001 |
| Corrosion | 402682 | gated | 0.957 | 0.734 | 0.304 | 0.574 (0.15) | 0.000 |
| Spalling | 1593045 | typed | 0.996 | 0.831 | 0.589 | 0.620 (0.40) | 0.010 |
| Spalling | 1593045 | gated | 0.992 | 0.867 | 0.674 | 0.678 (0.25) | 0.003 |
| Efflorescence | 4995329 | typed | 0.988 | 0.778 | 0.575 | 0.583 (0.20) | 0.008 |
| Efflorescence | 4995329 | gated | 0.972 | 0.704 | 0.460 | 0.503 (0.10) | 0.003 |

typed: mIoU@0.3 0.405, mIoU_best 0.432, mAP 0.569; gated: mIoU@0.3 0.413, mIoU_best 0.520, mAP 0.660
P-AUPRO (binary map) 0.7615
