# 实验结果汇总（CODEBRIM 验证集，400 张：277 正常 / 123 异常）

更新：2026-11-01。所有数字来自服务器 `runs/` 下的 metrics 文件；测试集在开发阶段不碰（已有一次 baseline-v1 的 test-zero-cpu 结果，仅记录，不用于比较）。

## 1. 二元异常检测

| 模型 | I-AUROC | I-AP | I-F1max | P-AUROC | P-AP | P-F1max | P-AUPRO |
|---|---|---|---|---|---|---|---|
| baseline-v1（官方 AdaptCLIP 三适配器，15 epoch） | 91.3 | 83.9 | 78.9 | 96.9 | 61.8 | 67.3 | 81.4 |
| nuisance-v0（13 锚点，20 epoch） | 88.0 | 84.9 | 78.0 | 97.7 | 69.7 | 67.1 | **92.0** |
| ablation-no-nuisance（6 锚点，去掉 7 个干扰锚点） | 训练中 | | | | | | |

- 两行像素指标的 GT 相同：原拍平并集掩码双线性缩到 518、>127 为正；P-AUPRO 用同一 `metrics.AUPRO`（fpr_limit 0.3）在 518 分辩率上计算，与 baseline-v1 评估器一致。nuisance-v0 的 P-AUPRO 在 CPU 上算得（GPU 被其他进程占用），数值不受设备影响。
- nuisance-v0 的图像级分数 = 0.5·图像头 softmax + 0.5·二元图 top-1% 均值，与基线的融合方式不同，I-AUROC 的 3 点差距混杂了融合方式差异，不能直接归因到模型。
- P-AUPRO 从 81.4 到 92.0 是目前最大的一项提升，P-AP +7.9。AUPRO 偏向"每个连通块都被覆盖"，说明新模型漏掉的缺陷块更少，而不是像素更准（P-F1max 持平）。

## 2. 按类多标签分割（nuisance-v0，dacl10k 式协议）

GT 来自 `multiclass_annotations/masks/<sample>__<Class>.png`（原始分层标注栅格化，允许重叠），最近邻缩到 518。两种预测：typed = π_c 上采样；gated = π_c × A_res。

| 类别 | GT 像素 | 变体 | P-AUROC | P-AP | IoU@0.3 | IoU_best（阈值） | 正常图被标面积@0.3 |
|---|---|---|---|---|---|---|---|
| 裂缝 | 165,419 | typed | 0.950 | 0.068 | 0.081 | 0.083（0.35） | 0.000 |
| 裂缝 | | gated | 0.803 | 0.182 | 0.154 | 0.195（0.10） | 0.000 |
| 锈蚀 | 402,682 | typed | 0.988 | 0.551 | 0.364 | 0.467（0.20） | 0.001 |
| 锈蚀 | | gated | 0.936 | 0.743 | 0.355 | 0.615（0.15） | 0.000 |
| 剥落 | 1,593,045 | typed | 0.996 | 0.801 | 0.584 | 0.590（0.35） | 0.008 |
| 剥落 | | gated | 0.991 | 0.865 | 0.640 | 0.670（0.15） | 0.003 |
| 泛碱 | 4,995,329 | typed | 0.987 | 0.785 | 0.574 | 0.592（0.15） | 0.005 |
| 泛碱 | | gated | 0.974 | 0.732 | 0.423 | 0.517（0.05） | 0.002 |

汇总：mIoU@0.3 typed 0.401 / gated 0.393；mIoU_best typed 0.433 / gated 0.499（阈值在验证集上选，偏乐观）；mAP typed 0.551 / gated 0.630。

解读与边界：
- 裂缝几乎失效（typed P-AP 0.07）。裂缝细长，37×37 的 patch 网格每格约 14 像素，裂缝宽度常小于一格，softmax 竞争里裂缝很难在整格上胜出；gated 变体靠残差把它拉到 0.18，仍远低于其他类。这是分辩率问题，不是锚点问题，要单独解决（高分辩率分支或多尺度窗口）。
- 锈蚀 typed IoU 0.36 偏低但 gated 的 IoU_best 0.61：π_corrosion 在非缺陷背景上有弥散的小概率，被残差门控抑制后好很多。说明"类型概率需要残差门控"对小面积类成立，对大面积类（泛碱）则反而损失召回。最终输出宜按类选变体，或把门控做成可学习的。
- 正常图上各类被标面积 ≤ 0.8%，类型通道本身几乎不在正常图上报警；此前审计里正常图 18% 的被标面积来自冻结骨干的残差，不是这里的类型头。
- IoU@0.3 使用模型规格里的初始阈值；IoU_best 只作上限参考，不进主表。

## 3. 前提检验：统计擦除充分性（已完成，见 audit-design.md）

DINOv2 与 CLIP 骨干上，IDEAL 式 NVE 擦除（α=0.8）使正常图被标面积仅变化 −2.9% / −1.8%，完全投影（α=0）反而上升；预注册判定"统计擦除不足，主路线成立"。

## 4. 进行中与待做

- **ablation-no-nuisance**（P2 聚合版）：2026-11-01 15:30 启动，20 epoch，seed 10，同一正常库；完成后用同一套脚本评估（`scripts/train_ablation.sh`）。预期若干扰锚点有效：正常图被标面积与 P-AUPRO 应劣于 v0；若两者持平，则 v0 的提升来自残差头与解释损失而非干扰锚点，论文主张要改。
- 服务器 nuisance-v0 的实现与 model-spec v0.1 有偏差（逐层视觉 MLP 替代共享适配器、3×3 卷积分割头、batch 1 + 8 步累积、L_pseudo 关闭），尚未在 model-spec 中登记。
- 未做：IDEAL 完整方法基线；P1（簇留出参考）、P3（擦除 + 锚点叠加）、P4（库规模）；S2DS / dacl10k 跨数据集；裂缝分辩率问题的对策。

## 5. 复现命令

```bash
python eval_nuisance.py --checkpoint runs/nuisance-v0/epoch_20.pth --out runs/nuisance-v0/val-epoch20 --save-typed
python metrics_nuisance.py runs/nuisance-v0/val-epoch20
python metrics_multiclass.py --run runs/nuisance-v0/val-epoch20          # AUPRO 默认在 CPU
bash scripts/train_ablation.sh no-nuisance runs/ablation-no-nuisance      # 训练 + 评估一体
```
