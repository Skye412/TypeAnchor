## runs/deeplabv3-r50/test-epoch40 per-class (test, 809 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 366536 | typed | 0.691 | 0.219 | 0.202 | 0.202 (0.15) | 0.000 |
| Crack | 366536 | gated | 0.691 | 0.220 | 0.200 | 0.202 (0.05) | 0.000 |
| Corrosion | 2066692 | typed | 0.889 | 0.665 | 0.531 | 0.534 (0.60) | 0.001 |
| Corrosion | 2066692 | gated | 0.889 | 0.662 | 0.529 | 0.530 (0.50) | 0.001 |
| Spalling | 10007679 | typed | 0.837 | 0.635 | 0.463 | 0.486 (0.05) | 0.003 |
| Spalling | 10007679 | gated | 0.837 | 0.638 | 0.454 | 0.472 (0.05) | 0.003 |
| Efflorescence | 9640891 | typed | 0.964 | 0.849 | 0.631 | 0.647 (0.05) | 0.001 |
| Efflorescence | 9640891 | gated | 0.964 | 0.849 | 0.621 | 0.635 (0.05) | 0.001 |

typed: mIoU@0.3 0.457, mIoU_best 0.467, mAP 0.592; gated: mIoU@0.3 0.451, mIoU_best 0.460, mAP 0.592
P-AUPRO (binary map) 0.6191
