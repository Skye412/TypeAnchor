## runs/nuisance-v0/test-epoch20 per-class (test, 809 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 366536 | typed | 0.921 | 0.019 | 0.016 | 0.035 (0.10) | 0.000 |
| Crack | 366536 | gated | 0.760 | 0.097 | 0.015 | 0.039 (0.05) | 0.000 |
| Corrosion | 2066692 | typed | 0.990 | 0.590 | 0.306 | 0.547 (0.10) | 0.001 |
| Corrosion | 2066692 | gated | 0.981 | 0.758 | 0.266 | 0.577 (0.05) | 0.000 |
| Spalling | 10007679 | typed | 0.955 | 0.710 | 0.490 | 0.551 (0.10) | 0.003 |
| Spalling | 10007679 | gated | 0.890 | 0.633 | 0.380 | 0.471 (0.05) | 0.001 |
| Efflorescence | 9640891 | typed | 0.960 | 0.625 | 0.402 | 0.402 (0.30) | 0.007 |
| Efflorescence | 9640891 | gated | 0.882 | 0.539 | 0.332 | 0.362 (0.10) | 0.002 |

typed: mIoU@0.3 0.304, mIoU_best 0.384, mAP 0.486; gated: mIoU@0.3 0.248, mIoU_best 0.362, mAP 0.507
P-AUPRO (binary map) 0.6563
