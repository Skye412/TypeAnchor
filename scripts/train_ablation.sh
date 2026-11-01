#!/usr/bin/env bash
# Train an anchor-set ablation of the nuisance-aware head with the same seed/epochs/bank as nuisance-v0,
# then evaluate it on the validation split.
# Usage: bash scripts/train_ablation.sh <anchor-set> <out-dir>    e.g. no-nuisance runs/ablation-no-nuisance
set -euo pipefail
cd "$(dirname "$0")/.."
source /home/skye/miniconda3/etc/profile.d/conda.sh
conda activate adaptclip
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
SET=${1:?anchor set}; OUT=${2:?out dir}
mkdir -p "$OUT"; git rev-parse HEAD > "$OUT/revision.txt"; git status --short > "$OUT/dirty.txt" || true
python train_nuisance.py --anchor-set "$SET" --out "$OUT" --epochs 20 --seed 10 --bank runs/nuisance-v0/normal_globals.pt
python eval_nuisance.py --checkpoint "$OUT/epoch_20.pth" --out "$OUT/val-epoch20" --save-typed
python metrics_nuisance.py "$OUT/val-epoch20"
python metrics_multiclass.py --run "$OUT/val-epoch20"
echo ABLATION_DONE
