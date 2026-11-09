## runs/ablation-v2-no-nuisance/s2ds-test-tgtref-full per-class (test, 447 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 107645 | typed | 0.887 | 0.075 | 0.073 | 0.073 (0.30) | 0.000 |
| Crack | 107645 | gated | 0.839 | 0.072 | 0.072 | 0.091 (0.05) | 0.000 |
| Crack | 107645 | nugated | 0.883 | 0.072 | 0.064 | 0.076 (0.05) | 0.000 |
| Corrosion | 2041564 | typed | 0.981 | 0.646 | 0.418 | 0.431 (0.10) | 0.000 |
| Corrosion | 2041564 | gated | 0.972 | 0.604 | 0.365 | 0.407 (0.05) | 0.000 |
| Corrosion | 2041564 | nugated | 0.979 | 0.629 | 0.396 | 0.423 (0.05) | 0.000 |
| Spalling | 9401631 | typed | 0.959 | 0.611 | 0.461 | 0.495 (0.05) | 0.012 |
| Spalling | 9401631 | gated | 0.959 | 0.601 | 0.354 | 0.455 (0.05) | 0.007 |
| Spalling | 9401631 | nugated | 0.958 | 0.591 | 0.430 | 0.482 (0.05) | 0.009 |
| Efflorescence | 2162061 | typed | 0.921 | 0.533 | 0.227 | 0.331 (0.05) | 0.001 |
| Efflorescence | 2162061 | gated | 0.917 | 0.556 | 0.217 | 0.324 (0.05) | 0.000 |
| Efflorescence | 2162061 | nugated | 0.921 | 0.531 | 0.188 | 0.284 (0.05) | 0.001 |

typed: mIoU@0.3 0.295, mIoU_best 0.332, mAP 0.466; gated: mIoU@0.3 0.252, mIoU_best 0.319, mAP 0.458; nugated: mIoU@0.3 0.269, mIoU_best 0.316, mAP 0.456
P-AUPRO (binary map) 0.3694
