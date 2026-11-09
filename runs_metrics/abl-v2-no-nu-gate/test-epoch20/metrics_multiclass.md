## runs/abl-v2-no-nu-gate/test-epoch20 per-class (test, 809 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 366536 | typed | 0.835 | 0.102 | 0.023 | 0.048 (0.05) | 0.000 |
| Crack | 366536 | gated | 0.819 | 0.155 | 0.019 | 0.040 (0.05) | 0.000 |
| Crack | 366536 | nugated | 0.834 | 0.097 | 0.016 | 0.033 (0.05) | 0.000 |
| Corrosion | 2066692 | typed | 0.971 | 0.821 | 0.596 | 0.597 (0.25) | 0.002 |
| Corrosion | 2066692 | gated | 0.970 | 0.820 | 0.583 | 0.601 (0.10) | 0.001 |
| Corrosion | 2066692 | nugated | 0.970 | 0.820 | 0.587 | 0.592 (0.20) | 0.002 |
| Spalling | 10007679 | typed | 0.925 | 0.734 | 0.397 | 0.479 (0.05) | 0.003 |
| Spalling | 10007679 | gated | 0.908 | 0.716 | 0.378 | 0.461 (0.05) | 0.002 |
| Spalling | 10007679 | nugated | 0.925 | 0.735 | 0.371 | 0.446 (0.05) | 0.002 |
| Efflorescence | 9640891 | typed | 0.980 | 0.731 | 0.485 | 0.506 (0.10) | 0.002 |
| Efflorescence | 9640891 | gated | 0.944 | 0.659 | 0.394 | 0.435 (0.05) | 0.001 |
| Efflorescence | 9640891 | nugated | 0.979 | 0.729 | 0.445 | 0.502 (0.05) | 0.002 |

typed: mIoU@0.3 0.375, mIoU_best 0.408, mAP 0.597; gated: mIoU@0.3 0.343, mIoU_best 0.384, mAP 0.587; nugated: mIoU@0.3 0.355, mIoU_best 0.393, mAP 0.595
P-AUPRO (binary map) 0.7175
