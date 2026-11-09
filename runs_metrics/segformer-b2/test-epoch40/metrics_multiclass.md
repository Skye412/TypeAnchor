## runs/segformer-b2/test-epoch40 per-class (test, 809 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 366536 | typed | 0.684 | 0.241 | 0.205 | 0.217 (0.05) | 0.000 |
| Crack | 366536 | gated | 0.684 | 0.240 | 0.197 | 0.207 (0.05) | 0.000 |
| Corrosion | 2066692 | typed | 0.935 | 0.818 | 0.673 | 0.681 (0.90) | 0.002 |
| Corrosion | 2066692 | gated | 0.935 | 0.819 | 0.678 | 0.685 (0.90) | 0.002 |
| Spalling | 10007679 | typed | 0.886 | 0.761 | 0.652 | 0.661 (0.05) | 0.004 |
| Spalling | 10007679 | gated | 0.886 | 0.762 | 0.639 | 0.655 (0.05) | 0.003 |
| Efflorescence | 9640891 | typed | 0.849 | 0.585 | 0.457 | 0.457 (0.50) | 0.005 |
| Efflorescence | 9640891 | gated | 0.849 | 0.585 | 0.457 | 0.457 (0.30) | 0.005 |

typed: mIoU@0.3 0.497, mIoU_best 0.504, mAP 0.601; gated: mIoU@0.3 0.493, mIoU_best 0.501, mAP 0.601
P-AUPRO (binary map) 0.6858
