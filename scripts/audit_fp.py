#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""假阳性审计工具。

输入约定（与模型代码解耦）：
  --maps <dir>     每个模型一个目录，内含与图像同名的 .npy 异常图（float，HxW，与原图同尺寸）。
  --images <dir>   原图目录（png/jpg）。
  --normal-list    正常图文件名列表（每行一个，不含路径，可带扩展名）。
  --anomaly-list   异常图文件名列表（用于阈值标定）。
  --masks <dir>    异常图的二值 GT 掩码目录（png，>0 为缺陷；多标签时先取并集），用于 TPR=95% 标定。

子命令：
  threshold  在异常图上标定 TPR=95% 阈值，写 threshold.json
  extract    在正常图上按阈值提取连通块，写 blobs.csv
  sample     面积三分位分层抽样，写 sample.csv（含空的 label 列）
  export     导出每个抽样块的标注卡 png 到 cards/
  summarize  读取填好 label 的 sample.csv，输出表 1–3（markdown）与图 1（png）

依赖：numpy, pillow, scipy, matplotlib（仅 summarize/export）。
"""
import argparse
import csv
import json
import os
import random
import sys

import numpy as np
from PIL import Image, ImageDraw

try:
    from scipy import ndimage
except ImportError:  # pragma: no cover
    ndimage = None

CATEGORIES = {
    "A1": "水渍/湿斑", "A2": "阴影/光照边界", "A3": "苔藓/生物附着", "A4": "修补/砂浆填充",
    "A5": "涂鸦/油漆", "A6": "模板纹理/施工缝/构件边缘", "A7": "污垢/烟熏",
    "B1": "骨料/表面纹理颗粒", "B2": "平滑光照渐变/曝光", "B3": "模糊/噪声/压缩伪影",
    "C1": "背景物体", "C2": "裁块边界/填充",
    "D1": "疑似四类缺陷", "D2": "疑似其他缺陷",
    "E": "无法判断",
}
GROUPS = ["A", "B", "C", "D", "E"]


def read_list(path):
    with open(path, encoding="utf-8") as f:
        return [ln.strip() for ln in f if ln.strip()]


def stem(name):
    return os.path.splitext(os.path.basename(name))[0]


def load_map(maps_dir, name):
    p = os.path.join(maps_dir, stem(name) + ".npy")
    if not os.path.exists(p):
        raise FileNotFoundError(p)
    return np.load(p).astype(np.float32)


def find_image(images_dir, name):
    for ext in ("", ".png", ".jpg", ".jpeg", ".PNG", ".JPG"):
        p = os.path.join(images_dir, stem(name) + ext) if ext else os.path.join(images_dir, name)
        if os.path.isfile(p):
            return p
    raise FileNotFoundError(os.path.join(images_dir, name))


def load_mask(masks_dir, name):
    p = find_image(masks_dir, name)
    m = np.array(Image.open(p))
    if m.ndim == 3:
        m = m.max(axis=2)
    return m > 0


def cmd_threshold(a):
    names = read_list(a.anomaly_list)
    pos, neg = [], []
    for n in names:
        s = load_map(a.maps, n)
        m = load_mask(a.masks, n)
        if s.shape != m.shape:
            raise ValueError(f"shape mismatch {n}: map {s.shape} mask {m.shape}")
        pos.append(s[m])
        neg.append(s[~m])
    pos = np.concatenate(pos)
    neg = np.concatenate(neg)
    thr = float(np.quantile(pos, 1.0 - a.tpr))
    fpr = float((neg >= thr).mean())
    out = {"model": a.model, "tpr_target": a.tpr, "threshold": thr,
           "pixel_fpr_on_anomaly_images": fpr, "n_images": len(names)}
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "threshold.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(json.dumps(out, ensure_ascii=False))


def cmd_extract(a):
    if ndimage is None:
        sys.exit("需要 scipy")
    with open(os.path.join(a.out, "threshold.json"), encoding="utf-8") as f:
        thr = json.load(f)["threshold"]
    names = read_list(a.normal_list)
    rows = []
    structure = np.ones((3, 3), dtype=bool)  # 8 连通
    for n in names:
        s = load_map(a.maps, n)
        b = s >= thr
        lab, k = ndimage.label(b, structure=structure)
        if k == 0:
            continue
        objs = ndimage.find_objects(lab)
        for i, sl in enumerate(objs, start=1):
            region = lab[sl] == i
            area = int(region.sum())
            if area < a.min_area:
                continue
            vals = s[sl][region]
            y0, y1 = sl[0].start, sl[0].stop
            x0, x1 = sl[1].start, sl[1].stop
            rows.append({
                "blob_id": f"{a.model}__{stem(n)}__{i}",
                "model": a.model, "image": n, "area": area,
                "x0": x0, "y0": y0, "x1": x1, "y1": y1,
                "mean_score": float(vals.mean()), "max_score": float(vals.max()),
            })
    path = os.path.join(a.out, "blobs.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["blob_id"])
        w.writeheader()
        w.writerows(rows)
    total_area = sum(r["area"] for r in rows)
    print(f"{a.model}: {len(rows)} blobs, total FP area {total_area} px over {len(names)} normal images")


def cmd_sample(a):
    with open(os.path.join(a.out, "blobs.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["area"] = int(r["area"])
    if not rows:
        sys.exit("blobs.csv 为空")
    areas = np.array([r["area"] for r in rows])
    q1, q2 = np.quantile(areas, [1 / 3, 2 / 3])
    strata = {0: [], 1: [], 2: []}
    for r in rows:
        k = 0 if r["area"] <= q1 else (1 if r["area"] <= q2 else 2)
        r["stratum"] = k
        strata[k].append(r)
    rng = random.Random(a.seed)
    picked = []
    for k, lst in strata.items():
        n_k = min(a.per_stratum, len(lst))
        chosen = rng.sample(lst, n_k)
        # 分层权重：该层总面积 / 抽中块总面积，用于还原面积占比
        tot = sum(r["area"] for r in lst)
        sub = sum(r["area"] for r in chosen) or 1
        for r in chosen:
            r["stratum_area_weight"] = tot / sub
            r["stratum_count_weight"] = len(lst) / n_k
            picked.append(r)
    fields = ["blob_id", "model", "image", "area", "x0", "y0", "x1", "y1",
              "mean_score", "max_score", "stratum", "stratum_area_weight",
              "stratum_count_weight", "label", "note"]
    path = os.path.join(a.out, "sample.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in picked:
            r.setdefault("label", "")
            r.setdefault("note", "")
            w.writerow({k: r.get(k, "") for k in fields})
    print(f"sampled {len(picked)} blobs -> {path}; 三分位边界 {q1:.0f}/{q2:.0f} px")


def cmd_export(a):
    with open(os.path.join(a.out, "sample.csv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(os.path.join(a.out, "threshold.json"), encoding="utf-8") as f:
        thr = json.load(f)["threshold"]
    cards = os.path.join(a.out, "cards")
    os.makedirs(cards, exist_ok=True)
    for r in rows:
        img = Image.open(find_image(a.images, r["image"])).convert("RGB")
        s = load_map(a.maps, r["image"])
        x0, y0, x1, y1 = (int(r[k]) for k in ("x0", "y0", "x1", "y1"))
        # 轮廓叠加
        b = (s >= thr)
        labels, _ = ndimage.label(b, structure=np.ones((3, 3), dtype=bool))
        component_id = int(r["blob_id"].rsplit("__", 1)[-1])
        component = labels == component_id
        if int(component.sum()) != int(r["area"]):
            raise ValueError(f"Component identity mismatch: {r['blob_id']}")
        b = component.astype(np.uint8)
        if ndimage is not None:
            edge = b - ndimage.binary_erosion(b).astype(np.uint8)
        else:
            edge = b
        ov = img.copy()
        arr = np.array(ov)
        arr[edge > 0] = [255, 0, 0]
        ov = Image.fromarray(arr)
        d = ImageDraw.Draw(ov)
        d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=(0, 255, 0), width=2)
        # 局部放大
        pad = a.pad
        cx0, cy0 = max(0, x0 - pad), max(0, y0 - pad)
        cx1, cy1 = min(img.width, x1 + pad), min(img.height, y1 + pad)
        crop = ov.crop((cx0, cy0, cx1, cy1))
        side = max(crop.width, crop.height)
        scale = max(1, 256 // max(1, side))
        crop = crop.resize((crop.width * scale, crop.height * scale), Image.NEAREST)
        W = ov.width + crop.width + 10
        H = max(ov.height, crop.height)
        card = Image.new("RGB", (W, H), (255, 255, 255))
        card.paste(ov, (0, 0))
        card.paste(crop, (ov.width + 10, 0))
        card.save(os.path.join(cards, r["blob_id"] + ".png"))
    print(f"exported {len(rows)} cards -> {cards}")


def cmd_summarize(a):
    rows = []
    for sample_path in a.samples:
        with open(sample_path, encoding="utf-8") as f:
            rows.extend(csv.DictReader(f))
    unl = [r for r in rows if not r["label"].strip()]
    if unl:
        print(f"警告：{len(unl)} 块未标注，已跳过", file=sys.stderr)
    rows = [r for r in rows if r["label"].strip()]
    bad = sorted({r["label"] for r in rows if r["label"] not in CATEGORIES})
    if bad:
        sys.exit(f"非法标签：{bad}")
    models = sorted({r["model"] for r in rows})
    lines = []
    # 表 1：模型 × 细类（面积占比，分层权重还原）
    lines.append("## 表 1 每模型 × 细类 假阳性面积占比（%）\n")
    cats = list(CATEGORIES.keys())
    lines.append("| 模型 | " + " | ".join(cats) + " |")
    lines.append("|---|" + "---|" * len(cats))
    group_share = {}
    h2 = {}
    for m in models:
        rs = [r for r in rows if r["model"] == m]
        tot = sum(float(r["area"]) * float(r["stratum_area_weight"]) for r in rs)
        share = {c: 0.0 for c in cats}
        for r in rs:
            share[r["label"]] += float(r["area"]) * float(r["stratum_area_weight"]) / tot * 100
        lines.append(f"| {m} | " + " | ".join(f"{share[c]:.1f}" for c in cats) + " |")
        g = {k: sum(v for c, v in share.items() if c.startswith(k)) for k in GROUPS}
        group_share[m] = g
        # H2：A 与 B 块的平均分（块数加权，不用面积权）
        def mean_of(prefix, key):
            v = [float(r[key]) for r in rs if r["label"].startswith(prefix)]
            return (sum(v) / len(v), len(v)) if v else (float("nan"), 0)
        h2[m] = {"A_mean": mean_of("A", "mean_score"), "B_mean": mean_of("B", "mean_score"),
                 "A_max": mean_of("A", "max_score"), "B_max": mean_of("B", "max_score")}
    # 表 2：组汇总 + 判定
    lines.append("\n## 表 2 组汇总面积占比（%）与判定\n")
    lines.append("| 模型 | A | B | C | D | E | share_A(排除D) | share_B(排除D) | 判定 |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for m in models:
        g = group_share[m]
        denom = 100.0 - g["D"] or 1.0
        sa, sb = g["A"] / denom, g["B"] / denom
        if g["D"] >= 15:
            verdict = "D≥15%：先清洗正常图标签"
        elif sb >= 0.5:
            verdict = "share_B≥0.5：转备用路线"
        elif sa >= 0.5:
            verdict = "share_A≥0.5：维持主路线"
        else:
            verdict = "A、B 均未过半：维持主路线，P3 升为核心"
        lines.append(f"| {m} | " + " | ".join(f"{g[k]:.1f}" for k in GROUPS) +
                     f" | {sa:.2f} | {sb:.2f} | {verdict} |")
    # 表 3：H2
    lines.append("\n## 表 3 H2：A 类与 B 类块的分数（块数加权均值，括号为块数）\n")
    lines.append("| 模型 | A mean | B mean | 差 | A max | B max | 差 |")
    lines.append("|---|---|---|---|---|---|---|")
    for m in models:
        d = h2[m]
        lines.append(f"| {m} | {d['A_mean'][0]:.3f} ({d['A_mean'][1]}) | {d['B_mean'][0]:.3f} ({d['B_mean'][1]}) | "
                     f"{d['A_mean'][0]-d['B_mean'][0]:+.3f} | {d['A_max'][0]:.3f} ({d['A_max'][1]}) | "
                     f"{d['B_max'][0]:.3f} ({d['B_max'][1]}) | {d['A_max'][0]-d['B_max'][0]:+.3f} |")
    os.makedirs(a.out, exist_ok=True)
    md = os.path.join(a.out, "audit-summary.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    # 图 1
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 3.2))
        bottom = np.zeros(len(models))
        for k in GROUPS:
            vals = np.array([group_share[m][k] for m in models])
            ax.barh(models, vals, left=bottom, label=k)
            bottom += vals
        ax.set_xlabel("FP area share (%)")
        ax.set_xlim(0, 100)
        ax.legend(ncol=5, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.25))
        fig.tight_layout()
        fig.savefig(os.path.join(a.out, "fig1-fp-share.png"), dpi=200)
        print("fig1 saved")
    except Exception as e:  # pragma: no cover
        print(f"图 1 未生成：{e}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("threshold")
    t.add_argument("--model", required=True)
    t.add_argument("--maps", required=True)
    t.add_argument("--masks", required=True)
    t.add_argument("--anomaly-list", required=True)
    t.add_argument("--tpr", type=float, default=0.95)
    t.add_argument("--out", required=True)
    t.set_defaults(fn=cmd_threshold)

    e = sub.add_parser("extract")
    e.add_argument("--model", required=True)
    e.add_argument("--maps", required=True)
    e.add_argument("--normal-list", required=True)
    e.add_argument("--min-area", type=int, default=64)
    e.add_argument("--out", required=True)
    e.set_defaults(fn=cmd_extract)

    s = sub.add_parser("sample")
    s.add_argument("--per-stratum", type=int, default=40)
    s.add_argument("--seed", type=int, default=0)
    s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_sample)

    x = sub.add_parser("export")
    x.add_argument("--maps", required=True)
    x.add_argument("--images", required=True)
    x.add_argument("--pad", type=int, default=32)
    x.add_argument("--out", required=True)
    x.set_defaults(fn=cmd_export)

    z = sub.add_parser("summarize")
    z.add_argument("--samples", nargs="+", required=True, help="一个或多个填好 label 的 sample.csv")
    z.add_argument("--out", required=True)
    z.set_defaults(fn=cmd_summarize)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
