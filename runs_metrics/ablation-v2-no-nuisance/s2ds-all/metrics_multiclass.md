## runs/ablation-v2-no-nuisance/s2ds-all per-class (all, 2226 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 813391 | typed | 0.920 | 0.097 | 0.071 | 0.088 (0.05) | 0.000 |
| Crack | 813391 | gated | 0.866 | 0.086 | 0.053 | 0.086 (0.05) | 0.000 |
| Crack | 813391 | nugated | 0.917 | 0.095 | 0.052 | 0.086 (0.05) | 0.000 |
| Corrosion | 10470675 | typed | 0.978 | 0.631 | 0.421 | 0.422 (0.20) | 0.000 |
| Corrosion | 10470675 | gated | 0.965 | 0.585 | 0.385 | 0.400 (0.05) | 0.000 |
| Corrosion | 10470675 | nugated | 0.976 | 0.615 | 0.411 | 0.417 (0.15) | 0.000 |
| Spalling | 47712740 | typed | 0.965 | 0.705 | 0.518 | 0.545 (0.05) | 0.006 |
| Spalling | 47712740 | gated | 0.963 | 0.664 | 0.422 | 0.512 (0.05) | 0.003 |
| Spalling | 47712740 | nugated | 0.964 | 0.681 | 0.490 | 0.536 (0.05) | 0.005 |
| Efflorescence | 6839581 | typed | 0.921 | 0.431 | 0.202 | 0.279 (0.05) | 0.001 |
| Efflorescence | 6839581 | gated | 0.918 | 0.454 | 0.191 | 0.276 (0.05) | 0.000 |
| Efflorescence | 6839581 | nugated | 0.921 | 0.434 | 0.166 | 0.249 (0.05) | 0.000 |

typed: mIoU@0.3 0.303, mIoU_best 0.334, mAP 0.466; gated: mIoU@0.3 0.263, mIoU_best 0.318, mAP 0.447; nugated: mIoU@0.3 0.280, mIoU_best 0.322, mAP 0.456
