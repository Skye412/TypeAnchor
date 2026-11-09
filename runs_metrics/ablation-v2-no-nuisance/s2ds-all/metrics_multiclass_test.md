## runs/ablation-v2-no-nuisance/s2ds-all per-class (all, 447 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 107645 | typed | 0.888 | 0.075 | 0.073 | 0.073 (0.30) | 0.000 |
| Crack | 107645 | gated | 0.836 | 0.071 | 0.071 | 0.091 (0.05) | 0.000 |
| Crack | 107645 | nugated | 0.885 | 0.073 | 0.064 | 0.076 (0.05) | 0.000 |
| Corrosion | 2041564 | typed | 0.981 | 0.646 | 0.416 | 0.431 (0.10) | 0.000 |
| Corrosion | 2041564 | gated | 0.972 | 0.596 | 0.359 | 0.396 (0.05) | 0.000 |
| Corrosion | 2041564 | nugated | 0.979 | 0.629 | 0.394 | 0.422 (0.05) | 0.000 |
| Spalling | 9401631 | typed | 0.959 | 0.610 | 0.459 | 0.494 (0.05) | 0.012 |
| Spalling | 9401631 | gated | 0.958 | 0.595 | 0.347 | 0.447 (0.05) | 0.007 |
| Spalling | 9401631 | nugated | 0.958 | 0.590 | 0.428 | 0.480 (0.05) | 0.009 |
| Efflorescence | 2162061 | typed | 0.921 | 0.533 | 0.226 | 0.330 (0.05) | 0.001 |
| Efflorescence | 2162061 | gated | 0.917 | 0.556 | 0.217 | 0.324 (0.05) | 0.000 |
| Efflorescence | 2162061 | nugated | 0.921 | 0.531 | 0.187 | 0.283 (0.05) | 0.001 |

typed: mIoU@0.3 0.294, mIoU_best 0.332, mAP 0.466; gated: mIoU@0.3 0.248, mIoU_best 0.314, mAP 0.454; nugated: mIoU@0.3 0.268, mIoU_best 0.315, mAP 0.455
P-AUPRO (binary map) 0.4154
