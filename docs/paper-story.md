# 论文故事线与引言初稿（2026-11-07）

目标期刊：Automation in Construction（研究论文）。全部数字取自 results.md 修正后的章节（§2e 至 §2o），单种子处已注明。英文稿段落为初稿，供全文写作沿用；中文部分是故事线与写作依据。

## 1. 故事线

**科学起点**：桥梁巡检产出的像素级缺陷图要进入维修决策，而维修措施按缺陷类型区分：裂缝要量宽度与走向，剥落与露筋锈蚀要估面积与深度，泛碱指向渗水路径。一张只分"有 / 无缺陷"的图不够用；同一表面上剥落里露出锈蚀、泛碱覆盖裂缝也很常见，类型之间会重叠。另一方面，每个管养单位的影像来自不同的桥、相机与光照，逐单位标注像素掩码的代价高，训练好的模型要能在另一批影像上继续用。

**领域现状**：全监督分割网络（SegFormer 一类通用网络，SCSegamba、CrackSSM 一类裂缝专用网络）在训练域内精度高，但类别封闭、跨影像集合时掉得快。基于 CLIP 的异常检测（AnomalyCLIP、AdaptCLIP、Bayes-PFL）靠冻结骨干与文本对齐取得跨域能力，但输出是二元异常图，没有类型；MultiADS 用多类型提示做像素 softmax，第一次把类型带进这条路线，但 softmax 互斥，且仍是工业数据上的设计。

**知识缺口与根因**：
1. 类型接口。异常检测的"正常 / 异常"二元框架给不出类型，也给不出重叠；多类 softmax 在重叠处只能选一个。
2. 尺度。CLIP ViT-L/14 在 518 输入下是 37×37 网格，每格约 14 像素；裂缝宽度常不足一格。区域池化或邻域平均会把裂缝抹掉（γ = 0 使裂缝 P-AP 从 35.7 掉到 8.2），而大面积类别（剥落、泛碱）又需要区域上下文。尺度需求按类别不同。
3. 评测。土木数据集多用拍平的单标签掩码，重叠被优先级规则抹去；正常集里混有未标注缺陷会让误报指标失真；P-AUPRO 的两种常用实现在同一预测上差 4.8 点。这些让"跨域是否真的更好"难以判断。

**核心洞见**：把文本锚点当作类别接口，而不是当作异常判别器。每个缺陷类型一个文本锚点，类型概率由"该类型锚点与正常锚点的相似度差"经独立 sigmoid 读出，允许重叠；相似度在局部与区域两条路上按锚点学一个混合权重，让细裂缝保留局部证据、大面积类别用区域上下文。与正常混凝土 patch 的残差距离不再做"异常分"，而是门控一条类无关缺陷通道与图像级头，用来压正常表面的误报并接住四类之外的缺陷。

**机制**（按洞见的顺序）：
- 冻结 CLIP ViT-L/14，取 6 / 12 / 18 / 24 层 patch token；轻量视觉适配器与逐层线性投影把 token 投到文本空间（约 6.6 M 可训练参数，骨干 0）。
- 六个文本锚点：正常、裂缝、锈蚀、剥落、泛碱、类无关缺陷。锚点 = 手写提示嵌入加一个有界可学偏移。
- 逐锚点局部 / 区域相似度混合（γ_a），区域相似度为残差加权的 5×5 高斯池化。
- 四个独立 sigmoid 类型头读"类型锚点减正常锚点"的差。
- 正常参考残差：查询 token 与一张正常图最近邻 token 的逐维差，经残差头得到 ν（缺陷质量）；ν 门控类无关通道与图像头。推理只需 1 张任意正常图。
- 损失：二元 focal + dice、图像级交叉熵、分组交叉熵（缺陷格 −log ν 加组内类型交叉熵，背景格 −log π_0）、类型损失；视觉侧与锚点偏移交替训练。

**证据梯**（全部已有结果）：
1. 现象：v0 的 13 路 softmax 加区域池化下裂缝 P-AP 0.07；γ = 0 消融复现同一失效（§2、§2f）。
2. 主效应（域内，CODEBRIM 验证集）：对 AdaptCLIP 基线二元 P-AP 61.8 → 81.8，I-AUROC 91.3 → 92.1；对 AnomalyCLIP、Bayes-PFL、MultiADS 分别 +51、+19、+25；按类 mAP 72.6 对 MultiADS 64.6（§2j、§2o）。3 种子均值 P-AP 79.9、I-AUROC 92.3（§2k）。
3. 机制：γ = 0 伤裂缝；去 ν 门控 I-AUROC −1.1、mAP −2.8；去残差 P-AP −9.7、正常图误报约 8 倍；参考数量与选择不敏感；12 对 6 锚点三种子无差异（§2e、§2f、§2h、§2i）。
4. 与全监督对照：SegFormer-B2 域内 mAP 81.5 对 72.6、裂缝 54.5 对 35.7；跨域 S2DS mAP 32.7 对 46.6，dacl10k 8.6 对 16.1（§2j、§2l）。
5. 跨域的边界：MultiADS 在 S2DS mAP 52.8、dacl10k 18.5，高于本方法；P-AUPRO 本方法在三套数据上都低于 AdaptCLIP 基线（§2o、§2n.3）。
6. 裂缝的尺度分析：滑窗推理 +6.6 但泛碱 −25；1/4 分辨率细节支路 +6.7，不迁移到外部集（§2m、§2n）。
7. 协议：Cleaned-Val 使正常图误报面积从 1.75% 到 0.12%，排序不变；GPU / CPU AUPRO 差 4.8（§2d、§2n.3）。

**中心主张**：在冻结 CLIP 上，以文本锚点为类别接口的多类型分割头在训练域内把二元像素 P-AP 提高 20 个点并给出可重叠的按类输出；这部分增益来自对训练域外观的拟合，不随模型迁移，而跨数据集能力来自冻结骨干与文本对齐本身，所以冻结 CLIP 方法整体优于全监督分割，而更简单的 MultiADS 优于本方法。

**边界（只写影响解释的）**：裂缝 P-AP 35.7，比 SegFormer-B2 低 19 点，分辨率补救只到 42；P-AUPRO 低于 AdaptCLIP 基线；跨域结果单种子，且随训练长度摆动 2 至 5 点，几个点以内的差异不作结论。

**贡献类型**：新模块（类型头 + 残差门控通道）、新实证发现（域内增益与跨域能力的来源分离）、新评测协议。不主张新任务或新数据集。

## 2. 章节安排

| 章节 | 任务 | 主要材料 |
|---|---|---|
| 1 Introduction | 起点、缺口、洞见、贡献 | 本文件 §4 |
| 2 Related work | 2.1 桥梁缺陷分割（全监督、裂缝专用）；2.2 CLIP 系异常检测与多类型扩展；2.3 土木数据集与评测 | idea-review.md 的先行工作表，参考文献目录 |
| 3 Method | 3.1 问题设定与记号；3.2 文本锚点与投影；3.3 局部 / 区域相似度混合；3.4 类型头；3.5 正常参考残差与 ν 门控通道；3.6 训练目标 | model-spec.md §10.1 至 §10.7 |
| 4 Experimental setup | 数据（CODEBRIM 裁块与标注、S2DS test、dacl10k 严格子集）、对比方法与训练设置、指标（二元、按类多标签、Cleaned-Val、匹配 TPR 误报、AUPRO 口径） | results.md §2g、§2l、§2k、§2n.3 |
| 5 Results | 5.1 域内对 CLIP 系方法（表 1）；5.2 按类分割与全监督对照（表 2）；5.3 消融（表 3）；5.4 跨数据集（表 4）；5.5 裂缝与尺度（表 5）；5.6 定性图 | §2o、§2j、§2f、§2i、§2l、§2m、§2n |
| 6 Discussion | 增益来源的分离；对巡检应用的含义（域内部署与跨单位复用的不同选择）；P-AUPRO 与评测口径 | §2o、§2n.1、§2n.3 |
| 7 Conclusion | 中心主张 | |

表格规划：
- 表 1 域内二元：AdaptCLIP、AnomalyCLIP、Bayes-PFL、MultiADS、SegFormer-B2、本方法；原集 / Cleaned-Val；I-AUROC、P-AUROC、P-AP、P-F1max、P-AUPRO（GPU）、参数量。
- 表 2 按类：MultiADS、SegFormer-B2、本方法；mAP、mIoU@0.3、四类 P-AP。
- 表 3 消融（seed 10，附 3 种子标准差）：完整、γ = 0、γ = 1、去 ν 门控、去残差、12 锚点、1 张随机参考。
- 表 4 跨数据集（S2DS test、dacl10k）：六个方法；I-AUROC、P-AP、P-AUPRO、mAP、裂缝 P-AP。
- 表 5 裂缝尺度：整图、滑窗、滑窗混合、细节支路（只训）、细节支路（联合）、多训 10 轮对照。

## 3. 主张与证据对照

| 主张 | 证据 | 强度 |
|---|---|---|
| 域内二元 P-AP 对 AdaptCLIP 基线 +20 | §2k 修正表，3 种子均值 79.9 对 61.8 | 强 |
| 域内对 AnomalyCLIP、Bayes-PFL、MultiADS 全面更好 | §2o 表，单种子 | 中（差距远大于种子方差） |
| 局部相似度必须保留 | γ = 0 裂缝 35.7 → 8.2（§2f） | 强 |
| 残差分支有用、参考不敏感 | §2i −9.7，§2h 差 0.1 至 0.3 | 中（单种子，但幅度大） |
| ν 门控有用 | §2f −1.1 / −2.8 | 中弱（单种子，超过图像级标准差） |
| 冻结 CLIP 方法跨域优于 SegFormer-B2 | §2j、§2l，两个外部集一致，差距 14 点 | 中 |
| 本方法跨域不如 MultiADS | §2o，S2DS mAP −6.2，dacl10k −2.4 | S2DS 中，dacl10k 弱（在摆动范围内） |
| 分辨率是裂缝瓶颈之一但不是全部 | §2m、§2n | 中 |
| P-AUPRO 低于基线 | §2n.3 同口径表 | 强 |

## 4. 英文初稿

### Title

Text-Anchored Multi-Type Defect Segmentation on a Frozen Vision-Language Model for Concrete Bridge Inspection

备选：Where Do the Gains Come From? Text-Anchored Multi-Type Defect Segmentation on Frozen CLIP for Bridge Inspection

### Abstract

Bridge inspection turns images of concrete surfaces into repair decisions, and the decision depends on the defect type: cracks are measured by width and orientation, spalling and corrosion by exposed area, efflorescence by the moisture path behind it. A pixel map that only separates damaged from intact surface is therefore not enough, and the types overlap on the same surface. Fully supervised segmentation networks deliver type-specific maps but transfer poorly to images from another agency, while CLIP-based anomaly detectors transfer better but return a single binary map. We treat the text embeddings of a frozen CLIP ViT-L/14 as a class interface for a light supervised head rather than as an anomaly score. Each defect type receives one text anchor; an independent sigmoid head reads the similarity margin between the type anchor and the intact-surface anchor, so types may overlap, and a learned per-anchor mixture of patch-level and neighbourhood similarity keeps thin cracks visible while large defects use regional context. The residual between the query and one intact reference image gates a class-agnostic defect channel and the image-level score. Trained on 2,861 CODEBRIM tiles, 917 of them with per-type masks, the head has 6.6 M trainable parameters and raises pixel average precision from 61.8 to 81.8 over the AdaptCLIP baseline, with per-type mean average precision 72.6 against 64.6 for MultiADS, the only compared method with type outputs. The same experiments locate the source of the gain: on S2DS and dacl10k, trained without target data, every frozen-CLIP method outperforms a fully trained SegFormer-B2 on per-type segmentation, and the simpler MultiADS outperforms ours. The in-domain gain comes from fitting the training domain's appearance, and transfer comes from the frozen backbone and its text alignment. We release the per-type masks, the evaluation protocol with a cleaned validation split and matched-recall false-alarm measurement, and a comparison of two P-AUPRO implementations that differ by 4.8 points on identical predictions.

（摘要约 330 词，期刊通常限 250 至 300，定稿时按刊物要求压缩。数据与代码公开的句子以用户确认 CODEBRIM 许可为前提。）

### 1. Introduction

Visual inspection of concrete bridges produces images in which several kinds of damage coexist: cracks as narrow discontinuities, spalling as broken-off regions that expose aggregate or reinforcement, corrosion as rust staining around exposed steel, and efflorescence as white deposits left by water moving through the concrete. Maintenance acts on these types differently. A crack is assessed by its width and orientation, spalling and corrosion by the exposed area and the condition of the reinforcement, and efflorescence as evidence of a leakage path. The pixel map that an inspection system hands to an engineer therefore needs to say which type is where, and it needs to allow overlap, because corrosion appears inside spalled regions and efflorescence runs across cracks. The map also needs to survive a change of image collection. Agencies photograph different structures with different cameras and lighting, and pixel-level annotation of every new collection is the most expensive step in deploying such a system.

Two families of methods meet parts of this requirement. Fully supervised segmentation networks, from general architectures such as SegFormer to crack-specific designs, give type-specific masks and high accuracy on the collection they were trained on. On a different collection their accuracy drops, and they are silent about any damage outside the training classes. Anomaly detection on frozen vision-language models moves in the opposite direction. AnomalyCLIP, AdaptCLIP and Bayes-PFL keep the CLIP encoders fixed, learn a few million parameters that align patch features with normal and abnormal text, and transfer across industrial domains with zero or one normal image. Their output is a single binary anomaly map. MultiADS extends this line with one text prompt per defect type and a pixel-level softmax over the types, which produces type maps but forces each pixel to one type and was designed on industrial objects photographed under controlled conditions.

Three obstacles separate these families from the inspection requirement. The class interface is the first. A normal-versus-abnormal formulation has no place for types, and a softmax over types has no place for overlap. The second is scale. At the 518-pixel input of CLIP ViT-L/14 the patch grid is 37 by 37, about 14 pixels per cell, and cracks are often thinner than one cell. Pooling similarity over a neighbourhood, which stabilises large defects, erases cracks: in our ablation, replacing patch-level similarity by 5 by 5 regional pooling drops crack average precision from 35.7 to 8.2, while spalling and efflorescence are unaffected. Scale requirements differ by type. The third is measurement. Public civil-engineering datasets store flattened single-label masks in which a priority rule removes overlap, validation sets labelled as intact contain unlabelled defects that inflate false-alarm measurements, and the two common implementations of the region-overlap metric P-AUPRO disagree by several points on identical predictions. Under these conditions it is hard to tell whether a method that looks better across datasets is better.

We address the interface and scale obstacles with one design decision: the text anchors of a frozen CLIP are used as a class interface for a light supervised head, not as an anomaly detector. Six anchors represent intact surface, the four defect types and a class-agnostic damaged surface. For each anchor the similarity to the projected patch tokens is computed at patch level and over a residual-weighted neighbourhood, and a learned per-anchor weight mixes the two, so the crack anchor can stay local while the spalling and efflorescence anchors use context. Four independent sigmoid heads read the margin between each type anchor and the intact anchor; a pixel may be positive for several types. The residual between the query tokens and the nearest tokens of a single intact reference image is kept, but as a gate: it scales a class-agnostic defect channel and the image-level head, suppressing responses on intact texture and catching damage outside the four types. The head has 6.6 M trainable parameters and needs one arbitrary intact image at inference.

We trained the head on 2,861 CODEBRIM training tiles, 917 of which carry overlapping per-type masks that we annotated, and evaluated it on the CODEBRIM validation split and, without any target data, on S2DS and on a strict four-type subset of dacl10k. Against AdaptCLIP trained on the same tiles, binary pixel average precision rises from 61.8 to 81.8 and image AUROC from 91.3 to 92.1. Against AnomalyCLIP, Bayes-PFL and MultiADS trained with their official code on the same tiles, the head is ahead by 51, 19 and 25 points of pixel average precision, and its per-type mean average precision is 72.6 against 64.6 for MultiADS. A fully trained SegFormer-B2 remains more accurate in-domain, by 8.9 points of per-type mean average precision and 19 points on cracks.

The cross-dataset results separate the two sources of performance. On S2DS and dacl10k every frozen-CLIP method segments the four types better than SegFormer-B2, by 14 points of mean average precision on S2DS for ours, and MultiADS, with 3.1 M linear parameters and no residual channel, is better than ours on both external sets. Fine-tuning the final model for ten more epochs moves the external numbers by two to five points in inconsistent directions. The in-domain gain of a supervised head is a gain on the training domain's appearance; what transfers is the frozen backbone and its alignment with text. Resolution explains part of the remaining crack deficit: sliding-window inference at twice the resolution and a quarter-resolution detail branch each add about seven points of crack average precision in-domain, and neither transfers.

The contributions are the following. We propose a text-anchored multi-type segmentation head for frozen CLIP, with independent per-type readouts on anchor margins, a per-anchor local-regional similarity mixture, and a residual-gated class-agnostic channel, and we show through ablation which part each component carries. We provide overlapping per-type pixel masks for CODEBRIM tiles together with an evaluation protocol for bridge inspection: per-type multi-label metrics, a cleaned validation split, false-alarm area at matched recall, two external test sets, and a reconciled P-AUPRO. We report, on the same data and protocol, how CLIP-based anomaly detectors, their multi-type extension and a fully supervised network compare in-domain and across datasets, and we trace the in-domain gain of supervision and the cross-dataset advantage of frozen backbones to different causes.

## 5. 写作前待用户确认的决定

1. 标题与定位：按 §4 的主标题（方法 + 发现）写，还是把"增益来源"做成主标题。
2. CODEBRIM 裁块与自标注掩码能否随论文公开：影响摘要与贡献里的"release"句子。
3. 对比表是否保留 Bayes-PFL（检查点来自旧项目，种子与选轮方式不同，已在 results.md §2o 注明）。
4. 与 ProtoBridge 稿件的关系：两稿共用 CODEBRIM / S2DS 数据与标注，本稿需在数据部分引用或说明标注来源，避免被视为重复发表。
