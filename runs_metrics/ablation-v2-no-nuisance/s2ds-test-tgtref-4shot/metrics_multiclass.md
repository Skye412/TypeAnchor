## runs/ablation-v2-no-nuisance/s2ds-test-tgtref-4shot per-class (test, 447 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 107645 | typed | 0.887 | 0.076 | 0.073 | 0.073 (0.30) | 0.000 |
| Crack | 107645 | gated | 0.849 | 0.072 | 0.071 | 0.090 (0.05) | 0.000 |
| Crack | 107645 | nugated | 0.884 | 0.073 | 0.064 | 0.076 (0.05) | 0.000 |
| Corrosion | 2041564 | typed | 0.981 | 0.647 | 0.418 | 0.432 (0.10) | 0.000 |
| Corrosion | 2041564 | gated | 0.972 | 0.608 | 0.369 | 0.410 (0.05) | 0.000 |
| Corrosion | 2041564 | nugated | 0.979 | 0.630 | 0.396 | 0.423 (0.05) | 0.000 |
| Spalling | 9401631 | typed | 0.959 | 0.612 | 0.462 | 0.496 (0.05) | 0.012 |
| Spalling | 9401631 | gated | 0.960 | 0.600 | 0.358 | 0.461 (0.05) | 0.007 |
| Spalling | 9401631 | nugated | 0.958 | 0.591 | 0.430 | 0.483 (0.05) | 0.009 |
| Efflorescence | 2162061 | typed | 0.921 | 0.534 | 0.227 | 0.332 (0.05) | 0.001 |
| Efflorescence | 2162061 | gated | 0.916 | 0.553 | 0.216 | 0.323 (0.05) | 0.001 |
| Efflorescence | 2162061 | nugated | 0.920 | 0.532 | 0.188 | 0.285 (0.05) | 0.001 |

typed: mIoU@0.3 0.295, mIoU_best 0.333, mAP 0.467; gated: mIoU@0.3 0.254, mIoU_best 0.321, mAP 0.458; nugated: mIoU@0.3 0.269, mIoU_best 0.317, mAP 0.457
P-AUPRO (binary map) 0.4145
