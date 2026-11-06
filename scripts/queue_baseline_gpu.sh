#!/usr/bin/env bash
# Recompute the AdaptCLIP baseline (baseline-v1, zero-shot) with the metrics on the GPU, so that its P-AUPRO uses the same
# connected-components implementation as our runs (metrics_multiclass.py --aupro-device cuda). CPU and GPU differ by several points.
# Usage: nohup bash scripts/queue_baseline_gpu.sh > runs/queue_baseline_gpu.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
PY=/home/skye/miniconda3/envs/adaptclip/bin/python
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1 EVAL_DEVICE=cuda
stamp(){ echo "=== $(date '+%F %T') $*"; }
BASE="--dataset codebrim --checkpoint_path runs/baseline-v1/epoch_15.pth --features_list 6 12 18 24 --image_size 518 --batch_size 4 --n_ctx 12 --vl_reduction 4 --pq_mid_dim 128 --visual_learner --textual_learner --pq_learner --pq_context --seed 10 --k_shots 0"
one(){ # $1 test data view, $2 out dir
  mkdir -p $2; stamp START $2
  $PY test.py $BASE --test_data_path $1 --save_path $2 > $2/console.log 2>&1 && stamp DONE $2 || stamp FAILED $2
}
one data_views/val runs/baseline-v1/val-zero-gpu
one data_views_s2ds_splits/test runs/baseline-v1/s2ds-test-zero-gpu
one data_views_dacl10k/test runs/baseline-v1/dacl10k-test-zero-gpu
stamp QUEUE_DONE
