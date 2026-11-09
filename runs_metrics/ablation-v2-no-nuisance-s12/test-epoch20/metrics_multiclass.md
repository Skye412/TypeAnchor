## runs/ablation-v2-no-nuisance-s12/test-epoch20 per-class (test, 809 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 366536 | typed | 0.864 | 0.133 | 0.030 | 0.077 (0.05) | 0.000 |
| Crack | 366536 | gated | 0.862 | 0.192 | 0.026 | 0.074 (0.05) | 0.000 |
| Crack | 366536 | nugated | 0.863 | 0.138 | 0.020 | 0.052 (0.05) | 0.000 |
| Corrosion | 2066692 | typed | 0.981 | 0.838 | 0.616 | 0.617 (0.35) | 0.002 |
| Corrosion | 2066692 | gated | 0.982 | 0.841 | 0.634 | 0.634 (0.30) | 0.001 |
| Corrosion | 2066692 | nugated | 0.982 | 0.844 | 0.622 | 0.622 (0.30) | 0.002 |
| Spalling | 10007679 | typed | 0.946 | 0.761 | 0.458 | 0.499 (0.05) | 0.003 |
| Spalling | 10007679 | gated | 0.940 | 0.751 | 0.453 | 0.494 (0.05) | 0.002 |
| Spalling | 10007679 | nugated | 0.945 | 0.758 | 0.441 | 0.479 (0.05) | 0.002 |
| Efflorescence | 9640891 | typed | 0.966 | 0.649 | 0.375 | 0.416 (0.05) | 0.002 |
| Efflorescence | 9640891 | gated | 0.940 | 0.605 | 0.339 | 0.383 (0.05) | 0.002 |
| Efflorescence | 9640891 | nugated | 0.964 | 0.644 | 0.347 | 0.398 (0.05) | 0.002 |

typed: mIoU@0.3 0.369, mIoU_best 0.402, mAP 0.595; gated: mIoU@0.3 0.363, mIoU_best 0.396, mAP 0.597; nugated: mIoU@0.3 0.358, mIoU_best 0.388, mAP 0.596
P-AUPRO (binary map) 0.7732
