## runs/nuisance-v0/s2ds-test-tgtref-4shot per-class (test, 447 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 107645 | typed | 0.782 | 0.008 | 0.016 | 0.018 (0.10) | 0.000 |
| Crack | 107645 | gated | 0.413 | 0.005 | 0.005 | 0.012 (0.05) | 0.000 |
| Corrosion | 2041564 | typed | 0.976 | 0.522 | 0.351 | 0.438 (0.15) | 0.000 |
| Corrosion | 2041564 | gated | 0.924 | 0.574 | 0.291 | 0.447 (0.10) | 0.000 |
| Spalling | 9401631 | typed | 0.971 | 0.725 | 0.561 | 0.563 (0.35) | 0.018 |
| Spalling | 9401631 | gated | 0.960 | 0.696 | 0.446 | 0.535 (0.05) | 0.004 |
| Efflorescence | 2162061 | typed | 0.965 | 0.594 | 0.385 | 0.428 (0.15) | 0.002 |
| Efflorescence | 2162061 | gated | 0.928 | 0.568 | 0.304 | 0.411 (0.10) | 0.000 |

typed: mIoU@0.3 0.328, mIoU_best 0.362, mAP 0.462; gated: mIoU@0.3 0.261, mIoU_best 0.351, mAP 0.461
P-AUPRO (binary map) 0.3776
