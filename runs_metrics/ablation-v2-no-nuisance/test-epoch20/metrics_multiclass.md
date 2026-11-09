## runs/ablation-v2-no-nuisance/test-epoch20 per-class (test, 809 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 366536 | typed | 0.778 | 0.083 | 0.024 | 0.056 (0.05) | 0.000 |
| Crack | 366536 | gated | 0.754 | 0.107 | 0.022 | 0.055 (0.05) | 0.000 |
| Crack | 366536 | nugated | 0.776 | 0.074 | 0.018 | 0.038 (0.05) | 0.000 |
| Corrosion | 2066692 | typed | 0.973 | 0.802 | 0.558 | 0.558 (0.25) | 0.002 |
| Corrosion | 2066692 | gated | 0.973 | 0.804 | 0.561 | 0.577 (0.10) | 0.001 |
| Corrosion | 2066692 | nugated | 0.973 | 0.798 | 0.552 | 0.556 (0.20) | 0.001 |
| Spalling | 10007679 | typed | 0.915 | 0.750 | 0.454 | 0.529 (0.05) | 0.002 |
| Spalling | 10007679 | gated | 0.906 | 0.734 | 0.430 | 0.499 (0.05) | 0.001 |
| Spalling | 10007679 | nugated | 0.914 | 0.750 | 0.428 | 0.501 (0.05) | 0.001 |
| Efflorescence | 9640891 | typed | 0.978 | 0.714 | 0.446 | 0.484 (0.05) | 0.003 |
| Efflorescence | 9640891 | gated | 0.969 | 0.693 | 0.402 | 0.453 (0.05) | 0.002 |
| Efflorescence | 9640891 | nugated | 0.977 | 0.712 | 0.412 | 0.471 (0.05) | 0.003 |

typed: mIoU@0.3 0.371, mIoU_best 0.407, mAP 0.587; gated: mIoU@0.3 0.354, mIoU_best 0.396, mAP 0.584; nugated: mIoU@0.3 0.352, mIoU_best 0.392, mAP 0.584
P-AUPRO (binary map) 0.7013
