"""Build the dacl10k cross-dataset evaluation view (strict four-class subset of the official v3 validation split).

Source: official dacl10k v3, 512x512 release (open-data.unibw.de files 7529 / 7530, MD5 verified 2026-11-05), validation
split (975 images; the only held-out split with public masks; nothing here was trained on dacl10k).
  anomaly : contains Crack / Rust / Spalling / Efflorescence and NO other damage class        (label 1)
  normal  : contains no damage class at all (bridge components such as bearings or drainage are allowed) (label 0)
  excluded: any image with another damage class (Weathering, Cavity, Hollowareas, ...), whose pixels are neither
            defect nor background for a four-class model.
Rust is mapped to our Corrosion class. Classes may overlap (independent masks); the flattened RGB mask uses the same
palette / priority as the CODEBRIM tiles (crack > corrosion > spalling > efflorescence).

Outputs (same layout as Bridge512_balance_S2DS so every evaluator applies unchanged):
  <out>/test_manifest.csv, <out>/test/{normal,annotated}/, <out>/test/multiclass_annotations/masks/<sample>__<Class>.png
  <view>/test/{meta.json,masks_union/}  for the official AdaptCLIP test.py
Usage: python scripts/prepare_dacl10k.py
"""
import argparse, csv, json, os
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
MAP = {'Crack': 'Crack', 'Rust': 'Corrosion', 'Spalling': 'Spalling', 'Efflorescence': 'Efflorescence'}
ORDER = ['Efflorescence', 'Spalling', 'Corrosion', 'Crack']            # painted in this order: later wins
PALETTE = {'Crack': (255, 0, 0), 'Corrosion': (0, 0, 255), 'Spalling': (0, 255, 0), 'Efflorescence': (255, 255, 0)}
OBJECTS = {'Bearing', 'EJoint', 'Drainage', 'PEquipment', 'JTape'}
OTHER = {'ACrack', 'Wetspot', 'Rockpocket', 'Hollowareas', 'Cavity', 'Graffiti', 'Weathering', 'Restformwork', 'ExposedRebars', 'WConccor'}
p = argparse.ArgumentParser()
p.add_argument('--src', default='/home/skye/data/Skye/databases/dacl10k_v3_512/extracted')
p.add_argument('--out', default='/home/skye/data/Skye/databases/Bridge512_dacl10k_val4')
p.add_argument('--view', default='data_views_dacl10k')
a = p.parse_args()
src = Path(a.src); out = Path(a.out); view = Path(a.view).resolve(); T = out / 'test'
for d in (T / 'normal', T / 'annotated', T / 'multiclass_annotations' / 'masks', view / 'test' / 'masks_union'): d.mkdir(parents=True, exist_ok=True)
rows = []; meta = []; stats = {'anomaly': 0, 'normal': 0, 'excluded_other_damage': 0, 'per_class_images': {c: 0 for c in PALETTE}, 'per_class_pixels': {c: 0 for c in PALETTE}}
def link(s, d):
    if d.is_symlink() or d.exists(): d.unlink()
    os.symlink(s, d)
for f in sorted((src / 'dacl10k_v3_devphase_annotations_512' / 'validation').glob('*.json')):
    d = json.loads(f.read_text()); st = {s['label'] for s in d['shapes']}
    unknown = st - set(MAP) - OBJECTS - OTHER
    if unknown: raise SystemExit(f'unknown labels {unknown} in {f.name}')
    img = src / 'images' / 'valid' / d['imageName']; sample = 'dacl10k_val_' + Path(d['imageName']).stem
    if st & OTHER: stats['excluded_other_damage'] += 1; continue
    if not st & set(MAP):
        link(img, T / 'normal' / (sample + '.jpg')); stats['normal'] += 1
        rows.append({'sample': sample, 'parent_id': 'dacl10k:' + sample, 'category': 'normal', 'labels': '', 'image_path': f'normal/{sample}.jpg', 'mask_path': ''})
        meta.append({'img_path': str(img), 'mask_path': '', 'anomaly': 0, 'cls_name': 'structural defects', 'specie_name': '', 'labels': [], 'parent_id': 'dacl10k:' + sample}); continue
    W, H = d['imageWidth'], d['imageHeight']; masks = {}
    for c_src, c in MAP.items():
        m = Image.new('L', (W, H), 0); dr = ImageDraw.Draw(m)
        for s in d['shapes']:
            if s['label'] == c_src and len(s['points']) >= 3: dr.polygon([(float(x), float(y)) for x, y in s['points']], fill=255)
        masks[c] = np.asarray(m) > 0
    present = [c for c in PALETTE if masks[c].any()]
    if not present: stats['excluded_other_damage'] += 1; continue          # degenerate polygons only
    rgb = np.zeros((H, W, 3), np.uint8)
    for c in ORDER: rgb[masks[c]] = PALETTE[c]
    for c in PALETTE:
        Image.fromarray((masks[c] * 255).astype(np.uint8)).save(T / 'multiclass_annotations' / 'masks' / f'{sample}__{c}.png')
        if masks[c].any(): stats['per_class_images'][c] += 1; stats['per_class_pixels'][c] += int(masks[c].sum())
    link(img, T / 'annotated' / (sample + '.jpg')); Image.fromarray(rgb).save(T / 'annotated' / (sample + '.png'))
    up = view / 'test' / 'masks_union' / (sample + '.png'); Image.fromarray(((rgb.sum(-1) > 0) * 255).astype(np.uint8)).save(up)
    stats['anomaly'] += 1
    rows.append({'sample': sample, 'parent_id': 'dacl10k:' + sample, 'category': 'annotated', 'labels': ';'.join(present), 'image_path': f'annotated/{sample}.jpg', 'mask_path': f'annotated/{sample}.png'})
    meta.append({'img_path': str(img), 'mask_path': str(up), 'anomaly': 1, 'cls_name': 'structural defects', 'specie_name': 'defect', 'labels': present, 'parent_id': 'dacl10k:' + sample})
with (out / 'test_manifest.csv').open('w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
(view / 'test' / 'meta.json').write_text(json.dumps({'train': {}, 'test': {'structural defects': meta}}, indent=1))
stats['total'] = len(rows); stats['source'] = 'dacl10k v3 512 official validation (975 images), strict four-class subset'
(out / 'summary.json').write_text(json.dumps(stats, indent=2)); (view / 'summary.json').write_text(json.dumps(stats, indent=2))
print(json.dumps(stats, indent=2))
