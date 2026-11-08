# 论文故事线（2026-11-08 第二版，按用户确认的中心主张重写）

目标期刊：Automation in Construction（研究论文）。域内数字取 results.md §2p（CODEBRIM test 划分 809 张，本方法为 3 种子均值 ± 标准差），跨数据集数字取 §2g、§2l、§2o，机制分析（消融、尺度、参考敏感性）取验证集章节并在文中注明。对比方法：AdaptCLIP、AnomalyCLIP、Bayes-PFL、MultiADS（冻结 CLIP 路线），SegFormer-B2、WPFormer（全监督分割）。MixerCSeg 的结果保留在 results.md 作记录，不进论文（用户 2026-11-08 决定）。

## 0. 题目与命名（已定）

**题目**：TypeAnchor: Text-Anchored Multi-Type Defect Segmentation on a Frozen Vision-Language Model for Concrete Bridge Inspection

备选（若编辑要求题目体现发现）：Text Anchors as a Class Interface: Multi-Type Concrete Defect Segmentation on Frozen CLIP and Where Its Accuracy Comes From

**方法名**：TypeAnchor。含义是"文本锚点作为类型接口"，不含 anomaly、nuisance、adapt 等词。全文用这一个名字指代整个分割头。

**三个模块**（名字对应 model-spec.md §10.1 至 §10.7 的实现；全文一名一物）：

| 模块 | 英文名与缩写 | 对应实现 | 一句话 |
|---|---|---|---|
| 锚点差读出 | Anchor Margin Readout（AMR） | 4 路独立 sigmoid 类型头，输入为"类型锚点相似度减正常锚点相似度" | 类型概率由锚点差读出，互不排斥，允许重叠 |
| 局部与区域相似度混合 | Local–Regional Similarity Mixture（LRM） | 逐锚点可学权重 γ_a，混合 patch 级相似度与残差加权 5×5 区域相似度 | 裂缝锚点保留局部证据，大面积类别用区域上下文 |
| 参考残差门 | Reference-Residual Gate（RRG） | 查询 token 与 1 张正常参考图最近邻 token 的逐维残差经残差头得 ν，门控类无关缺陷通道与图像级头 | 用正常表面的外观压误报，接住四类之外的缺陷 |

其余名词固定为：text anchor（文本锚点，共 6 个：intact、crack、corrosion、spalling、efflorescence、generic defect）、intact anchor（正常锚点，不用 normal）、type head、defect mass ν、intact reference（正常参考图）、Cleaned-Val、matched-recall false-alarm area（匹配召回误报面积）。

## 1. 故事线

**科学起点**：桥梁巡检产出的像素级缺陷图要进入维修决策，而维修措施按缺陷类型区分：裂缝量宽度与走向，剥落与露筋锈蚀估面积与深度，泛碱指向渗水路径。一张只分"有 / 无缺陷"的图不够用；同一表面上剥落里露出锈蚀、泛碱覆盖裂缝也常见，类型会重叠。每个管养单位的影像来自不同的桥、相机与光照，逐单位标注像素掩码代价高，模型要能在另一批影像上继续用。

**领域现状**：全监督分割网络（SegFormer 一类通用网络，WPFormer 一类面向表面缺陷的查询式 Transformer，SCSegamba、CrackSSM 一类裂缝专用网络）在训练域内精度高，但类别封闭，跨影像集合时掉得快。冻结 CLIP 的异常检测（AnomalyCLIP、AdaptCLIP、Bayes-PFL）靠冻结骨干与文本对齐取得跨域能力，输出是一张二元异常图，没有类型；MultiADS 用多类型提示做像素 softmax，第一次把类型带进这条路线，但 softmax 互斥，且设计与验证都在工业数据上。

**知识缺口与根因**：
1. 类型接口。"正常 / 异常"二元框架给不出类型，也给不出重叠；多类 softmax 在重叠处只能选一个。
2. 尺度。CLIP ViT-L/14 在 518 输入下是 37×37 网格，每格约 14 像素，裂缝宽度常不足一格。区域池化稳定大面积类别，却把裂缝抹掉（验证集上纯区域池化使裂缝 P-AP 从 35.7 掉到 8.2）。尺度需求按类别不同。
3. 评测。土木数据集多用拍平的单标签掩码，重叠被优先级规则抹去；正常集里混有未标注缺陷，误报指标失真；P-AUPRO 的两种常用实现在同一预测上差 4.8 点；验证集与测试集的缺陷面积分布差 7 倍，同一方法对基线的差距从 20 点变成 3.5 点。这些使"哪种方法更好、好在哪"难以判断。

**核心洞见**：把文本锚点当作类别接口，而不是当作异常判别器。每个缺陷类型一个文本锚点，类型概率由"该类型锚点与正常锚点的相似度差"经独立 sigmoid 读出，允许重叠；相似度在局部与区域两条路上按锚点学一个混合权重，让细裂缝保留局部证据、大面积类别用区域上下文。与正常表面 patch 的残差不再做异常分，而是门控一条类无关缺陷通道与图像级头，压正常表面的误报并接住四类之外的缺陷。

**机制**（TypeAnchor，按洞见的顺序）：
- 冻结 CLIP ViT-L/14，取 6 / 12 / 18 / 24 层 patch token；轻量视觉适配器与逐层线性投影把 token 投到文本空间（6.6 M 可训练参数，骨干 0）。
- 六个文本锚点：intact、crack、corrosion、spalling、efflorescence、generic defect。锚点 = 手写提示嵌入加一个有界可学偏移。
- LRM：逐锚点局部 / 区域相似度混合，区域相似度为残差加权的 5×5 高斯池化。
- AMR：四个独立 sigmoid 类型头读"类型锚点减正常锚点"的差。
- RRG：查询 token 与 1 张正常参考图最近邻 token 的逐维残差，经残差头得 ν；ν 门控类无关通道与图像头。推理只需 1 张任意正常图。
- 损失：二元 focal + dice、图像级交叉熵、分组交叉熵（缺陷格 −log ν 加组内类型交叉熵，背景格 −log π_0）、类型损失；视觉侧与锚点偏移交替训练。

**证据梯**（全部为已有结果）：
1. 现象：v0 的 13 路 softmax 加区域池化下裂缝 P-AP 验证集 0.07、test 1.9；γ = 0 消融复现同一失效（验证集 35.7 → 8.2，test 8.3 → 5.2）（§2、§2f、§2p.3）。
2. 主效应（CODEBRIM test 809 张，§2p）：二元 P-AP 76.8 ± 3.1，与全监督 SegFormer-B2 76.4 持平，高于 WPFormer 70.8、AdaptCLIP 73.3、MultiADS 69.8、Bayes-PFL 62.7、AnomalyCLIP 57.0；I-AUROC 92.0 ± 0.7，AdaptCLIP 92.7。TPR 0.9 时正常图被标面积 4.4%（3 种子 4.3 至 4.6），AdaptCLIP 9.5%、SegFormer-B2 10.0%、MultiADS 12.0%、Bayes-PFL 16.1%、AnomalyCLIP 18.4%、WPFormer 27.7%；TPR 0.8 时 2.5%，与 SegFormer-B2 2.4% 持平，其余 4.6% 至 11.3%。
3. 按类（test，§2p.2）：mAP 59.4 对 MultiADS 56.2、SegFormer-B2 60.1；泛碱 70.5 对 58.7 / 58.5，锈蚀与剥落三者在 2 点内，裂缝 10.3 对 15.2 / 24.1。
4. 机制（验证集 §2f、§2h、§2i；test §2p.3）：LRM 的 γ = 0 伤裂缝；AMR 相对 v0 softmax 读出使裂缝从 1.9 到 8.3、mAP 从 48.6 到 58.7、误报面积从 5.98% 到 2.39%（test）；RRG 去残差后 P-AP 验证集 −9.7、test −3.1，正常图误报验证集约 8 倍、test 1.2 倍；参考数量与选择不敏感（差 0.1 至 0.3）；12 对 6 锚点无差异。test 种子标准差 P-AP 3.1、P-AUPRO 3.6，单种子消融差异在 3 点以内的不作结论；去 ν 门控在 test 上无可测变化。
5. 跨数据集（S2DS test 447 张、dacl10k 严格四类子集 262 张，均未接触目标域标注，§2g、§2l、§2o）：两个带类型的冻结 CLIP 头（TypeAnchor、MultiADS）在二元 P-AP 上高于两个全监督网络（S2DS 70.9 / 71.5 对 WPFormer 64.4、SegFormer-B2 63.0；dacl10k 32.8 / 36.2 对 28.4、22.0）；按类 mAP TypeAnchor 46.6 / 16.1 对 SegFormer-B2 32.7 / 8.6；MultiADS 52.8 / 18.5 高于 TypeAnchor。P-AUPRO 与图像级在 S2DS 上 WPFormer（64.2、84.6）与 Bayes-PFL（图像级 85.1）最高，TypeAnchor P-AUPRO 41.5 最低。
6. 裂缝的尺度分析（验证集）：滑窗推理 +6.6 但泛碱 −25；1/4 分辨率细节支路 +6.7，不迁移到外部集（§2m、§2n）。
7. 协议：Cleaned-Val 使正常图误报面积从 1.75% 到 0.12%，排序不变；GPU / CPU AUPRO 差 4.8；验证集（缺陷像素中位数 6,297）与 test（44,114）使 AdaptCLIP P-AP 从 61.8 变到 73.3、TypeAnchor 从 81.8 变到 76.8（§2d、§2n.3、§2p）。

**中心主张**：在冻结 CLIP 上，以文本锚点为类别接口的多类型分割头 TypeAnchor（6.6 M 可训练参数）在未参与任何选择的 CODEBRIM test 划分上，二元像素精度与全参数训练的 SegFormer-B2 持平、高于 WPFormer 与全部 CLIP 系异常检测方法，匹配召回下的正常表面误报面积为全部方法最低，并给出允许重叠的按类掩码；跨数据集上带类型的冻结 CLIP 头在像素 P-AP 与按类 mAP 上优于两个全监督分割网络，其中结构更简单的 MultiADS 优于 TypeAnchor。有监督头部的域内精度是对训练域外观的精度，跨域能力来自冻结骨干与文本对齐本身。

**边界（只写影响解释的）**：裂缝 test P-AP 10.3 对 SegFormer-B2 24.1，验证集上的分辨率补救只到 42；P-AUPRO 域内 73.5 低于 AdaptCLIP 80.4、MultiADS 78.8、WPFormer 78.0，S2DS 上最低；与 AdaptCLIP 的域内二元差距 3.5 P-AP，图像级不占优；跨域结果单种子，随训练长度摆动 2 至 5 点，几点以内的差异不作结论；WPFormer 的检查点按验证集在 15 个评估点里选最优，验证集数字偏乐观（94.6 → test 70.8），论文只用其 test 与外部集数字。

**贡献类型**：新模块（AMR + LRM + RRG）、新实证发现（域内精度与跨域能力的来源分离，评测划分对结论的影响）、新评测协议与标注。不主张新任务或新数据集。

## 2. 章节安排

| 章节 | 任务 | 主要材料 |
|---|---|---|
| 1 Introduction | 起点、缺口、洞见、贡献 | 本文件 §4 |
| 2 Related work | 2.1 桥梁与表面缺陷分割（SegFormer、WPFormer、SCSegamba、CrackSSM）；2.2 冻结 CLIP 的异常检测与多类型扩展（AnomalyCLIP、AdaptCLIP、Bayes-PFL、MultiADS、AA-CLIP、FB-CLIP）；2.3 土木数据集与评测（CODEBRIM、S2DS、dacl10k，P-AUPRO 口径） | idea-review.md 的先行工作表，参考文献目录 |
| 3 Method | 3.1 问题设定与记号；3.2 冻结骨干、适配器与文本锚点；3.3 LRM；3.4 AMR；3.5 RRG；3.6 训练目标 | model-spec.md §10.1 至 §10.7 |
| 4 Experimental setup | 数据（CODEBRIM 裁块与四类重叠掩码、train / val / test 用途、S2DS test、dacl10k 严格子集、两划分的缺陷分布）、对比方法与训练设置、指标（二元、按类多标签、匹配召回误报、P-AUPRO 口径、Cleaned-Val） | results.md §2g、§2l、§2k、§2n.3、§2p |
| 5 Results | 5.1 域内二元与误报（表 1）；5.2 按类（表 2）；5.3 消融（表 3）；5.4 跨数据集（表 4）；5.5 裂缝与尺度（表 5）；5.6 定性图 | §2p、§2f、§2i、§2l、§2o、§2m、§2n |
| 6 Discussion | 精度来源的分离；评测划分对结论的影响；对巡检应用的含义（域内部署与跨单位复用的不同选择）；P-AUPRO 与误报面积测的不是同一件事 | §2p.4、§2n.1、§2n.3、§2o |
| 7 Conclusion | 中心主张 | |

表格规划（域内表全部用 test 划分）：
- 表 1 域内二元（test 809 张）：AdaptCLIP、AnomalyCLIP、Bayes-PFL、MultiADS、SegFormer-B2、WPFormer、TypeAnchor（3 种子均值 ± 标准差）；参数量、I-AUROC、P-AUROC、P-AP、P-F1max、P-AUPRO、TPR 0.8 / 0.9 时正常图被标面积。
- 表 2 按类（test）：MultiADS、SegFormer-B2、TypeAnchor；mAP、mIoU、四类 P-AP。
- 表 3 消融（test seed 10，附 3 种子标准差；验证集数字放附表）：完整、无 LRM（γ = 0 与 γ = 1）、无 RRG（去残差）、去 ν 门控、12 锚点、v0 softmax 读出。
- 表 4 跨数据集（S2DS test、dacl10k）：七个方法；I-AUROC、P-AP、P-AUPRO、mAP、裂缝 P-AP。
- 表 5 裂缝尺度（验证集，分析实验）：整图、滑窗、滑窗混合、细节支路（只训）、细节支路（联合）、多训 10 轮对照。
- 附表：验证集原集 / Cleaned-Val 二元表（§2k）与两个划分的缺陷分布，支撑讨论里"评测划分影响结论"一段。

## 3. 主张与证据对照

| 主张 | 证据 | 强度 |
|---|---|---|
| 域内二元 P-AP 与 SegFormer-B2 持平、高于 WPFormer 与全部 CLIP 系方法 | §2p.1，3 种子 76.8 ± 3.1 对 76.4 / 70.8 / 73.3 / 69.8 / 62.7 / 57.0 | 对 CLIP 系与 WPFormer 中到强（差距 3.5 至 20）；对 SegFormer "持平" |
| 匹配召回下正常图误报面积最低 | §2p.1 TPR 0.9：4.4% 对 9.5% / 10.0% / 12.0% / 27.7%，3 种子 4.3 至 4.6 | 强 |
| 按类 mAP 高于 MultiADS、与 SegFormer-B2 相近；泛碱最好 | §2p.2，59.4 对 56.2 / 60.1；泛碱 70.5 对 58.7 / 58.5 | 中（MultiADS、SegFormer 单种子） |
| AMR 优于 softmax 读出；LRM 的局部相似度必须保留 | v0 裂缝 0.07 / 1.9，γ = 0 裂缝 35.7 → 8.2（验证集）、8.3 → 5.2（test）；v0 误报 5.98% 对 2.39% | 强 |
| RRG 有用、参考不敏感 | §2i −9.7（验证集），§2p.3 −3.1（test），§2h 差 0.1 至 0.3 | 中弱（test 差异在种子标准差内） |
| ν 门控 | §2f −1.1 / −2.8；§2p.3 +0.4 / −0.1 | 不作主张，作为模型组成描述 |
| 带类型的冻结 CLIP 头跨域 P-AP 与 mAP 优于全监督分割 | §2o、§2l：两个外部集一致，P-AP 高 4 至 14 点（dacl10k 上 TypeAnchor 对 WPFormer 只高 4.4），mAP 高 7.5 至 14 点 | 中（P-AUPRO 与图像级不成立） |
| TypeAnchor 跨域不如 MultiADS | §2o，S2DS mAP −6.2，dacl10k −2.4 | S2DS 中，dacl10k 弱（在摆动范围内） |
| 分辨率是裂缝瓶颈之一但不是全部 | §2m、§2n | 中 |
| P-AUPRO 低于 AdaptCLIP、MultiADS、WPFormer | §2p.1（80.4 / 78.8 / 78.0 对 73.5 ± 3.6）、§2o | 强 |
| 评测划分改变结论 | §2p：AdaptCLIP 61.8 → 73.3，TypeAnchor 81.8 → 76.8，缺陷像素中位数差 7 倍 | 强 |

## 4. 英文初稿

### Title

TypeAnchor: Text-Anchored Multi-Type Defect Segmentation on a Frozen Vision-Language Model for Concrete Bridge Inspection

### Abstract

Bridge inspection turns images of concrete surfaces into repair decisions, and the decision depends on the defect type: cracks are measured by width and orientation, spalling and corrosion by exposed area, efflorescence by the moisture path behind it. A pixel map that only separates damaged from intact surface is therefore not enough, and the types overlap on the same surface. Fully supervised segmentation networks deliver type-specific maps but lose accuracy on images from another agency, while anomaly detectors built on frozen CLIP transfer better but return one binary map. We present TypeAnchor, a light supervised head that uses the text embeddings of a frozen CLIP ViT-L/14 as a class interface rather than as an anomaly score. Each defect type receives a text anchor, and an Anchor Margin Readout turns the similarity margin between the type anchor and the intact-surface anchor into an independent per-type probability, so types may overlap. A Local–Regional Similarity Mixture learns, per anchor, how much patch-level and neighbourhood similarity to use, which keeps thin cracks visible while large defects draw on context. A Reference-Residual Gate derived from one intact image scales a class-agnostic defect channel and the image-level score. Trained on 2,861 CODEBRIM tiles, 917 with per-type masks, the head has 6.6 M trainable parameters. On the held-out CODEBRIM test split of 809 tiles its binary pixel average precision is 76.8 over three seeds, level with a fully trained SegFormer-B2 at 76.4 and above WPFormer, AdaptCLIP, MultiADS, Bayes-PFL and AnomalyCLIP trained on the same tiles. At 90% pixel recall it marks 4.4% of the intact surface, less than half of every other method, and its per-type masks reach a mean average precision of 59.4 against 56.2 for MultiADS. On S2DS and dacl10k, without target data, the two type-aware frozen-CLIP heads exceed both supervised networks in pixel average precision and per-type mean average precision, and the simpler MultiADS exceeds TypeAnchor. In-domain accuracy of a supervised head is accuracy on the training domain's appearance; transfer comes from the frozen backbone and its text alignment. We release the per-type masks and an evaluation protocol with matched-recall false-alarm area, a cleaned validation split, two external test sets and a reconciled P-AUPRO, and we show that moving from a validation split dominated by small defects to a test split dominated by large ones changes the margin over AdaptCLIP from 20 points to 3.5.

（约 370 词，期刊通常限 250 至 300，定稿时压缩。数据与代码公开的句子以用户确认 CODEBRIM 许可为前提。）

### 1. Introduction

Visual inspection of concrete bridges produces images in which several kinds of damage coexist: cracks as narrow discontinuities, spalling as broken-off regions that expose aggregate or reinforcement, corrosion as rust staining around exposed steel, and efflorescence as white deposits left by water moving through the concrete. Maintenance acts on these types differently. A crack is assessed by its width and orientation, spalling and corrosion by the exposed area and the condition of the reinforcement, and efflorescence as evidence of a leakage path. The pixel map that an inspection system hands to an engineer therefore needs to say which type is where, and it needs to allow overlap, because corrosion appears inside spalled regions and efflorescence runs across cracks. The map also needs to survive a change of image collection. Agencies photograph different structures with different cameras and lighting, and pixel-level annotation of every new collection is the most expensive step in deploying such a system.

Two families of methods meet parts of this requirement. Fully supervised segmentation networks, from general architectures such as SegFormer to surface-defect designs such as WPFormer and crack-specific networks, give type-specific masks and high accuracy on the collection they were trained on. On a different collection their accuracy drops, and they are silent about damage outside the training classes. Anomaly detection on frozen vision-language models moves in the opposite direction. AnomalyCLIP, AdaptCLIP and Bayes-PFL keep the CLIP encoders fixed, learn a few million parameters that align patch features with normal and abnormal text, and transfer across industrial domains with zero or one normal image. Their output is a single binary anomaly map. MultiADS extends this line with one text prompt per defect type and a pixel-level softmax over the types, which produces type maps but assigns each pixel one type and was designed on industrial objects photographed under controlled conditions.

Three obstacles separate these families from the inspection requirement. The class interface is the first. A normal-versus-abnormal formulation has no place for types, and a softmax over types has no place for overlap. The second is scale. At the 518-pixel input of CLIP ViT-L/14 the patch grid is 37 by 37, about 14 pixels per cell, and cracks are often thinner than one cell. Pooling similarity over a neighbourhood, which stabilises large defects, erases cracks: in our ablation on the validation split, replacing patch-level similarity by 5 by 5 regional pooling drops crack average precision from 35.7 to 8.2, while spalling and efflorescence are unaffected. Scale requirements differ by type. The third is measurement. Public civil-engineering datasets store flattened single-label masks in which a priority rule removes overlap, validation sets labelled as intact contain unlabelled defects that inflate false-alarm measurements, the two common implementations of the region-overlap metric P-AUPRO disagree by several points on identical predictions, and the defect-size distribution of the evaluation split moves the margin between two methods by more than ten points. Under these conditions it is hard to tell whether a method that looks better is better.

TypeAnchor addresses the interface and scale obstacles with one design decision: the text anchors of a frozen CLIP serve as a class interface for a light supervised head, not as an anomaly detector. Six anchors represent intact surface, the four defect types and generic damaged surface. The Local–Regional Similarity Mixture computes, for each anchor, the similarity between the anchor and the projected patch tokens at patch level and over a residual-weighted neighbourhood, and a learned per-anchor weight mixes the two, so the crack anchor can stay local while the spalling and efflorescence anchors use context. The Anchor Margin Readout passes the margin between each type anchor and the intact anchor through an independent sigmoid; a pixel may be positive for several types. The Reference-Residual Gate keeps the residual between the query tokens and the nearest tokens of a single intact reference image, not as a score but as a gate that scales a class-agnostic defect channel and the image-level head, suppressing responses on intact texture and catching damage outside the four types. The head has 6.6 M trainable parameters and needs one arbitrary intact image at inference.

We trained TypeAnchor on 2,861 CODEBRIM training tiles, 917 of which carry overlapping per-type masks that we annotated, selected every design choice on the validation split, and report on the test split of 809 tiles that no choice ever touched, and, without any target data, on S2DS and on a strict four-type subset of dacl10k. On the test split the head reaches a binary pixel average precision of 76.8 over three seeds, level with a fully trained SegFormer-B2 at 76.4 and above WPFormer at 70.8, AdaptCLIP at 73.3, MultiADS at 69.8, Bayes-PFL at 62.7 and AnomalyCLIP at 57.0, all trained with their official code on the same tiles. Image-level AUROC is 92.0 against 92.7 for AdaptCLIP. At 90% pixel recall the head marks 4.4% of the intact surface, against 9.5% for AdaptCLIP, 10.0% for SegFormer-B2 and 12.0% for MultiADS. Its per-type mean average precision is 59.4 against 56.2 for MultiADS and 60.1 for SegFormer-B2, with the largest per-type difference on efflorescence, 70.5 against 58.7 and 58.5; on cracks SegFormer-B2 keeps a lead of 14 points.

The cross-dataset results separate the two sources of accuracy. On S2DS and dacl10k the two type-aware frozen-CLIP heads, TypeAnchor and MultiADS, reach a higher pixel average precision than WPFormer and SegFormer-B2 on both sets, and TypeAnchor segments the four types better than SegFormer-B2 by 14 points of mean average precision on S2DS and 7.5 on dacl10k, while MultiADS, with 3.1 M linear parameters and no residual channel, is better than TypeAnchor on both external sets. Fine-tuning TypeAnchor for ten more epochs moves the external numbers by two to five points in inconsistent directions. The evaluation split matters as much as the method: on the validation split, where the median defect covers 6,300 pixels, TypeAnchor is 20 points of pixel average precision ahead of AdaptCLIP; on the test split, where it covers 44,000, the margin is 3.5. In-domain accuracy of a supervised head is accuracy on the training domain's appearance; what transfers is the frozen backbone and its alignment with text. Resolution explains part of the crack deficit: sliding-window inference at twice the resolution and a quarter-resolution detail branch each add about seven points of crack average precision on the validation split, and neither transfers.

The contributions are the following. We propose TypeAnchor, a text-anchored multi-type segmentation head for frozen CLIP with independent per-type readouts on anchor margins, a per-anchor local-regional similarity mixture, and a residual-gated class-agnostic channel, and we show through ablation which obstacle each part removes. We provide overlapping per-type pixel masks for CODEBRIM tiles together with an evaluation protocol for bridge inspection: per-type multi-label metrics, false-alarm area at matched recall, a cleaned validation split, two external test sets, and a reconciled P-AUPRO. We report, on the same data and protocol, how CLIP-based anomaly detectors, their multi-type extension and two fully supervised networks compare in-domain and across datasets, and we trace in-domain accuracy and cross-dataset accuracy to different causes.

## 5. 已定事项（2026-11-08，用户决定）

1. CODEBRIM 裁块与自标注掩码：合理请求下提供（available on request），不写无条件公开。
2. 对比表保留 Bayes-PFL 与 WPFormer（检查点来自旧项目，results.md §2o 注明选轮方式）。
3. ProtoBridge 未发表，文中不提。
4. 题目与模块名（§0）；中心主张（§1）；去掉 MixerCSeg；主表用 test 划分。
5. 投稿格式：IEEE 会议模板（IEEEtran conference），正文含参考文献 6 页；作者暂列 Qiang Liu、Haifeng Zhong（湖南工业大学两处署名），其余作者待加。

## 6. 初稿（2026-11-08）

paper/main.tex、paper/refs.bib、paper/IEEEtran.cls，服务器编译 6 页无错误；打包 paper/TypeAnchor_overleaf.zip。主图（图 1 总览）与定性图（图 2）为占位框，待绘制。表 1 至表 4 数字来自 results.md §2p、§2o、§2l；消融表最后一列为验证集裂缝 P-AP（runs/*/val-epoch20/metrics_multiclass.json）。
