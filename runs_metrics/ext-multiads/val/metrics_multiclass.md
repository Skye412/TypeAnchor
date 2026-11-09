## runs/ext-multiads/val per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.978 | 0.337 | 0.250 | 0.300 (0.50) | 0.001 |
| Crack | 165419 | gated | 0.962 | 0.326 | 0.293 | 0.293 (0.35) | 0.000 |
| Corrosion | 402682 | typed | 0.998 | 0.843 | 0.421 | 0.615 (0.50) | 0.005 |
| Corrosion | 402682 | gated | 0.998 | 0.824 | 0.528 | 0.584 (0.45) | 0.003 |
| Spalling | 1593045 | typed | 0.982 | 0.694 | 0.377 | 0.492 (0.45) | 0.022 |
| Spalling | 1593045 | gated | 0.991 | 0.717 | 0.487 | 0.487 (0.30) | 0.007 |
| Efflorescence | 4995329 | typed | 0.970 | 0.712 | 0.459 | 0.495 (0.20) | 0.005 |
| Efflorescence | 4995329 | gated | 0.957 | 0.649 | 0.229 | 0.441 (0.10) | 0.001 |

typed: mIoU@0.3 0.377, mIoU_best 0.476, mAP 0.646; gated: mIoU@0.3 0.384, mIoU_best 0.451, mAP 0.629
P-AUPRO (binary map) 0.7808
