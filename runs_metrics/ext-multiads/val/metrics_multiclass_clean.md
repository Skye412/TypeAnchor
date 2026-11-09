## runs/ext-multiads/val per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.979 | 0.358 | 0.268 | 0.316 (0.50) | 0.001 |
| Crack | 165419 | gated | 0.964 | 0.347 | 0.311 | 0.311 (0.30) | 0.000 |
| Corrosion | 402682 | typed | 0.999 | 0.921 | 0.704 | 0.751 (0.40) | 0.001 |
| Corrosion | 402682 | gated | 0.999 | 0.912 | 0.739 | 0.739 (0.30) | 0.000 |
| Spalling | 1593045 | typed | 0.988 | 0.850 | 0.633 | 0.664 (0.40) | 0.004 |
| Spalling | 1593045 | gated | 0.997 | 0.896 | 0.636 | 0.682 (0.20) | 0.001 |
| Efflorescence | 4995329 | typed | 0.973 | 0.743 | 0.472 | 0.533 (0.20) | 0.003 |
| Efflorescence | 4995329 | gated | 0.964 | 0.698 | 0.230 | 0.478 (0.10) | 0.001 |

typed: mIoU@0.3 0.519, mIoU_best 0.566, mAP 0.718; gated: mIoU@0.3 0.479, mIoU_best 0.553, mAP 0.713
P-AUPRO (binary map) 0.8182
