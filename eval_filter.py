"""Shared helper: optional exclusion list for the Cleaned-Val protocol (docs/results.md §2d.1).
The list file holds one sample name per line (comments with #). Rows whose sample is listed are dropped.
"""
from pathlib import Path
import numpy as np
from PIL import Image

def load_exclude(path):
 if not path: return set()
 return {l.split('#')[0].strip() for l in Path(path).read_text(encoding='utf-8').splitlines() if l.split('#')[0].strip()}

def filter_rows(rows,exclude):
 if not exclude: return rows
 return [r for r in rows if r['sample'] not in exclude]

def union_mask(path,size=518):
 """Binary union GT at `size`: any non-black pixel of the flattened RGB mask, resized bilinear and thresholded at 127.
 Identical to the baseline's masks_union (scripts/prepare_codebrim.py) followed by its preprocessing.
 Do NOT use convert('L')>127 on the RGB mask: red (crack) maps to 76 and blue (corrosion) to 29, i.e. to background."""
 rgb=np.asarray(Image.open(path).convert('RGB')); u=Image.fromarray(((rgb.sum(-1)>0)*255).astype(np.uint8))
 return np.asarray(u.resize((size,size),Image.Resampling.BILINEAR))>127
