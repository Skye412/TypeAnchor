#!/usr/bin/env bash
# Closing experiments for route A (docs/results.md §2e.2):
#  1. cross-dataset S2DS (all 2226 tiles, references = CODEBRIM training normals, zero-shot w.r.t. S2DS):
#     baseline-v1 (official test.py), nuisance-v0, v2-no-nuisance (final model)
#  2. component ablations on the 6-anchor v2 (seed 10): no nu gating; gamma fixed 0 (regional) / 1 (local)
# Usage: nohup bash scripts/queue_final.sh > runs/queue_final.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
source /home/skye/miniconda3/etc/profile.d/conda.sh
conda activate adaptclip
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
C=/home/skye/data/Skye/feature_cache
S=/home/skye/data/Skye/databases/Bridge512_balance_S2DS_all
stamp(){ echo "=== $(date '+%F %T') $*"; }
evalx(){ # $1 checkpoint $2 out dir
  stamp START $2
  python eval_nuisance.py --checkpoint "$1" --out "$2" --data $S --split all --save-typed > "$2.log" 2>&1 \
  && python metrics_nuisance.py "$2" all --data $S >> "$2.log" 2>&1 \
  && python metrics_multiclass.py --run "$2" --data $S --split all >> "$2.log" 2>&1 \
  && stamp DONE $2 || stamp FAILED $2
}
mkdir -p runs/baseline-v1/s2ds-zero
stamp START runs/baseline-v1/s2ds-zero
python test.py --dataset codebrim --test_data_path data_views_s2ds/val --save_path runs/baseline-v1/s2ds-zero --checkpoint_path runs/baseline-v1/epoch_15.pth \
  --features_list 6 12 18 24 --image_size 518 --batch_size 4 --n_ctx 12 --vl_reduction 4 --pq_mid_dim 128 --visual_learner --textual_learner --pq_learner --pq_context --seed 10 --k_shots 0 \
  > runs/baseline-v1/s2ds-zero/console.log 2>&1 && stamp DONE runs/baseline-v1/s2ds-zero || stamp FAILED runs/baseline-v1/s2ds-zero
evalx runs/nuisance-v0/epoch_20.pth runs/nuisance-v0/s2ds-all
evalx runs/ablation-v2-no-nuisance/epoch_20.pth runs/ablation-v2-no-nuisance/s2ds-all
python compare_fp.py runs/nuisance-v0/s2ds-all runs/ablation-v2-no-nuisance/s2ds-all --data $S --split all --suffix _s2ds > runs/compare_fp_s2ds.log 2>&1 && stamp DONE compare_fp_s2ds
run(){ stamp START $2; bash scripts/train_ablation.sh "$@" > "$2/console.log" 2>&1 && stamp DONE $2 || stamp FAILED $2; }
mkdir -p runs/abl-v2-no-nu-gate runs/abl-v2-gamma0 runs/abl-v2-gamma1
run no-nuisance runs/abl-v2-no-nu-gate --arch v2 --cache-dir $C --no-nu-gate
run no-nuisance runs/abl-v2-gamma0 --arch v2 --cache-dir $C --gamma-fixed 0
run no-nuisance runs/abl-v2-gamma1 --arch v2 --cache-dir $C --gamma-fixed 1
stamp QUEUE_DONE
