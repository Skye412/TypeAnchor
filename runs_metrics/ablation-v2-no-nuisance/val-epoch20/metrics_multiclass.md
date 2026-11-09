## runs/ablation-v2-no-nuisance/val-epoch20 per-class (val, 400 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.963 | 0.357 | 0.259 | 0.275 (0.45) | 0.000 |
| Crack | 165419 | gated | 0.937 | 0.417 | 0.278 | 0.331 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.962 | 0.364 | 0.272 | 0.280 (0.20) | 0.000 |
| Corrosion | 402682 | typed | 0.997 | 0.854 | 0.538 | 0.638 (0.90) | 0.002 |
| Corrosion | 402682 | gated | 0.983 | 0.809 | 0.575 | 0.635 (0.65) | 0.001 |
| Corrosion | 402682 | nugated | 0.997 | 0.848 | 0.563 | 0.638 (0.80) | 0.002 |
| Spalling | 1593045 | typed | 0.995 | 0.842 | 0.588 | 0.595 (0.50) | 0.009 |
| Spalling | 1593045 | gated | 0.995 | 0.875 | 0.642 | 0.643 (0.35) | 0.005 |
| Spalling | 1593045 | nugated | 0.995 | 0.850 | 0.593 | 0.593 (0.30) | 0.007 |
| Efflorescence | 4995329 | typed | 0.993 | 0.852 | 0.567 | 0.645 (0.05) | 0.003 |
| Efflorescence | 4995329 | gated | 0.993 | 0.846 | 0.512 | 0.598 (0.05) | 0.002 |
| Efflorescence | 4995329 | nugated | 0.993 | 0.852 | 0.517 | 0.612 (0.05) | 0.002 |

typed: mIoU@0.3 0.488, mIoU_best 0.538, mAP 0.726; gated: mIoU@0.3 0.502, mIoU_best 0.552, mAP 0.737; nugated: mIoU@0.3 0.486, mIoU_best 0.531, mAP 0.728
P-AUPRO (binary map) 0.7884
