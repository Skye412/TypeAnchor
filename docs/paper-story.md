# 论文故事线与引言初稿（2026-11-07 初稿，2026-11-08 按 test 划分改写）

目标期刊：Automation in Construction（研究论文）。域内数字取 results.md §2p（CODEBRIM test 划分 809 张，本方法 3 种子均值），跨数据集数字取 §2g、§2l、§2o，机制分析（消融、尺度、参考敏感性）取验证集章节并注明。英文稿段落为初稿，供全文写作沿用；中文部分是故事线与写作依据。

**2026-11-08 改写要点**：主表切到 test 后，"域内对 AdaptCLIP +20 P-AP"缩为 +3.5，"ν 门控有用"失去证据，这两条从主张里撤出；域内主张改为"二元像素精度与全监督 SegFormer-B2 持平、高于全部 CLIP 系方法，匹配召回下的正常图误报面积是全部方法里最低的，并给出可重叠的按类输出"。两个全监督二元方法（WPFormer、MixerCSeg）进入对比表。

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
2. 主效应（域内，CODEBRIM test 809 张，本方法 3 种子均值，§2p）：二元 P-AP 76.8 ± 3.1，与全监督 SegFormer-B2 76.4 持平，高于 AdaptCLIP 基线 73.3（+3.5）、MultiADS 69.8、Bayes-PFL 62.7、AnomalyCLIP 57.0，以及两个全监督二元网络 WPFormer 70.8、MixerCSeg 52.1；I-AUROC 92.0 ± 0.7，基线 92.7。按类 mAP 59.4 对 MultiADS 56.2、SegFormer-B2 60.1。TPR 0.9 时正常图被标面积 4.4%，基线 9.5%、SegFormer-B2 10.0%、MultiADS 12.0%、WPFormer 27.7%，为全部方法最低。验证集上的 +20（§2k）来自小面积缺陷占多数的划分（缺陷像素中位数 6,297 对 test 的 44,114），写进讨论作"划分影响结论"的分析，不作主张。
3. 机制（验证集 §2f、§2h、§2i；test §2p.3）：γ = 0 伤裂缝（验证集 35.7 → 8.2，test 8.3 → 5.2）；v0 的 13 路 softmax 读出裂缝 test 1.9；去残差 test P-AP −3.1（验证集 −9.7），正常图误报验证集约 8 倍、test 1.2 倍；参考数量与选择不敏感；12 对 6 锚点无差异。去 ν 门控在 test 上无可测变化（I-AUROC +0.4，P-AP −0.1），验证集的 −1.1 / −2.8 撤回。test 种子标准差 P-AP 3.1、P-AUPRO 3.6，单种子消融差异在 3 点以内的不作结论。
4. 与全监督对照（§2j、§2l、§2o、§2p）：域内 SegFormer-B2 按类 mAP 60.1 对 59.4、裂缝 24.1 对 10.3、mIoU 50.4 对 40.7，二元 P-AP 76.4 对 76.8；WPFormer 二元 P-AP 70.8、P-AUPRO 78.0。跨域 S2DS mAP SegFormer-B2 32.7 对本方法 46.6，dacl10k 8.6 对 16.1；二元 P-AP WPFormer S2DS 64.4 对本方法 70.9 / MultiADS 71.5，dacl10k 28.4 对 32.8 / 36.2；MixerCSeg 45.6 / 8.6。
5. 跨域的边界（§2o、§2p）：MultiADS S2DS mAP 52.8、dacl10k 18.5 高于本方法；P-AUPRO 本方法 test 73.5 低于 AdaptCLIP 基线 80.4（最高）、MultiADS 78.8、WPFormer 78.0、Bayes-PFL 75.6，S2DS 上 WPFormer 64.2 最高、本方法 41.5 最低；图像级跨域 Bayes-PFL 与 WPFormer 高于本方法。
6. 裂缝的尺度分析（验证集）：滑窗推理 +6.6 但泛碱 −25；1/4 分辨率细节支路 +6.7，不迁移到外部集（§2m、§2n）。test 上所有方法的裂缝 P-AP 都低于 25。
7. 协议：Cleaned-Val 使正常图误报面积从 1.75% 到 0.12%，排序不变；GPU / CPU AUPRO 差 4.8；验证集与 test 的缺陷面积分布差 7 倍，使 AdaptCLIP 基线 P-AP 从 61.8 变到 73.3、本方法从 81.8 变到 76.8（§2d、§2n.3、§2p）。

**中心主张**：在冻结 CLIP 上，以文本锚点为类别接口的多类型分割头（6.6 M 可训练参数）在未接触过的 CODEBRIM test 划分上，二元像素精度与全参数训练的 SegFormer-B2 持平、高于全部 CLIP 系异常检测方法，匹配召回下的正常表面误报面积为全部方法最低，并给出允许重叠的按类掩码；跨数据集上冻结 CLIP 这一路线在像素 P-AP 与按类 mAP 上优于三种全监督分割网络，其中更简单的 MultiADS 优于本方法。有监督头部的域内增益来自对训练域外观的拟合，跨域能力来自冻结骨干与文本对齐本身。

**边界（只写影响解释的）**：裂缝 test P-AP 10.3 对 SegFormer-B2 24.1（验证集 35.7 对 54.5），分辨率补救在验证集只到 42；P-AUPRO 低于 AdaptCLIP 基线、MultiADS、WPFormer、Bayes-PFL；与 AdaptCLIP 基线的域内差距 3.5 P-AP，I-AUROC 不高于基线；跨域结果单种子，随训练长度摆动 2 至 5 点，几个点以内的差异不作结论；WPFormer、MixerCSeg 的检查点来自旧项目，按验证集选轮。

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

表格规划（域内表全部用 test 划分，results.md §2p）：
- 表 1 域内二元（test 809 张）：AdaptCLIP、AnomalyCLIP、Bayes-PFL、MultiADS、SegFormer-B2、WPFormer、MixerCSeg、本方法（3 种子均值 ± 标准差）；参数量、I-AUROC、P-AUROC、P-AP、P-F1max、P-AUPRO、TPR 0.8 / 0.9 时正常图被标面积。
- 表 2 按类（test）：MultiADS、SegFormer-B2、本方法；mAP、mIoU、四类 P-AP。
- 表 3 消融（test seed 10，附 3 种子标准差；验证集数字放附表）：完整、γ = 0、γ = 1、去 ν 门控、去残差、12 锚点、v0。
- 表 4 跨数据集（S2DS test、dacl10k）：八个方法；I-AUROC、P-AP、P-AUPRO、mAP、裂缝 P-AP。
- 表 5 裂缝尺度（验证集，分析实验）：整图、滑窗、滑窗混合、细节支路（只训）、细节支路（联合）、多训 10 轮对照。
- 附表：验证集原集 / Cleaned-Val 二元表（§2k）与两个划分的缺陷分布，支撑讨论里"划分影响结论"一段。

## 3. 主张与证据对照

| 主张 | 证据 | 强度 |
|---|---|---|
| 域内二元 P-AP 与 SegFormer-B2 持平、高于全部 CLIP 系方法 | §2p.1，3 种子 76.8 ± 3.1 对 76.4 / 73.3 / 69.8 / 62.7 / 57.0 | 对 CLIP 系方法强（差距 ≥ 3.5，对基线弱）；对 SegFormer "持平" |
| 匹配召回下正常图误报面积最低 | §2p.1 TPR 0.9：4.4% 对 9.5% / 10.0% / 12.0% / 27.7%，3 种子 4.3 至 4.6 | 强 |
| 按类 mAP 高于 MultiADS、略低于 SegFormer-B2 | §2p.2，59.4 对 56.2 / 60.1 | 中（MultiADS 单种子） |
| 局部相似度必须保留 | γ = 0 裂缝 35.7 → 8.2（§2f），test 8.3 → 5.2（§2p.3）；v0 裂缝 0.07 / 1.9 | 强 |
| 残差分支有用、参考不敏感 | §2i −9.7（验证集），§2p.3 −3.1（test），§2h 差 0.1 至 0.3 | 中弱（test 差异在种子标准差内） |
| ν 门控有用 | §2f −1.1 / −2.8；§2p.3 +0.4 / −0.1 | 撤回，不作主张 |
| 冻结 CLIP 方法跨域 P-AP 与 mAP 优于全监督分割 | §2j、§2l、§2o，两个外部集一致，mAP 差 14 点；WPFormer P-AP 低 6 至 7 点 | 中（P-AUPRO 与图像级不成立） |
| 本方法跨域不如 MultiADS | §2o，S2DS mAP −6.2，dacl10k −2.4 | S2DS 中，dacl10k 弱（在摆动范围内） |
| 分辨率是裂缝瓶颈之一但不是全部 | §2m、§2n | 中 |
| P-AUPRO 低于 AdaptCLIP 基线、MultiADS、WPFormer、Bayes-PFL | §2p.1（基线 80.4，本方法 73.5 ± 3.6）、§2o 同口径表 | 强 |
| 评测划分改变结论 | §2p：基线 61.8 → 73.3，本方法 81.8 → 76.8，缺陷像素中位数差 7 倍 | 强 |

## 4. 英文初稿

### Title

Text-Anchored Multi-Type Defect Segmentation on a Frozen Vision-Language Model for Concrete Bridge Inspection

备选：Where Do the Gains Come From? Text-Anchored Multi-Type Defect Segmentation on Frozen CLIP for Bridge Inspection

### Abstract

Bridge inspection turns images of concrete surfaces into repair decisions, and the decision depends on the defect type: cracks are measured by width and orientation, spalling and corrosion by exposed area, efflorescence by the moisture path behind it. A pixel map that only separates damaged from intact surface is therefore not enough, and the types overlap on the same surface. Fully supervised segmentation networks deliver type-specific maps but transfer poorly to images from another agency, while CLIP-based anomaly detectors transfer better but return a single binary map. We treat the text embeddings of a frozen CLIP ViT-L/14 as a class interface for a light supervised head rather than as an anomaly score. Each defect type receives one text anchor; an independent sigmoid head reads the similarity margin between the type anchor and the intact-surface anchor, so types may overlap, and a learned per-anchor mixture of patch-level and neighbourhood similarity keeps thin cracks visible while large defects use regional context. The residual between the query and one intact reference image gates a class-agnostic defect channel and the image-level score. Trained on 2,861 CODEBRIM tiles, 917 of them with per-type masks, the head has 6.6 M trainable parameters. On the held-out CODEBRIM test split of 809 tiles its binary pixel average precision is 76.8 over three seeds, level with a fully trained SegFormer-B2 at 76.4 and above AdaptCLIP, MultiADS, Bayes-PFL and AnomalyCLIP trained on the same tiles, which reach 73.3, 69.8, 62.7 and 57.0. At 90% pixel recall it marks 4.4% of the intact surface, against 9.5% for AdaptCLIP, 10.0% for SegFormer-B2 and 12.0% for MultiADS, and it returns per-type masks with mean average precision 59.4 against 56.2 for MultiADS, the only compared method with type outputs. On S2DS and dacl10k, without target data, the frozen-CLIP methods exceed three fully trained segmentation networks in pixel average precision and per-type mean average precision, and the simpler MultiADS exceeds ours. The in-domain accuracy of a supervised head is accuracy on the training domain's appearance, and transfer comes from the frozen backbone and its text alignment. We release the per-type masks and an evaluation protocol with a cleaned validation split, matched-recall false-alarm measurement, two external test sets and a reconciled P-AUPRO, and we show that moving from a validation split dominated by small defects to a test split dominated by large ones changes the margin over AdaptCLIP from 20 points to 3.5.

（摘要约 340 词，期刊通常限 250 至 300，定稿时按刊物要求压缩。数据与代码公开的句子以用户确认 CODEBRIM 许可为前提。）

### 1. Introduction

Visual inspection of concrete bridges produces images in which several kinds of damage coexist: cracks as narrow discontinuities, spalling as broken-off regions that expose aggregate or reinforcement, corrosion as rust staining around exposed steel, and efflorescence as white deposits left by water moving through the concrete. Maintenance acts on these types differently. A crack is assessed by its width and orientation, spalling and corrosion by the exposed area and the condition of the reinforcement, and efflorescence as evidence of a leakage path. The pixel map that an inspection system hands to an engineer therefore needs to say which type is where, and it needs to allow overlap, because corrosion appears inside spalled regions and efflorescence runs across cracks. The map also needs to survive a change of image collection. Agencies photograph different structures with different cameras and lighting, and pixel-level annotation of every new collection is the most expensive step in deploying such a system.

Two families of methods meet parts of this requirement. Fully supervised segmentation networks, from general architectures such as SegFormer to crack-specific designs, give type-specific masks and high accuracy on the collection they were trained on. On a different collection their accuracy drops, and they are silent about any damage outside the training classes. Anomaly detection on frozen vision-language models moves in the opposite direction. AnomalyCLIP, AdaptCLIP and Bayes-PFL keep the CLIP encoders fixed, learn a few million parameters that align patch features with normal and abnormal text, and transfer across industrial domains with zero or one normal image. Their output is a single binary anomaly map. MultiADS extends this line with one text prompt per defect type and a pixel-level softmax over the types, which produces type maps but forces each pixel to one type and was designed on industrial objects photographed under controlled conditions.

Three obstacles separate these families from the inspection requirement. The class interface is the first. A normal-versus-abnormal formulation has no place for types, and a softmax over types has no place for overlap. The second is scale. At the 518-pixel input of CLIP ViT-L/14 the patch grid is 37 by 37, about 14 pixels per cell, and cracks are often thinner than one cell. Pooling similarity over a neighbourhood, which stabilises large defects, erases cracks: in our ablation on the validation split, replacing patch-level similarity by 5 by 5 regional pooling drops crack average precision from 35.7 to 8.2, while spalling and efflorescence are unaffected. Scale requirements differ by type. The third is measurement. Public civil-engineering datasets store flattened single-label masks in which a priority rule removes overlap, validation sets labelled as intact contain unlabelled defects that inflate false-alarm measurements, and the two common implementations of the region-overlap metric P-AUPRO disagree by several points on identical predictions. Under these conditions it is hard to tell whether a method that looks better across datasets is better.

We address the interface and scale obstacles with one design decision: the text anchors of a frozen CLIP are used as a class interface for a light supervised head, not as an anomaly detector. Six anchors represent intact surface, the four defect types and a class-agnostic damaged surface. For each anchor the similarity to the projected patch tokens is computed at patch level and over a residual-weighted neighbourhood, and a learned per-anchor weight mixes the two, so the crack anchor can stay local while the spalling and efflorescence anchors use context. Four independent sigmoid heads read the margin between each type anchor and the intact anchor; a pixel may be positive for several types. The residual between the query tokens and the nearest tokens of a single intact reference image is kept, but as a gate: it scales a class-agnostic defect channel and the image-level head, suppressing responses on intact texture and catching damage outside the four types. The head has 6.6 M trainable parameters and needs one arbitrary intact image at inference.

We trained the head on 2,861 CODEBRIM training tiles, 917 of which carry overlapping per-type masks that we annotated, selected every design choice on the validation split, and report on the test split of 809 tiles that no choice ever touched, and, without any target data, on S2DS and on a strict four-type subset of dacl10k. On the test split the head reaches a binary pixel average precision of 76.8 over three seeds, level with a fully trained SegFormer-B2 at 76.4 and above AdaptCLIP at 73.3, MultiADS at 69.8, Bayes-PFL at 62.7 and AnomalyCLIP at 57.0, all trained with their official code on the same tiles, and above two fully supervised binary networks, WPFormer at 70.8 and MixerCSeg at 52.1. Image-level AUROC is 92.0 against 92.7 for AdaptCLIP. At 90% pixel recall the head marks 4.4% of the intact surface, less than half of AdaptCLIP, SegFormer-B2 and MultiADS. Its per-type mean average precision is 59.4 against 56.2 for MultiADS and 60.1 for SegFormer-B2; on cracks SegFormer-B2 keeps a lead of 14 points.

The cross-dataset results separate the two sources of performance. On S2DS and dacl10k every frozen-CLIP method segments the four types better than SegFormer-B2, by 14 points of mean average precision on S2DS for ours, and reaches a higher pixel average precision than WPFormer, while MultiADS, with 3.1 M linear parameters and no residual channel, is better than ours on both external sets. Fine-tuning the final model for ten more epochs moves the external numbers by two to five points in inconsistent directions. The evaluation split matters as much as the method: on the validation split, where the median defect covers 6,300 pixels, the head is 20 points of pixel average precision ahead of AdaptCLIP; on the test split, where it covers 44,000, the margin is 3.5. The in-domain accuracy of a supervised head is accuracy on the training domain's appearance; what transfers is the frozen backbone and its alignment with text. Resolution explains part of the crack deficit: sliding-window inference at twice the resolution and a quarter-resolution detail branch each add about seven points of crack average precision on the validation split, and neither transfers.

The contributions are the following. We propose a text-anchored multi-type segmentation head for frozen CLIP, with independent per-type readouts on anchor margins, a per-anchor local-regional similarity mixture, and a residual-gated class-agnostic channel, and we show through ablation which part each component carries. We provide overlapping per-type pixel masks for CODEBRIM tiles together with an evaluation protocol for bridge inspection: per-type multi-label metrics, a cleaned validation split, false-alarm area at matched recall, two external test sets, and a reconciled P-AUPRO. We report, on the same data and protocol, how CLIP-based anomaly detectors, their multi-type extension and a fully supervised network compare in-domain and across datasets, and we trace the in-domain gain of supervision and the cross-dataset advantage of frozen backbones to different causes.

## 5. 写作前待用户确认的决定

1. 标题与定位：按 §4 的主标题（方法 + 发现）写，还是把"增益来源"做成主标题。
2. CODEBRIM 裁块与自标注掩码能否随论文公开：影响摘要与贡献里的"release"句子。
3. 对比表是否保留 Bayes-PFL（检查点来自旧项目，种子与选轮方式不同，已在 results.md §2o 注明）。
4. 与 ProtoBridge 稿件的关系：两稿共用 CODEBRIM / S2DS 数据与标注，本稿需在数据部分引用或说明标注来源，避免被视为重复发表。用户已决定 ProtoBridge 不进入对比表。
5. （2026-11-08 新增）主表切到 test 后对 AdaptCLIP 的域内优势只有 3.5 P-AP、I-AUROC 不占优：是否接受上面改写后的中心主张（与全监督二元精度持平、误报最低、按类输出），还是补做能拉开差距的实验（用户此前已决定实验停止）。
6. （2026-11-08 新增）WPFormer、MixerCSeg 的检查点来自旧项目、按验证集选轮且 MixerCSeg 域内偏弱：是否保留两者，或只保留 WPFormer。
