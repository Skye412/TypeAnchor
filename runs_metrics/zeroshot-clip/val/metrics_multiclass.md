## runs/zeroshot-clip/val per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.848 | 0.034 | 0.002 | 0.011 (0.95) | 1.000 |
| Crack | 165419 | gated | 0.848 | 0.034 | 0.002 | 0.041 (0.95) | 0.990 |
| Corrosion | 402682 | typed | 0.932 | 0.198 | 0.012 | 0.164 (0.75) | 0.281 |
| Corrosion | 402682 | gated | 0.911 | 0.159 | 0.016 | 0.136 (0.65) | 0.198 |
| Spalling | 1593045 | typed | 0.734 | 0.056 | 0.020 | 0.067 (0.65) | 0.638 |
| Spalling | 1593045 | gated | 0.670 | 0.037 | 0.021 | 0.046 (0.60) | 0.478 |
| Efflorescence | 4995329 | typed | 0.645 | 0.088 | 0.042 | 0.071 (0.10) | 0.013 |
| Efflorescence | 4995329 | gated | 0.627 | 0.079 | 0.028 | 0.067 (0.10) | 0.008 |

typed: mIoU@0.3 0.019, mIoU_best 0.078, mAP 0.094; gated: mIoU@0.3 0.017, mIoU_best 0.072, mAP 0.077
P-AUPRO (binary map) 0.2709
