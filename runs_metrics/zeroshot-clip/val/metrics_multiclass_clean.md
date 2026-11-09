## runs/zeroshot-clip/val per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.845 | 0.036 | 0.002 | 0.011 (0.95) | 1.000 |
| Crack | 165419 | gated | 0.845 | 0.036 | 0.002 | 0.042 (0.95) | 0.991 |
| Corrosion | 402682 | typed | 0.935 | 0.242 | 0.013 | 0.194 (0.75) | 0.268 |
| Corrosion | 402682 | gated | 0.914 | 0.185 | 0.017 | 0.153 (0.65) | 0.189 |
| Spalling | 1593045 | typed | 0.737 | 0.060 | 0.021 | 0.070 (0.65) | 0.631 |
| Spalling | 1593045 | gated | 0.671 | 0.039 | 0.023 | 0.048 (0.60) | 0.473 |
| Efflorescence | 4995329 | typed | 0.651 | 0.094 | 0.043 | 0.076 (0.10) | 0.012 |
| Efflorescence | 4995329 | gated | 0.632 | 0.085 | 0.029 | 0.071 (0.10) | 0.007 |

typed: mIoU@0.3 0.020, mIoU_best 0.088, mAP 0.108; gated: mIoU@0.3 0.017, mIoU_best 0.079, mAP 0.086
P-AUPRO (binary map) 0.2680
