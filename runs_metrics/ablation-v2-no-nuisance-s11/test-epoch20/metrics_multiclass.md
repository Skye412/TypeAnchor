## runs/ablation-v2-no-nuisance-s11/test-epoch20 per-class (test, 809 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 366536 | typed | 0.777 | 0.093 | 0.014 | 0.027 (0.05) | 0.000 |
| Crack | 366536 | gated | 0.777 | 0.127 | 0.013 | 0.028 (0.05) | 0.000 |
| Crack | 366536 | nugated | 0.776 | 0.093 | 0.009 | 0.019 (0.05) | 0.000 |
| Corrosion | 2066692 | typed | 0.979 | 0.783 | 0.532 | 0.535 (0.20) | 0.001 |
| Corrosion | 2066692 | gated | 0.979 | 0.790 | 0.533 | 0.536 (0.20) | 0.001 |
| Corrosion | 2066692 | nugated | 0.979 | 0.780 | 0.528 | 0.532 (0.20) | 0.001 |
| Spalling | 10007679 | typed | 0.928 | 0.768 | 0.487 | 0.552 (0.05) | 0.004 |
| Spalling | 10007679 | gated | 0.928 | 0.779 | 0.482 | 0.554 (0.05) | 0.002 |
| Spalling | 10007679 | nugated | 0.927 | 0.767 | 0.457 | 0.522 (0.05) | 0.003 |
| Efflorescence | 9640891 | typed | 0.974 | 0.753 | 0.454 | 0.534 (0.05) | 0.001 |
| Efflorescence | 9640891 | gated | 0.973 | 0.751 | 0.446 | 0.529 (0.05) | 0.001 |
| Efflorescence | 9640891 | nugated | 0.973 | 0.750 | 0.397 | 0.504 (0.05) | 0.001 |

typed: mIoU@0.3 0.372, mIoU_best 0.412, mAP 0.599; gated: mIoU@0.3 0.368, mIoU_best 0.412, mAP 0.612; nugated: mIoU@0.3 0.348, mIoU_best 0.394, mAP 0.598
P-AUPRO (binary map) 0.7318
