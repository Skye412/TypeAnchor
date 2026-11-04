#!/usr/bin/env bash
# Cross-dataset S2DS evaluation (route A, P5). Two tiers so that all three models share one protocol:
#   all   = all 2,226 S2DS tiles: I/P-AUROC, AP, F1 (no AUPRO; the baseline evaluator was OOM-killed with AUPRO on 2,226)
#   test  = original S2DS test split (447 tiles: 73 normal / 374 anomaly): all metrics incl. P-AUPRO and per-class
# References for v0 / v2 remain the CODEBRIM training normals (zero-shot w.r.t. S2DS); baseline runs with k_shots=0.
# Usage: nohup bash scripts/queue_s2ds.sh > runs/queue_s2ds.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
source /home/skye/miniconda3/etc/profile.d/conda.sh
conda activate adaptclip
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
S=/home/skye/data/Skye/databases/Bridge512_balance_S2DS_all
EX=s2ds_exclude_trainval.txt
stamp(){ echo "=== $(date '+%F %T') $*"; }
BASE="--dataset codebrim --checkpoint_path runs/baseline-v1/epoch_15.pth --features_list 6 12 18 24 --image_size 518 --batch_size 4 --n_ctx 12 --vl_reduction 4 --pq_mid_dim 128 --visual_learner --textual_learner --pq_learner --pq_context --seed 10 --k_shots 0"
# 1. baseline on the test split, full metrics
mkdir -p runs/baseline-v1/s2ds-test-zero
stamp START baseline test-split
python test.py $BASE --test_data_path data_views_s2ds_splits/test --save_path runs/baseline-v1/s2ds-test-zero > runs/baseline-v1/s2ds-test-zero/console.log 2>&1 && stamp DONE baseline test-split || stamp FAILED baseline test-split
# 2. our models on all tiles, then two-tier metrics
evalx(){ # $1 checkpoint $2 out
  stamp START $2
  python eval_nuisance.py --checkpoint "$1" --out "$2" --data $S --split all --save-typed > "$2.log" 2>&1 \
  && python metrics_nuisance.py "$2" all --data $S >> "$2.log" 2>&1 \
  && python metrics_multiclass.py --run "$2" --data $S --split all --skip-aupro >> "$2.log" 2>&1 \
  && python metrics_nuisance.py "$2" all --data $S --exclude $EX --suffix _test >> "$2.log" 2>&1 \
  && python metrics_multiclass.py --run "$2" --data $S --split all --exclude $EX --suffix _test >> "$2.log" 2>&1 \
  && stamp DONE $2 || stamp FAILED $2
}
evalx runs/nuisance-v0/epoch_20.pth runs/nuisance-v0/s2ds-all
evalx runs/ablation-v2-no-nuisance/epoch_20.pth runs/ablation-v2-no-nuisance/s2ds-all
python compare_fp.py runs/nuisance-v0/s2ds-all runs/ablation-v2-no-nuisance/s2ds-all --data $S --split all --suffix _s2ds_all > runs/compare_fp_s2ds_all.log 2>&1 && stamp DONE compare_fp all
python compare_fp.py runs/nuisance-v0/s2ds-all runs/ablation-v2-no-nuisance/s2ds-all --data $S --split all --exclude $EX --suffix _s2ds_test > runs/compare_fp_s2ds_test.log 2>&1 && stamp DONE compare_fp test
# 3. baseline on all tiles without AUPRO (may still be memory-heavy; last so nothing else depends on it)
mkdir -p runs/baseline-v1/s2ds-all-zero
stamp START baseline all
python test.py $BASE --test_data_path data_views_s2ds/val --save_path runs/baseline-v1/s2ds-all-zero --eval_metrics I-AUROC I-AP I-F1max P-AUROC P-AP P-F1max > runs/baseline-v1/s2ds-all-zero/console.log 2>&1 && stamp DONE baseline all || stamp FAILED baseline all
stamp QUEUE_DONE
