#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
source /home/skye/miniconda3/etc/profile.d/conda.sh
conda activate adaptclip
export CUDA_VISIBLE_DEVICES=0
export PYTHONUNBUFFERED=1
mkdir -p runs/baseline-v1
# User requires an uploaded revision before every full training.
git diff --exit-code
git diff --cached --exit-code
test -z "$(git ls-files --others --exclude-standard)"
git push origin HEAD
 git rev-parse HEAD > runs/baseline-v1/revision.txt
conda list --explicit > runs/baseline-v1/environment.txt
python train.py --dataset codebrim --train_data_path data_views/train --save_path runs/baseline-v1 --features_list 6 12 18 24 --image_size 518 --batch_size 8 --epoch 15 --save_freq 1 --n_ctx 12 --vl_reduction 4 --pq_mid_dim 128 --visual_learner --textual_learner --pq_learner --pq_context --seed 10
