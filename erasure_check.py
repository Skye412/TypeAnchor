#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""统计擦除充分性检验（docs/audit-design.md 协议修正 2）。

在未经桥梁训练的冻结骨干上，用 patch 最近邻残差做异常分，并在残差上施加
IDEAL 式 Normal Variation Eraser（最近 12 个正常 patch 的 PCA 4 维子空间，
子空间内分量乘 alpha）。alpha=1.0 为不擦除，0.8 为 IDEAL 默认，0.0 为完全投影。
只用视觉特征，不用文本。

骨干：
  dino  DINOv2-B/14，最后一层 patch token（与 runs/audit/anomalydino 同配置）
  clip  CLIP ViT-L/14@336（DPAM 20），层 6/12/18/24 patch token，分数取四层均值
参考：runs/audit/anomalydino/references.json 的 16 张训练集正常图（种子 10）。
特征统一 L2 归一化后用欧氏距离。
输出：runs/erasure/<backbone>/alpha_<a>/maps/<stem>.npy（512×512，高斯 sigma 4）
      runs/erasure/<backbone>/results.json 与 results.md
"""
import argparse, json, os, sys, time
from pathlib import Path
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from scipy.ndimage import gaussian_filter
import cv2

ROOT = Path(__file__).resolve().parent
ALPHAS = [1.0, 0.8, 0.0]
K_NEIGH = 12
N_COMP = 4


def read_list(p):
    return [l.strip() for l in open(p, encoding='utf-8') if l.strip()]


class Backbone:
    def __init__(self, name, device):
        self.name = name; self.device = device
        if name == 'dino':
            from torchvision import transforms
            self.model = torch.hub.load('/home/skye/.cache/torch/hub/facebookresearch_dinov2_main', 'dinov2_vitb14',
                                        source='local', pretrained=True).to(device).eval()
            self.tf = transforms.Compose([
                transforms.Resize((518, 518), interpolation=transforms.InterpolationMode.BICUBIC, antialias=True),
                transforms.ToTensor(), transforms.Normalize((.485, .456, .406), (.229, .224, .225))])
        elif name == 'clip':
            import adaptcliplib
            from tools import get_transform
            self.model, _ = adaptcliplib.load('ViT-L/14@336px', device=device)
            self.model.visual.DAPM_replace(DPAM_layer=20); self.model.eval()
            self.tf, _ = get_transform(518)
        else:
            raise ValueError(name)

    @torch.inference_mode()
    def features(self, path):
        """返回 list of [N, d]（每层一个），已 L2 归一化，不含 CLS。"""
        x = self.tf(Image.open(path).convert('RGB')).unsqueeze(0).to(self.device)
        if self.name == 'dino':
            f = self.model.get_intermediate_layers(x)[0][0].float()
            return [F.normalize(f, dim=-1)]
        _, toks = self.model.encode_image(x, [6, 12, 18, 24], proj_use=False, DPAM_layer=20)
        return [F.normalize(t[0, 1:].float(), dim=-1) for t in toks]


@torch.inference_mode()
def erased_scores(q, bank, chunk=256):
    """q [N,d], bank [M,d] -> dict alpha -> [N] 残差范数。"""
    out = {a: [] for a in ALPHAS}
    for part in q.split(chunk):
        d = torch.cdist(part, bank)                      # [n, M]
        idx = d.topk(K_NEIGH, dim=1, largest=False).indices  # [n, K]
        nb = bank[idx]                                   # [n, K, d]
        nearest = nb[:, 0]
        r = part - nearest                               # [n, d]
        c = nb - nb.mean(1, keepdim=True)                # [n, K, d]
        # 批量 SVD 取前 N_COMP 个右奇异向量作为局部正常变异子空间
        _, _, vh = torch.linalg.svd(c, full_matrices=False)   # vh [n, K, d]
        u = vh[:, :N_COMP]                               # [n, C, d]
        proj = torch.einsum('nd,ncd->nc', r, u)          # [n, C]
        r_sub = torch.einsum('nc,ncd->nd', proj, u)      # [n, d]
        for a in ALPHAS:
            ra = r - (1.0 - a) * r_sub
            out[a].append(ra.norm(dim=-1))
    return {a: torch.cat(v) for a, v in out.items()}


def to_map(grid37):
    g = grid37.reshape(37, 37).cpu().numpy().astype(np.float32)
    return gaussian_filter(cv2.resize(g, (512, 512), interpolation=cv2.INTER_LINEAR), sigma=4).astype(np.float32)


def run_maps(args, device):
    bb = Backbone(args.backbone, device)
    refs = json.loads((ROOT / 'runs/audit/anomalydino/references.json').read_text())
    banks = None
    for p in refs:
        fs = bb.features(p)
        banks = [[f] for f in fs] if banks is None else [b + [f] for b, f in zip(banks, fs)]
    banks = [torch.cat(b) for b in banks]               # per layer [M, d]
    print(f'[{args.backbone}] bank layers={len(banks)} M={banks[0].shape[0]} d={banks[0].shape[1]}', flush=True)
    view = ROOT / 'data_views/val'
    names = read_list(view / 'normal.txt') + read_list(view / 'anomaly.txt')
    if args.limit: names = names[:args.limit // 2] + names[-(args.limit - args.limit // 2):]
    outdir = ROOT / 'runs/erasure' / args.backbone
    for a in ALPHAS: (outdir / f'alpha_{a}' / 'maps').mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    for i, n in enumerate(names):
        stem = Path(n).stem
        if all((outdir / f'alpha_{a}' / 'maps' / f'{stem}.npy').exists() for a in ALPHAS): continue
        fs = bb.features(view / 'images' / n)
        acc = {a: None for a in ALPHAS}
        for f, bank in zip(fs, banks):
            s = erased_scores(f, bank)
            for a in ALPHAS: acc[a] = s[a] if acc[a] is None else acc[a] + s[a]
        for a in ALPHAS:
            m = to_map(acc[a] / len(fs))
            if not np.isfinite(m).all(): raise ValueError(n)
            np.save(outdir / f'alpha_{a}' / 'maps' / f'{stem}.npy', m)
        if (i + 1) % 20 == 0: print(f'  {i+1}/{len(names)}  {time.time()-t0:.0f}s', flush=True)
    print(f'[{args.backbone}] maps done in {time.time()-t0:.0f}s', flush=True)


def metrics(args):
    from sklearn.metrics import roc_auc_score, average_precision_score
    view = ROOT / 'data_views/val'
    normal = read_list(view / 'normal.txt'); anomaly = read_list(view / 'anomaly.txt')
    if args.limit: normal = normal[:args.limit // 2]; anomaly = anomaly[-(args.limit - args.limit // 2):]
    outdir = ROOT / 'runs/erasure' / args.backbone
    masks = {}
    for n in anomaly:
        m = np.asarray(Image.open(view / 'masks_union' / (Path(n).stem + '.png')).convert('L').resize((512, 512), Image.NEAREST)) > 0
        masks[n] = m
    rng = np.random.default_rng(0)
    res = {}
    for a in ALPHAS:
        md = outdir / f'alpha_{a}' / 'maps'
        pos, neg, nm = [], [], []
        for n in anomaly:
            s = np.load(md / (Path(n).stem + '.npy')); g = masks[n]; pos.append(s[g]); neg.append(s[~g])
        for n in normal: nm.append(np.load(md / (Path(n).stem + '.npy')).ravel())
        pos = np.concatenate(pos); neg = np.concatenate(neg); nm = np.concatenate(nm)
        thr = float(np.quantile(pos, 1 - args.tpr))
        flagged = float((nm >= thr).mean()); bgfpr = float((neg >= thr).mean())
        # 像素级 AUROC/AP：分层子采样 2M 像素（诊断用途）
        negall = np.concatenate([neg, nm])
        k = min(1_000_000, len(pos)); kp = rng.choice(len(pos), k, replace=False)
        k2 = min(1_000_000, len(negall)); kn = rng.choice(len(negall), k2, replace=False)
        y = np.r_[np.ones(k), np.zeros(k2)]; sc = np.r_[pos[kp], negall[kn]]
        res[str(a)] = {'threshold_tpr50': thr, 'normal_img_flagged_area': flagged, 'anomaly_img_bg_fpr': bgfpr,
                       'P-AUROC_subsampled': float(roc_auc_score(y, sc)), 'P-AP_subsampled': float(average_precision_score(y, sc)),
                       'n_normal': len(normal), 'n_anomaly': len(anomaly)}
    base = res['1.0']['normal_img_flagged_area']
    for a in ALPHAS:
        res[str(a)]['relative_drop_vs_alpha1'] = 1 - res[str(a)]['normal_img_flagged_area'] / base
    def verdict(drop):
        if drop >= .5: return '下降≥50%：统计擦除基本够用，语义锚点改为互补'
        if drop < .25: return '下降<25%：统计擦除不足，主路线成立'
        return '25%–50%：主路线保留，P3 互补性升为核心'
    res['verdict_alpha0.8'] = verdict(res['0.8']['relative_drop_vs_alpha1'])
    res['verdict_alpha0.0'] = verdict(res['0.0']['relative_drop_vs_alpha1'])
    res['protocol'] = {'tpr': args.tpr, 'k_neighbors': K_NEIGH, 'n_components': N_COMP, 'features': 'L2-normalized', 'references': 16, 'limit': args.limit}
    (outdir / 'results.json').write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = [f'## {args.backbone}：统计擦除充分性（TPR={args.tpr}，正常图 {len(normal)}，异常图 {len(anomaly)}）', '',
             '| alpha | 阈值 | 正常图被标面积 | 相对 alpha=1 下降 | 异常图背景 FPR | P-AUROC(子采样) | P-AP(子采样) |', '|---|---|---|---|---|---|---|']
    for a in ALPHAS:
        r = res[str(a)]
        lines.append(f"| {a} | {r['threshold_tpr50']:.4f} | {r['normal_img_flagged_area']:.3f} | {r['relative_drop_vs_alpha1']:+.1%} | {r['anomaly_img_bg_fpr']:.3f} | {r['P-AUROC_subsampled']:.3f} | {r['P-AP_subsampled']:.3f} |")
    lines += ['', f"判定（alpha=0.8）：{res['verdict_alpha0.8']}", f"判定（alpha=0.0）：{res['verdict_alpha0.0']}"]
    (outdir / 'results.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\n'.join(lines), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--backbone', choices=['dino', 'clip'], required=True)
    ap.add_argument('--limit', type=int, default=0, help='烟雾测试用：只处理前 N 张（正常/异常各半）')
    ap.add_argument('--tpr', type=float, default=0.5)
    ap.add_argument('--skip-maps', action='store_true')
    a = ap.parse_args()
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    if not a.skip_maps: run_maps(a, device)
    metrics(a)


if __name__ == '__main__':
    main()
