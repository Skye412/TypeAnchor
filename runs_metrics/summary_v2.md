## 原集 val 400（均值 ± 标准差，n = 种子数）

| 指标 | v2 (n=3) | v2-no-nuisance (n=3) |
|---|---|---|
| I-AUROC | 92.61 ± 0.27 | 92.33 ± 0.29 |
| I-AP | 87.38 ± 1.67 | 87.03 ± 0.30 |
| P-AUROC | 97.89 ± 0.51 | 98.17 ± 0.10 |
| P-AP | 67.05 ± 4.97 | 68.27 ± 1.27 |
| P-F1max | 68.08 ± 5.20 | 70.57 ± 1.37 |
| P-AUPRO | 90.16 ± 1.66 | 89.76 ± 0.21 |
| mAP_typed | 71.43 ± 1.11 | 71.08 ± 1.12 |
| mIoU@0.3_typed | 45.25 ± 2.23 | 46.15 ± 1.88 |
| Crack_AP_typed | 38.75 ± 1.62 | 33.39 ± 2.41 |
| FP@TPR0.8(%) | 2.47 ± 0.92 | 2.17 ± 0.29 |
| FP@TPR0.9(%) | 3.51 ± 1.00 | 3.33 ± 0.47 |
| bgFPR@TPR0.8(%) | 6.55 ± 1.89 | 5.01 ± 1.00 |

逐种子：
- runs/nuisance-v2: I-AUROC 92.99, I-AP 89.30, P-AUROC 97.80, P-AP 68.09, P-F1max 66.65, P-AUPRO 90.27, mAP_typed 72.15, mIoU@0.3_typed 45.53, Crack_AP_typed 40.53, FP@TPR0.8(%) 2.19, FP@TPR0.9(%) 3.22, bgFPR@TPR0.8(%) 8.17
- runs/nuisance-v2-s11: I-AUROC 92.42, I-AP 87.60, P-AUROC 98.55, P-AP 72.56, P-F1max 75.04, P-AUPRO 92.14, mAP_typed 72.27, mIoU@0.3_typed 47.83, Crack_AP_typed 36.61, FP@TPR0.8(%) 1.51, FP@TPR0.9(%) 2.45, bgFPR@TPR0.8(%) 3.90
- runs/nuisance-v2-s12: I-AUROC 92.41, I-AP 85.22, P-AUROC 97.31, P-AP 60.52, P-F1max 62.54, P-AUPRO 88.07, mAP_typed 69.85, mIoU@0.3_typed 42.39, Crack_AP_typed 39.11, FP@TPR0.8(%) 3.72, FP@TPR0.9(%) 4.85, bgFPR@TPR0.8(%) 7.59
- runs/ablation-v2-no-nuisance: I-AUROC 92.13, I-AP 87.16, P-AUROC 98.26, P-AP 70.06, P-F1max 70.85, P-AUPRO 89.64, mAP_typed 72.63, mIoU@0.3_typed 48.80, Crack_AP_typed 35.67, FP@TPR0.8(%) 1.78, FP@TPR0.9(%) 2.67, bgFPR@TPR0.8(%) 5.87
- runs/ablation-v2-no-nuisance-s11: I-AUROC 92.74, I-AP 87.32, P-AUROC 98.23, P-AP 67.54, P-F1max 72.09, P-AUPRO 90.06, mAP_typed 70.00, mIoU@0.3_typed 44.60, Crack_AP_typed 30.05, FP@TPR0.8(%) 2.27, FP@TPR0.9(%) 3.74, bgFPR@TPR0.8(%) 3.61
- runs/ablation-v2-no-nuisance-s12: I-AUROC 92.12, I-AP 86.62, P-AUROC 98.03, P-AP 67.21, P-F1max 68.77, P-AUPRO 89.59, mAP_typed 70.62, mIoU@0.3_typed 45.05, Crack_AP_typed 34.45, FP@TPR0.8(%) 2.48, FP@TPR0.9(%) 3.56, bgFPR@TPR0.8(%) 5.55

## Cleaned-Val 379（均值 ± 标准差，n = 种子数）

| 指标 | v2 (n=3) | v2-no-nuisance (n=3) |
|---|---|---|
| I-AUROC | 94.79 ± 0.32 | 94.59 ± 0.33 |
| I-AP | 92.87 ± 0.34 | 93.01 ± 0.38 |
| P-AUROC | 98.73 ± 0.31 | 98.96 ± 0.12 |
| P-AP | 76.68 ± 3.36 | 78.20 ± 1.05 |
| P-F1max | 77.09 ± 4.46 | 79.71 ± 2.17 |
| P-AUPRO | 92.47 ± 1.34 | 92.23 ± 0.52 |
| mAP_typed | 78.80 ± 0.53 | 77.51 ± 0.98 |
| mIoU@0.3_typed | 60.14 ± 2.12 | 58.53 ± 1.33 |
| Crack_AP_typed | 40.56 ± 2.28 | 34.50 ± 2.79 |
| FP@TPR0.8(%) | 0.24 ± 0.15 | 0.18 ± 0.06 |
| FP@TPR0.9(%) | 0.54 ± 0.28 | 0.43 ± 0.13 |
| bgFPR@TPR0.8(%) | 6.55 ± 1.89 | 5.01 ± 1.00 |

逐种子：
- runs/nuisance-v2: I-AUROC 94.78, I-AP 93.28, P-AUROC 98.50, P-AP 75.49, P-F1max 73.92, P-AUPRO 91.98, mAP_typed 79.03, mIoU@0.3_typed 59.43, Crack_AP_typed 43.14, FP@TPR0.8(%) 0.19, FP@TPR0.9(%) 0.57, bgFPR@TPR0.8(%) 8.17
- runs/nuisance-v2-s11: I-AUROC 94.40, I-AP 92.88, P-AUROC 99.17, P-AP 81.26, P-F1max 83.40, P-AUPRO 94.29, mAP_typed 79.30, mIoU@0.3_typed 63.02, Crack_AP_typed 37.61, FP@TPR0.8(%) 0.09, FP@TPR0.9(%) 0.18, bgFPR@TPR0.8(%) 3.90
- runs/nuisance-v2-s12: I-AUROC 95.18, I-AP 92.46, P-AUROC 98.51, P-AP 73.28, P-F1max 73.97, P-AUPRO 91.12, mAP_typed 78.06, mIoU@0.3_typed 57.98, Crack_AP_typed 40.92, FP@TPR0.8(%) 0.45, FP@TPR0.9(%) 0.87, bgFPR@TPR0.8(%) 7.59
- runs/ablation-v2-no-nuisance: I-AUROC 94.29, I-AP 92.71, P-AUROC 98.88, P-AP 77.63, P-F1max 78.35, P-AUPRO 91.57, mAP_typed 78.19, mIoU@0.3_typed 59.44, Crack_AP_typed 37.40, FP@TPR0.8(%) 0.12, FP@TPR0.9(%) 0.28, bgFPR@TPR0.8(%) 5.87
- runs/ablation-v2-no-nuisance-s11: I-AUROC 95.06, I-AP 93.55, P-AUROC 99.13, P-AP 79.67, P-F1max 82.77, P-AUPRO 92.85, mAP_typed 76.13, mIoU@0.3_typed 56.64, Crack_AP_typed 30.73, FP@TPR0.8(%) 0.17, FP@TPR0.9(%) 0.43, bgFPR@TPR0.8(%) 3.61
- runs/ablation-v2-no-nuisance-s12: I-AUROC 94.44, I-AP 92.77, P-AUROC 98.85, P-AP 77.30, P-F1max 78.00, P-AUPRO 92.26, mAP_typed 78.22, mIoU@0.3_typed 59.50, Crack_AP_typed 35.37, FP@TPR0.8(%) 0.26, FP@TPR0.9(%) 0.59, bgFPR@TPR0.8(%) 5.55

