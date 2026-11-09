## runs/segformer-b2/s2ds-test per-class (test, 447 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 107645 | typed | 0.611 | 0.090 | 0.108 | 0.108 (0.35) | 0.000 |
| Crack | 107645 | gated | 0.611 | 0.090 | 0.108 | 0.108 (0.10) | 0.000 |
| Corrosion | 2041564 | typed | 0.706 | 0.367 | 0.310 | 0.321 (0.05) | 0.000 |
| Corrosion | 2041564 | gated | 0.706 | 0.365 | 0.308 | 0.320 (0.05) | 0.000 |
| Spalling | 9401631 | typed | 0.795 | 0.429 | 0.392 | 0.403 (0.05) | 0.006 |
| Spalling | 9401631 | gated | 0.795 | 0.428 | 0.383 | 0.395 (0.05) | 0.005 |
| Efflorescence | 2162061 | typed | 0.743 | 0.421 | 0.359 | 0.360 (0.15) | 0.000 |
| Efflorescence | 2162061 | gated | 0.743 | 0.421 | 0.357 | 0.359 (0.05) | 0.000 |

typed: mIoU@0.3 0.292, mIoU_best 0.298, mAP 0.327; gated: mIoU@0.3 0.289, mIoU_best 0.296, mAP 0.326
P-AUPRO (binary map) 0.4573
