#!/usr/bin/env bash
# Train a variant of the nuisance-aware head with the same seed/epochs/bank as nuisance-v0, then evaluate it on validation
# under both the raw protocol and the Cleaned-Val protocol (eval_exclude_normals.txt).
# Usage: bash scripts/train_ablation.sh <anchor-set> <out-dir> [extra train_nuisance.py args...]
#   e.g. bash scripts/train_ablation.sh no-nuisance runs/ablation-no-nuisance
#        bash scripts/train_ablation.sh v2 runs/nuisance-v2 --arch v2 --cache-dir /home/skye/data/Skye/feature_cache
set -euo pipefail
cd "$(dirname "$0")/.."
source /home/skye/miniconda3/etc/profile.d/conda.sh
conda activate adaptclip
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
SET=${1:?anchor set}; OUT=${2:?out dir}; shift 2
mkdir -p "$OUT"; git rev-parse HEAD > "$OUT/revision.txt"; git status --short > "$OUT/dirty.txt" || true
python train_nuisance.py --anchor-set "$SET" --out "$OUT" --epochs 20 --seed 10 --bank runs/nuisance-v0/normal_globals.pt "$@"
python eval_nuisance.py --checkpoint "$OUT/epoch_20.pth" --out "$OUT/val-epoch20" --save-typed
python metrics_nuisance.py "$OUT/val-epoch20"
python metrics_multiclass.py --run "$OUT/val-epoch20"
python metrics_nuisance.py "$OUT/val-epoch20" --exclude eval_exclude_normals.txt --suffix _clean
python metrics_multiclass.py --run "$OUT/val-epoch20" --exclude eval_exclude_normals.txt --suffix _clean
echo ABLATION_DONE
