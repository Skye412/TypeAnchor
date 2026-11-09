## 原集 val 400（均值 ± 标准差，n = 种子数）

| 指标 | v2-6anchor (n=1) | no-nu-gate (n=1) | gamma0 (n=1) | gamma1 (n=1) |
|---|---|---|---|---|
| I-AUROC | 92.13 ± 0.00 | 90.98 ± 0.00 | 89.22 ± 0.00 | 92.87 ± 0.00 |
| I-AP | 87.16 ± 0.00 | 85.47 ± 0.00 | 85.23 ± 0.00 | 89.62 ± 0.00 |
| P-AUROC | 98.26 ± 0.00 | 97.94 ± 0.00 | 97.90 ± 0.00 | 98.03 ± 0.00 |
| P-AP | 70.06 ± 0.00 | 68.18 ± 0.00 | 66.02 ± 0.00 | 68.05 ± 0.00 |
| P-F1max | 70.85 ± 0.00 | 67.59 ± 0.00 | 67.82 ± 0.00 | 68.64 ± 0.00 |
| P-AUPRO | 89.64 ± 0.00 | 89.80 ± 0.00 | 89.22 ± 0.00 | 89.98 ± 0.00 |
| mAP_typed | 72.63 ± 0.00 | 69.79 ± 0.00 | 63.68 ± 0.00 | 71.07 ± 0.00 |
| mIoU@0.3_typed | 48.80 ± 0.00 | 45.68 ± 0.00 | 43.82 ± 0.00 | 47.25 ± 0.00 |
| Crack_AP_typed | 35.67 ± 0.00 | 35.46 ± 0.00 | 8.23 ± 0.00 | 37.60 ± 0.00 |
| FP@TPR0.8(%) | 1.78 ± 0.00 | 2.29 ± 0.00 | 1.82 ± 0.00 | 2.04 ± 0.00 |
| FP@TPR0.9(%) | 2.67 ± 0.00 | 3.67 ± 0.00 | 2.74 ± 0.00 | 3.06 ± 0.00 |
| bgFPR@TPR0.8(%) | 5.87 ± 0.00 | 7.23 ± 0.00 | 8.23 ± 0.00 | 6.89 ± 0.00 |

逐种子：
- runs/ablation-v2-no-nuisance: I-AUROC 92.13, I-AP 87.16, P-AUROC 98.26, P-AP 70.06, P-F1max 70.85, P-AUPRO 89.64, mAP_typed 72.63, mIoU@0.3_typed 48.80, Crack_AP_typed 35.67, FP@TPR0.8(%) 1.78, FP@TPR0.9(%) 2.67, bgFPR@TPR0.8(%) 5.87
- runs/abl-v2-no-nu-gate: I-AUROC 90.98, I-AP 85.47, P-AUROC 97.94, P-AP 68.18, P-F1max 67.59, P-AUPRO 89.80, mAP_typed 69.79, mIoU@0.3_typed 45.68, Crack_AP_typed 35.46, FP@TPR0.8(%) 2.29, FP@TPR0.9(%) 3.67, bgFPR@TPR0.8(%) 7.23
- runs/abl-v2-gamma0: I-AUROC 89.22, I-AP 85.23, P-AUROC 97.90, P-AP 66.02, P-F1max 67.82, P-AUPRO 89.22, mAP_typed 63.68, mIoU@0.3_typed 43.82, Crack_AP_typed 8.23, FP@TPR0.8(%) 1.82, FP@TPR0.9(%) 2.74, bgFPR@TPR0.8(%) 8.23
- runs/abl-v2-gamma1: I-AUROC 92.87, I-AP 89.62, P-AUROC 98.03, P-AP 68.05, P-F1max 68.64, P-AUPRO 89.98, mAP_typed 71.07, mIoU@0.3_typed 47.25, Crack_AP_typed 37.60, FP@TPR0.8(%) 2.04, FP@TPR0.9(%) 3.06, bgFPR@TPR0.8(%) 6.89

## Cleaned-Val 379（均值 ± 标准差，n = 种子数）

| 指标 | v2-6anchor (n=1) | no-nu-gate (n=1) | gamma0 (n=1) | gamma1 (n=1) |
|---|---|---|---|---|
| I-AUROC | 94.29 ± 0.00 | 93.12 ± 0.00 | 90.99 ± 0.00 | 94.46 ± 0.00 |
| I-AP | 92.71 ± 0.00 | 91.11 ± 0.00 | 90.05 ± 0.00 | 93.21 ± 0.00 |
| P-AUROC | 98.88 ± 0.00 | 98.66 ± 0.00 | 98.53 ± 0.00 | 98.68 ± 0.00 |
| P-AP | 77.63 ± 0.00 | 75.62 ± 0.00 | 73.53 ± 0.00 | 75.30 ± 0.00 |
| P-F1max | 78.35 ± 0.00 | 75.19 ± 0.00 | 74.13 ± 0.00 | 75.94 ± 0.00 |
| P-AUPRO | 91.57 ± 0.00 | 91.57 ± 0.00 | 90.81 ± 0.00 | 91.96 ± 0.00 |
| mAP_typed | 78.19 ± 0.00 | 76.92 ± 0.00 | 68.06 ± 0.00 | 78.15 ± 0.00 |
| mIoU@0.3_typed | 59.44 ± 0.00 | 56.99 ± 0.00 | 52.38 ± 0.00 | 58.73 ± 0.00 |
| Crack_AP_typed | 37.40 ± 0.00 | 38.34 ± 0.00 | 8.38 ± 0.00 | 41.05 ± 0.00 |
| FP@TPR0.8(%) | 0.12 ± 0.00 | 0.25 ± 0.00 | 0.16 ± 0.00 | 0.27 ± 0.00 |
| FP@TPR0.9(%) | 0.28 ± 0.00 | 0.53 ± 0.00 | 0.34 ± 0.00 | 0.61 ± 0.00 |
| bgFPR@TPR0.8(%) | 5.87 ± 0.00 | 7.23 ± 0.00 | 8.23 ± 0.00 | 6.89 ± 0.00 |

逐种子：
- runs/ablation-v2-no-nuisance: I-AUROC 94.29, I-AP 92.71, P-AUROC 98.88, P-AP 77.63, P-F1max 78.35, P-AUPRO 91.57, mAP_typed 78.19, mIoU@0.3_typed 59.44, Crack_AP_typed 37.40, FP@TPR0.8(%) 0.12, FP@TPR0.9(%) 0.28, bgFPR@TPR0.8(%) 5.87
- runs/abl-v2-no-nu-gate: I-AUROC 93.12, I-AP 91.11, P-AUROC 98.66, P-AP 75.62, P-F1max 75.19, P-AUPRO 91.57, mAP_typed 76.92, mIoU@0.3_typed 56.99, Crack_AP_typed 38.34, FP@TPR0.8(%) 0.25, FP@TPR0.9(%) 0.53, bgFPR@TPR0.8(%) 7.23
- runs/abl-v2-gamma0: I-AUROC 90.99, I-AP 90.05, P-AUROC 98.53, P-AP 73.53, P-F1max 74.13, P-AUPRO 90.81, mAP_typed 68.06, mIoU@0.3_typed 52.38, Crack_AP_typed 8.38, FP@TPR0.8(%) 0.16, FP@TPR0.9(%) 0.34, bgFPR@TPR0.8(%) 8.23
- runs/abl-v2-gamma1: I-AUROC 94.46, I-AP 93.21, P-AUROC 98.68, P-AP 75.30, P-F1max 75.94, P-AUPRO 91.96, mAP_typed 78.15, mIoU@0.3_typed 58.73, Crack_AP_typed 41.05, FP@TPR0.8(%) 0.27, FP@TPR0.9(%) 0.61, bgFPR@TPR0.8(%) 6.89

