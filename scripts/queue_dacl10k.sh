#!/usr/bin/env bash
# Second cross-dataset test: dacl10k v3 official validation, strict four-class subset (207 anomaly / 55 normal,
# built by scripts/prepare_dacl10k.py). All models are trained on CODEBRIM only; references for v0 / v2 are the
# CODEBRIM training normals; baseline runs zero-shot (k_shots=0).
# Usage: nohup bash scripts/queue_dacl10k.sh > runs/queue_dacl10k.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
ADPY=/home/skye/miniconda3/envs/adaptclip/bin/python
SEGPY=/home/skye/miniconda3/envs/MixerCSeg/bin/python
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
D=/home/skye/data/Skye/databases/Bridge512_dacl10k_val4
stamp(){ echo "=== $(date '+%F %T') $*"; }
metrics(){ # $1 run dir
  $ADPY metrics_nuisance.py "$1" test --data $D >> "$1.log" 2>&1 \
  && { $ADPY metrics_multiclass.py --run "$1" --data $D --split test --aupro-device cuda >> "$1.log" 2>&1 || $ADPY metrics_multiclass.py --run "$1" --data $D --split test >> "$1.log" 2>&1; }
}
for m in ablation-v2-no-nuisance nuisance-v0; do
  out=runs/$m/dacl10k-test; stamp START $out
  $ADPY eval_nuisance.py --checkpoint runs/$m/epoch_20.pth --out $out --data $D --split test --save-typed > $out.log 2>&1 && metrics $out && stamp DONE $out || stamp FAILED $out
done
out=runs/ablation-v2-no-nuisance/dacl10k-test-ref1; stamp START $out
$ADPY eval_nuisance.py --checkpoint runs/ablation-v2-no-nuisance/epoch_20.pth --out $out --data $D --split test --save-typed --ref-subset 1 --ref-seed 10 > $out.log 2>&1 && metrics $out && stamp DONE $out || stamp FAILED $out
out=runs/segformer-b2/dacl10k-test; stamp START $out
$SEGPY train_segformer.py --out runs/segformer-b2 --eval-only --eval-data $D --split test --eval-out $out > $out.log 2>&1 && metrics $out && stamp DONE $out || stamp FAILED $out
$ADPY compare_fp.py runs/ablation-v2-no-nuisance/dacl10k-test runs/nuisance-v0/dacl10k-test runs/segformer-b2/dacl10k-test --data $D --split test --suffix _dacl10k > runs/compare_fp_dacl10k.log 2>&1 && stamp DONE compare_fp
mkdir -p runs/baseline-v1/dacl10k-test-zero; stamp START baseline zero-shot
$ADPY test.py --dataset codebrim --checkpoint_path runs/baseline-v1/epoch_15.pth --features_list 6 12 18 24 --image_size 518 --batch_size 4 --n_ctx 12 --vl_reduction 4 --pq_mid_dim 128 --visual_learner --textual_learner --pq_learner --pq_context --seed 10 --k_shots 0 \
  --test_data_path data_views_dacl10k/test --save_path runs/baseline-v1/dacl10k-test-zero > runs/baseline-v1/dacl10k-test-zero/console.log 2>&1 && stamp DONE baseline zero-shot || stamp FAILED baseline zero-shot
stamp QUEUE_DONE
