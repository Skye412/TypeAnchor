# 假阳性审计设计（2026-10-29）

模式：design（先导诊断实验，非发表主实验）
场合与假设：桥梁 CODEBRIM 裁块；主张来自 idea-card.md 的核心洞见。

## 要回答的问题
H1：在桥梁正常图上，现有"偏离参考"类检测器的假阳性面积，主要落在可命名的良性干扰上，而不是连续低层变异上。
H2（次要）：可命名干扰相对正常参考的偏离幅度不小于低层变异（否则"统计擦除原理上处理不了"的论证不成立）。
H3（次要）：正常图标签噪声（未标注的真实缺陷）占比可控。

## 预注册决策规则（审计前冻结）
令 share_A = 类别 A 的假阳性面积 / (A+B+C+E 总面积)，D 单独统计。
- 两个被审计模型的 share_A 均 ≥ 0.50 → 维持主路线。
- 任一模型 share_B ≥ 0.50 → 转备用路线（统计擦除 vs 语义锚定的诊断研究）。
- 其余（A、B 均在 0.30–0.50）→ 维持主路线，但 P3 互补性预测升为核心主张。
- D ≥ 0.15 → 先清洗正常图标签，再重跑审计。
- H2 检验：A 类块的平均残差分 ≥ B 类块；若显著低于，洞见第二段需改写。

## 被审计模型（均不在自建集上训练）
| 模型 | 代表什么 | 配置 | 来源 |
|---|---|---|---|
| AdaptCLIP 官方权重 | CLIP 系 + 参考残差 | ViT-L/14@336，518 输入；zero-shot 与 4-shot 各一套图；4-shot 参考从训练集正常图随机抽 4 张，固定种子 | github.com/gaobb/AdaptCLIP |
| AnomalyDINO | 纯视觉残差（训练免费） | DINOv2-B/14，参考 = 训练集正常图随机 16 张，patch 最近邻距离 | github.com/dammsi/AnomalyDINO |
| IDEAL（可选） | 统计擦除 | 若 mala-lab/IDEAL 代码可跑：正常参考 16 张 + 异常参考每类 4 张（来自训练集） | arXiv 2605.23231 |

AdaptCLIP 与 AnomalyDINO 为必做；IDEAL 能跑则加，直接服务 H2 与 P3。

## 数据
- 审计图像：验证集正常图 277 张（不动测试集）。
- 阈值标定：验证集异常图 123 张。
- 参考图：训练集正常图。

## 阈值
每个模型独立标定：在验证集异常图上取像素级 TPR = 95% 对应的阈值（与 FPR@95TPR 约定一致）。同时记录该阈值下验证集异常图的像素 FPR 作参考。不使用各模型论文的默认阈值。

## 假阳性块的提取与抽样
1. 对每张正常图的异常图做阈值二值化，取 8 连通块，丢弃面积 < 64 px（512² 下约 0.02%）的块。
2. 记录每块：图像名、面积、包围框、块内平均分、块内最大分。
3. 抽样：每个模型按面积三分位分层，每层 40 块，共 120 块/模型；三个模型最多 360 块。面积分层是为了让面积占比估计不被大量小块主导。
4. 导出每块的标注卡：原图 + 块轮廓叠加 + 局部放大（块包围框外扩 32 px），文件名含块 ID。

## 标注分类体系（冻结）
A 可命名良性干扰：A1 水渍/湿斑；A2 阴影/光照边界；A3 苔藓/生物附着（薄层）；A4 修补/砂浆填充；A5 涂鸦/油漆；A6 模板纹理/施工缝/构件边缘；A7 污垢/烟熏。
B 连续低层变异：B1 骨料/表面纹理颗粒；B2 平滑光照渐变/曝光；B3 模糊/噪声/压缩伪影。
C 非表面区域：C1 背景物体（天空、构件外植被、线缆）；C2 裁块边界/填充。
D 疑似真实缺陷（正常图标签噪声）：D1 疑似四类之一；D2 疑似其他缺陷。
E 无法判断。

每块只选一个主类别；若块跨两类，按面积大者。标注者为用户本人；随机抽 20% 块在一周后盲重标，报告自一致率。

## 统计输出
- 表 1：每模型 × 类别的块数占比与面积占比（面积占比用分层权重还原）。
- 表 2：每模型 A、B、C、D、E 的汇总面积占比，附决策规则判定。
- 表 3（H2）：每模型 A 类与 B 类块的平均分、最大分及差值。
- 图 1：每模型的假阳性面积占比堆叠条形图（类别 A–E），作为论文动机图候选。
- 图 2：每类别 2–3 个代表块示例。

## 结果表模板
| 模型 | A 面积占比 | B | C | D | E | 判定 |
|---|---|---|---|---|---|---|
| AdaptCLIP zero-shot | — | — | — | — | — | — |
| AdaptCLIP 4-shot | — | — | — | — | — | — |
| AnomalyDINO 16-shot | — | — | — | — | — | — |
| IDEAL（可选） | — | — | — | — | — | — |

## 执行顺序与成本
1. 跑三个模型在 400 张验证图上的异常图并存为 npy（GPU 约 1 小时）。
2. 运行 audit_fp.py extract → sample → export（CPU 几分钟）。
3. 人工标注约 240–360 块（约 3–4 小时）。
4. 运行 audit_fp.py summarize，生成表 1–3 与图 1。
5. 按决策规则判定并回写 idea-card.md。

## 缺失值
所有结果单元格为"—"直到实际执行。本文件不含任何预测数值。

## 下一个 CCFA 负责人
执行后若需论文动机图成稿：ccf-visual-composer。若判定转备用路线：ccf-idea-optimizer。

## 脚本用法（audit_fp.py，已用合成数据自检全流程）
依赖：numpy、pillow、scipy、matplotlib。每个模型先把验证集 400 张图的异常图存为 `<maps_dir>/<图名>.npy`（float，512×512）。

```bash
python audit_fp.py threshold --model adaptclip_zs --maps maps/adaptclip_zs --masks val/masks_union --anomaly-list val/anomaly.txt --out audit/adaptclip_zs
python audit_fp.py extract   --model adaptclip_zs --maps maps/adaptclip_zs --normal-list val/normal.txt --out audit/adaptclip_zs
python audit_fp.py sample    --per-stratum 40 --out audit/adaptclip_zs
python audit_fp.py export    --maps maps/adaptclip_zs --images val/images --out audit/adaptclip_zs
# 人工在 audit/<model>/sample.csv 的 label 列填 A1–E，对照 cards/ 目录的标注卡
python audit_fp.py summarize --samples audit/adaptclip_zs/sample.csv audit/adaptclip_4s/sample.csv audit/anomalydino/sample.csv --out audit/summary
```

`masks_union` 为四类掩码的并集二值图（>0 为缺陷）。summarize 会按预注册规则直接给出每个模型的判定，并输出 fig1-fp-share.png。
