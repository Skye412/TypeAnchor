# Nuisance-aware AdaptCLIP 模型与损失设计

- v0.2（2026-11-03）：现行实现 v2，见文末 §10；对应服务器 `nuisance_model.py` 的 `NuisanceHeadV2` / `explanation_loss_v2` 与 `train_nuisance.py` 的 `AnchorsV2`（提交 ae776d9 及之后）。
- v0.1（2026-10-29）：首版设计，§1–§9。服务器 nuisance-v0 按此实现但有偏差（逐层视觉 MLP 替代共享适配器、3×3 卷积分割头、batch 1 + 8 步累积、L_pseudo 关闭）。

## v0.1（2026-10-29）

状态：首版设计稿。所有超参为初始值。

## 1. 记号与骨干
- 骨干：CLIP ViT-L/14@336，冻结。输入 518×518，patch 网格 37×37，N = 1369，d = 1024。取层 l ∈ {6, 12, 18, 24} 的 patch token F_l ∈ R^{N×d}。文本编码器冻结，输出维 d_t = 768。
- 每层一个可学习线性投影 P_l: R^d → R^{d_t}，把视觉 token 投到文本空间（沿用 AnomalyCLIP / AdaptCLIP 做法）。
- 查询图 x；正常库 𝒩 = 训练集正常图（1,944 张）。

## 2. 组件 M1：检索式正常参考
- 库向量：g(n) = CLIP 全局图像嵌入（层 24 的 CLS 经投影头）。离线算好。
- 检索：对查询 x，取余弦相似度 top-k（k = 4）正常图 {n_j}。
- 对齐残差（沿用 AdaptCLIP prompt-query adapter）：对每层 l、每个查询 token q_{l,i}，在 k 张参考的全部 token 中取 L2 最近邻 n*_{l,i}，残差 r_{l,i} = |q_{l,i} − n*_{l,i}|（逐维绝对值）。上下文特征 z_{l,i} = [q_{l,i}; r_{l,i}] ∈ R^{2d}。
- 残差分割头 H_res：AdaptCLIP 原头（四层 z 经 1×1 卷积降到 128，逐层转置卷积 2× 上采样后相加，再 1×1 输出 1 通道）→ A_res ∈ [0,1]^{518×518}。图像头：对四层 z 做 avg/max 池化拼接 → MLP → 图像级分数 a_res。
- 消融点：k ∈ {1, 4, 8}；随机参考 vs 检索参考；库规模 {10%, 30%, 100%}。

## 3. 贡献 M2：语义锚点与竞争式解释
### 3.1 锚点集合（13 个）
| 组 | 锚点 | 文本名（固定） | 可学习上下文 |
|---|---|---|---|
| 正常 | T_0 | intact concrete surface | 12 个 token |
| 缺陷类型 | T_1..T_4 | crack / corrosion / spalling / efflorescence | 各 12 个 |
| 类无关缺陷 | T_g | damaged concrete surface | 12 个 |
| 良性干扰 | T_u1..T_u7 | water stain, shadow, moss, patch repair, graffiti, formwork texture, dirt | 各 12 个 |

- corrosion 用两条子提示（rust stain on concrete / exposed corroded rebar）取文本嵌入均值。
- 每个锚点的提示 = [可学习上下文 12 token] + [固定类名 token]，过冻结文本编码器得 t ∈ R^{d_t}。上下文按锚点独立，不共享（DAPO 报告共享更好，但那是同域工业数据；此处留消融）。
- 模板集成：每个锚点用 4 条模板（"a photo of {}", "a close-up photo of {} on a bridge", "{} on a concrete wall", "an inspection image showing {}"）求均值。

### 3.2 patch 级相似度与残差加权邻域池化（区域级近似）
- 相似度 S_{l,i,a} = cos(P_l F_{l,i}, t_a) / τ，τ = 0.07。四层平均得 S_i ∈ R^{13}。
- 邻域池化（可微的"连通块级比较"）：在 5×5 窗内，权重 w_{ij} ∝ Ā_j · exp(−‖p_i − p_j‖² / 2σ²)，σ = 1.5 patch，Ā 为 A_res 下采样到 37×37。Ŝ_i = Σ_j w_{ij} S_j / Σ_j w_{ij}。
  - 作用：高残差块内的 token 互相借证据，低残差背景不参与，近似"先取块再池化比锚点"，且端到端可微。
  - 消融：σ = 0（退化为逐 patch），σ = 1.5，硬连通块池化（不可微，仅推理）。

### 3.3 竞争式解释
- π_i = softmax(Ŝ_i) ∈ Δ^{13}，含正常、4 类缺陷、类无关缺陷、7 类干扰。
- 缺陷质量 ν_i = π_{i,g} + Σ_{c=1..4} π_{i,c}；干扰质量 μ_i = Σ_u π_{i,u}。
- 阴影里的锈迹：锈的文本证据进入 π_{i,corrosion}，与 shadow 竞争而非被 shadow 一票否决。

### 3.4 输出
- 类型图 M_c = up(π_{·,c})，c = 1..4，上采样到 518。多标签判定：M_c ≥ τ_c（τ_c 在验证集按 per-class IoU 选，初始 0.3），不用 argmax，所以剥落内的锈蚀可同时为正。
- 类无关缺陷图 A_cls = A_res ⊙ up(ν)。
- 二元异常图 A_bin = max(A_cls, max_c M_c)。图像级分数 = 0.5·a_res + 0.5·max_i A_bin（top-1% 均值）。
- 未知缺陷：A_cls ≥ τ_bin 且 max_c M_c < τ_c 的像素标为 unknown。
- 干扰解释图 U = up(μ) 仅作可视化与审计，不参与评分。

## 4. 训练数据组织
- 二元 AdaptCLIP 基线只用 Y_∪，与掩码路径无关，可先行启动。
- 每个 batch：异常图与正常图各半（约 1:1 重采样，训练集比例原为 917:1944）。
- 异常图 GT，两条路径：
  - 路径 A（目标）：4 通道二值掩码 Y_c 从原始分层标注重建，允许重叠；并集 Y_∪ = max_c Y_c。
  - 路径 B（当前服务器可用，2026-10-29 起先用）：拍平 RGB 掩码按调色板解码为单标签图 y ∈ {0,1,2,3,4}，Y_c = [y = c]，像素互斥；Y_∪ = [y > 0]。与路径 A 的唯一差别是 L_exp 的缺陷像素软目标退化为 one-hot，其余损失、结构、推理不变。换到路径 A 时只需替换数据加载器，不改模型与训练代码。
  - 路径 B 的已知偏差：裂缝 > 锈蚀 > 剥落 > 泛碱的拍平优先级使剥落与泛碱在重叠处被扣掉，这两类的 IoU 会被系统性低估；二元指标与开放集评估不受影响。切换到路径 A 后需重跑 per-class 指标。
  - 解码前先统计全部掩码的唯一颜色集合并固化调色板文件；若出现调色板之外的颜色（抗锯齿或混合色），按最近颜色归类并记录数量。
- 正常图 GT：Y_∪ = 0。
- 参考：训练时每张查询图从 𝒩 中检索 k 张（排除同一来源原图的裁块，避免近重复参考）；5% 概率改为随机参考，作为鲁棒性正则。

## 5. 损失
记 patch 级目标由像素级 GT 下采样（区域内比例 ≥ 0.25 记为正）。

- L_res = Focal(A_res, Y_∪) + Dice(A_res, Y_∪) + CE(a_res, y_img)。沿用 AdaptCLIP。
- L_exp（解释头的分组交叉熵）：
  - 缺陷像素（Y_∪ = 1）：软目标 y_i ∈ Δ^{13}，在该像素为正的缺陷类上均分（重叠像素 0.5/0.5），其余为 0。L = −Σ_a y_{i,a} log π_{i,a}。
  - 非缺陷像素（异常图的背景与正常图全部）：只约束"不是缺陷"，L = −log(π_{i,0} + μ_i)。不规定是正常还是哪种干扰，让干扰锚点由 CLIP 文本先验自组织。
- L_cls = Focal(A_cls, Y_∪) + Dice(A_cls, Y_∪)。让门控乘积本身校准。
- L_drop（类型 dropout，训练类无关锚点）：每个 batch 以 p = 0.25 随机选一个缺陷类 c*，把该类像素的软目标改为 T_g（类无关）。T_g 由此学到"类型未知的缺陷"，直接服务开放集。推理时不 dropout。
- L_pseudo（干扰伪标签，可选，审计 (b) 方案）：对正常图上 A_res 高响应的 token，用冻结 CLIP 的手写提示零样本打分，若最高的干扰类置信度 ≥ 0.6，则对该 token 施加完整 CE 到该干扰类。权重 λ_p = 0.1。默认关闭，消融开启。
- L_prior（锚点漂移约束）：每个锚点的学习上下文嵌入与其手写提示嵌入的余弦距离，Σ_a (1 − cos(t_a, t_a^{hand}))，权重 λ_r = 1.0。防止干扰锚点学成通用抑制项（对应判别性预测 P2）。
- 总损失：L = L_res + L_exp + λ_1 L_cls + L_drop（已含于 L_exp 的目标替换）+ λ_p L_pseudo + λ_r L_prior，λ_1 = 0.5。
- 交替训练（沿用 AdaptCLIP）：奇数 epoch 更新视觉侧（视觉适配器、P_l、H_res、图像头），冻结文本上下文；偶数 epoch 更新文本上下文，冻结视觉侧。共 20 epoch，lr 1e-3，AdamW，batch 8。

## 6. 可训练参数
视觉适配器（AdaptCLIP 原：两支残差 MLP）、四个 P_l、H_res、图像头、13 × 12 个上下文 token。合计约 3–4 M，骨干 0。

## 7. 推理流程
1. 检索 k = 4 参考 → 四层残差 → A_res, a_res。
2. 四层投影与 13 锚点相似度 → 残差加权邻域池化 → π。
3. M_c、A_cls、A_bin、unknown 图。
4. 阈值 τ_c、τ_bin 在验证集固定后用于所有测试集。

## 8. 与判别性预测的对应
- P1（参考外干扰）：从 𝒩 剔除含某干扰的正常图，检查 A_bin 在该干扰区域的 FPR；对比 IDEAL 式统计擦除（在 r 上做局部 PCA 抑制替换 §3 全部）。
- P2（锚点特异性）：删除 T_u 中一个锚点重训，FPR 增量按审计类别拆分。
- P3（互补性）：在 r 上叠加 NVE 式子空间抑制后再进 §3。
- P4：§2 消融。
- P5：跨数据集主表。

## 9. 已知风险与对应开关
- CLIP patch 局部语义弱：§3.2 池化是对策；若不足，视觉侧换 DINOv2-L/14 做 M1 残差、CLIP 只做 §3（需单独消融骨干增益）。
- 干扰锚点坍缩为通用抑制：L_prior 与 P2 监控。
- 多标签软目标与 softmax 的张力：若 per-class IoU 受损，改为 {正常, 类无关, 7 干扰} 9 路竞争 + 4 个独立 sigmoid 类型头，类型头乘以 ν 门控。

## 10. v0.2：现行实现 v2（RC-HDG，2026-11-03）

与 v0.1 的差别用"改"标出；未提及处沿用 §1–§2（骨干、M1 检索、残差头、图像头的输入）。

### 10.1 锚点（改 §3.1）
- 12 个锚点：T_0 正常、T_1..T_4 缺陷类型、T_5 类无关缺陷、T_6..T_11 干扰（water stain / shadow / moss / patch repair / formwork texture / dirt；graffiti 因 CODEBRIM 中不存在而删除）。
- 不再学上下文 token，不再逐步过文本编码器。每个锚点 t_a = norm(t_a^hand + ε·Δ_a / max(1, ‖Δ_a‖))，t_a^hand 为 4 模板集成的手写提示嵌入，Δ_a ∈ R^768 可学，ε = 0.5。余弦下界 cos(asin ε) = 0.866，所有锚点自由度相同。实测 20 epoch 后全部锚点停在 0.867–0.890，即顶到上限。
- L_ortho = Σ_{u<v, 干扰} max(0, cos(t_u, t_v) − cos(t_u^hand, t_v^hand))，权重 0.1。L_prior 取消（上界已由构造保证）。

### 10.2 相似度与双路池化（改 §3.2）
- 局部相似度 S^loc_{i,a} = cos(P_l F_{l,i}, t_a)/τ 四层平均；区域相似度 S^reg 为 §3.2 的残差加权 5×5 高斯池化（σ = 1.5）。
- 逐锚点可学门 γ_a = sigmoid(g_a)，S̃_{i,a} = γ_a S^loc + (1 − γ_a) S^reg，g 初始化为 0（γ = 0.5）。实测 γ：剥落 0.22、泛碱 0.18、锈蚀 0.33、裂缝 0.59、正常 0.59、干扰 0.62–0.88。

### 10.3 三元竞争与输出（改 §3.3–§3.4）
- π_i = softmax(S̃_i) ∈ Δ^12；ν_i = Σ_{a=1..5} π_{i,a}（缺陷质量），μ_i = Σ_{a≥6} π_{i,a}（非缺陷偏离质量），π_{i,0} 为正常。
- 类型头：p_{i,c} = sigmoid(s_c · (S̃_{i,c} − S̃_{i,0}) + b_c)，c = 1..4，s_c、b_c 可学（初始 1、0）。独立 sigmoid，允许重叠。
- 输出：typed_c = up(p_c)（未门控）；typed_gated_c = typed_c · up(ν)；A_cls = A_res · up(ν)；A_bin = max(A_cls, max_c typed_gated_c)；未知缺陷 = A_cls 高且 max_c p_c 低。μ 图仅作解释与审计。
- 图像头：对四层残差特征 z_l 按 (0.5 + 0.5ν) 逐格加权后做 mean/max 池化 → MLP → 2 类 logits。图像分数 = 0.5·softmax + 0.5·A_bin top-1% 均值。

### 10.4 损失（改 §5）
patch 级目标：缺陷格 = 任一类掩码在格内占比 ≥ 0.25。
- L_res = Focal + Dice(A_res, Y_∪)；L_img = CE；L_cls = Focal + Dice(A_cls, Y_∪)，权重 0.5；L_type = 平均_c Focal + Dice(typed_gated_c, Y_c)，权重 1。
- L_exp（残差条件化分层交叉熵）：
  - 缺陷格：−log ν_i + 组内交叉熵 −Σ_c y_{i,c} log(π_{i,c}/ν_i)/Σy，软目标在同时为正的类上均分；以 p = 0.25 做类型 dropout，被丢弃类的目标改为 T_5。
  - 干净背景格：−log π_{i,0}。
  - 可疑背景格：0.5·(−log μ_i) + 0.5·KL(q_i^zs ‖ π_{i,6..}/μ_i)。q^zs 为冻结 CLIP 投影 patch token 与手写提示（正常 + 6 干扰）的四层平均余弦，减去 200 张训练正常图上的类均值后 softmax(100·)。可疑 = (σ(res_i) > 0.25 且在该图背景残差前 30%，前 2 epoch 不启用) 或 (max_u q^zs_{i,u} ≥ 0.5)。实测可疑格占全部格子约 10%。
  - 无干扰锚点消融（6 锚点）：全部背景格为干净格。
- 总损失 L = L_res + L_img + L_exp + 0.5 L_cls + L_type + 0.1 L_ortho。交替训练同 §5：奇数 epoch 更新头部，偶数 epoch 更新 Δ。20 epoch，AdamW lr 1e-3，batch 1 + 8 步累积（沿用 v0 实现）。

### 10.5 训练数据与特征缓存
- 冻结 CLIP 的四层 patch token（fp16）与全局嵌入预先缓存（`build_feature_cache.py`，训练 + 验证共 35 GB），训练时不做任何图像前向；步速 1.26 → 6–10 步/秒，20 epoch 约 1.5 小时。
- 参考检索、同原图排除、5% 随机参考同 §4。

### 10.6 已知结果与未验证项
- 验证集：I-AUROC 93.0（基线 91.3），P-AP 68.1，P-AUPRO 90.3；Cleaned-Val 94.8 / 75.5 / 92.0；裂缝 P-AP 0.405。
- 干扰锚点 T_6..T_11 在验证集上 argmax 占比 0.1%、μ 均值 0.056，未起作用；A_bin 分数整体偏低（TPR0.8 阈值 0.02），固定阈值指标跨版本不可比。
- 进行中：6 锚点消融与 3 种子（`scripts/queue_v2.sh`）。未做：§9 的分辨率分支（v2b）、P1 / P3 / P4 / P5。
