## runs/ext-multiads/test per-class (test, 809 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 366536 | typed | 0.979 | 0.152 | 0.157 | 0.159 (0.25) | 0.001 |
| Crack | 366536 | gated | 0.975 | 0.176 | 0.141 | 0.184 (0.15) | 0.001 |
| Corrosion | 2066692 | typed | 0.989 | 0.799 | 0.562 | 0.562 (0.30) | 0.004 |
| Corrosion | 2066692 | gated | 0.990 | 0.802 | 0.556 | 0.562 (0.25) | 0.002 |
| Spalling | 10007679 | typed | 0.940 | 0.710 | 0.491 | 0.498 (0.25) | 0.010 |
| Spalling | 10007679 | gated | 0.960 | 0.747 | 0.359 | 0.538 (0.10) | 0.003 |
| Efflorescence | 9640891 | typed | 0.949 | 0.587 | 0.375 | 0.390 (0.25) | 0.006 |
| Efflorescence | 9640891 | gated | 0.930 | 0.534 | 0.228 | 0.352 (0.10) | 0.001 |

typed: mIoU@0.3 0.396, mIoU_best 0.402, mAP 0.562; gated: mIoU@0.3 0.321, mIoU_best 0.409, mAP 0.565
P-AUPRO (binary map) 0.7884
