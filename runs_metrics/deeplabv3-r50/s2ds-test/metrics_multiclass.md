## runs/deeplabv3-r50/s2ds-test per-class (test, 447 images)

| class | GT px | variant | P-AUROC | P-AP | IoU@0.3 | IoU_best (thr) | normal flagged@0.3 |
|---|---|---|---|---|---|---|---|
| Crack | 107645 | typed | 0.648 | 0.067 | 0.067 | 0.075 (0.05) | 0.000 |
| Crack | 107645 | gated | 0.648 | 0.067 | 0.063 | 0.069 (0.05) | 0.000 |
| Corrosion | 2041564 | typed | 0.714 | 0.318 | 0.214 | 0.234 (0.05) | 0.000 |
| Corrosion | 2041564 | gated | 0.714 | 0.318 | 0.206 | 0.224 (0.05) | 0.000 |
| Spalling | 9401631 | typed | 0.694 | 0.326 | 0.217 | 0.233 (0.05) | 0.000 |
| Spalling | 9401631 | gated | 0.694 | 0.325 | 0.205 | 0.220 (0.05) | 0.000 |
| Efflorescence | 2162061 | typed | 0.788 | 0.169 | 0.159 | 0.162 (0.70) | 0.031 |
| Efflorescence | 2162061 | gated | 0.788 | 0.168 | 0.161 | 0.162 (0.50) | 0.030 |

typed: mIoU@0.3 0.164, mIoU_best 0.176, mAP 0.220; gated: mIoU@0.3 0.159, mIoU_best 0.169, mAP 0.220
P-AUPRO (binary map) 0.2200
