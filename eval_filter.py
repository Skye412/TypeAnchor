"""Shared helper: optional exclusion list for the Cleaned-Val protocol (docs/results.md §2d.1).
The list file holds one sample name per line (comments with #). Rows whose sample is listed are dropped.
"""
from pathlib import Path

def load_exclude(path):
 if not path: return set()
 return {l.split('#')[0].strip() for l in Path(path).read_text(encoding='utf-8').splitlines() if l.split('#')[0].strip()}

def filter_rows(rows,exclude):
 if not exclude: return rows
 return [r for r in rows if r['sample'] not in exclude]
