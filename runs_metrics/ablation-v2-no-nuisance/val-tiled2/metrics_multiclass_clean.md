## runs/ablation-v2-no-nuisance/val-tiled2 per-class (val, 379 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 165419 | typed | 0.944 | 0.432 | 0.205 | 0.287 (0.05) | 0.000 |
| Crack | 165419 | gated | 0.924 | 0.539 | 0.127 | 0.271 (0.05) | 0.000 |
| Crack | 165419 | nugated | 0.944 | 0.442 | 0.115 | 0.263 (0.05) | 0.000 |
| Corrosion | 402682 | typed | 0.993 | 0.843 | 0.456 | 0.598 (0.05) | 0.000 |
| Corrosion | 402682 | gated | 0.988 | 0.764 | 0.319 | 0.438 (0.05) | 0.000 |
| Corrosion | 402682 | nugated | 0.992 | 0.820 | 0.370 | 0.530 (0.05) | 0.000 |
| Spalling | 1593045 | typed | 0.969 | 0.823 | 0.397 | 0.488 (0.05) | 0.000 |
| Spalling | 1593045 | gated | 0.964 | 0.828 | 0.341 | 0.459 (0.05) | 0.000 |
| Spalling | 1593045 | nugated | 0.969 | 0.820 | 0.339 | 0.456 (0.05) | 0.000 |
| Efflorescence | 4995329 | typed | 0.946 | 0.670 | 0.158 | 0.287 (0.05) | 0.001 |
| Efflorescence | 4995329 | gated | 0.943 | 0.672 | 0.105 | 0.215 (0.05) | 0.000 |
| Efflorescence | 4995329 | nugated | 0.945 | 0.666 | 0.103 | 0.216 (0.05) | 0.000 |

typed: mIoU@0.3 0.304, mIoU_best 0.415, mAP 0.692; gated: mIoU@0.3 0.223, mIoU_best 0.346, mAP 0.701; nugated: mIoU@0.3 0.232, mIoU_best 0.366, mAP 0.687
P-AUPRO (binary map) 0.8356
