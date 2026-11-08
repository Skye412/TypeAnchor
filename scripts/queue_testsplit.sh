#!/usr/bin/env bash
# Main-table evaluation on the untouched CODEBRIM test split (809 tiles: 254 with defects / 555 normal).  Inference only, every
# checkpoint as selected or fixed during development on the val split.  Outputs <run>/test-* with metrics_nuisance.py and
# metrics_multiclass.py (P-AUPRO on the GPU), then compare_fp.py for the false-alarm area at matched recall.
# Usage: nohup bash scripts/queue_testsplit.sh > runs/queue_testsplit.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
PY=/home/skye/miniconda3/envs/adaptclip/bin/python; SEGPY=/home/skye/miniconda3/envs/MixerCSeg/bin/python
WPPY=/home/skye/miniconda3/envs/wpformer/bin/python; MXPY=/home/skye/miniconda3/envs/MixerCSeg/bin/python
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
C=/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM
stamp(){ echo "=== $(date '+%F %T') $*"; }
mc(){ $PY metrics_multiclass.py "$@" --aupro-device hybrid; }   # CCA on the GPU, ROC on the CPU: 809 tiles do not fit the GPU
metrics(){ $PY metrics_nuisance.py $1 test >> $1.log 2>&1 && mc --run $1 --split test >> $1.log 2>&1; }
ours(){ # $1 run dir, $2 epoch
  out=$1/test-epoch$2; stamp START $out
  $PY eval_nuisance.py --checkpoint $1/epoch_$2.pth --out $out --split test --save-typed > $out.log 2>&1 && metrics $out && stamp DONE $out || stamp FAILED $out
}
# our method: final model (3 seeds) and the component ablations (seed 10)
for r in ablation-v2-no-nuisance ablation-v2-no-nuisance-s11 ablation-v2-no-nuisance-s12 abl-v2-no-nu-gate abl-v2-gamma0 abl-v2-gamma1 abl-v2-no-residual nuisance-v2 nuisance-v0; do ours runs/$r 20; done
# AdaptCLIP baseline, metrics on the GPU (same P-AUPRO implementation as the other rows)
out=runs/baseline-v1/test-zero-gpu; mkdir -p $out; stamp START $out
EVAL_DEVICE=cpu SAVE_MAPS=1 $PY test.py --dataset codebrim --checkpoint_path runs/baseline-v1/epoch_15.pth --features_list 6 12 18 24 --image_size 518 --batch_size 4 --n_ctx 12 --vl_reduction 4 --pq_mid_dim 128 --visual_learner --textual_learner --pq_learner --pq_context --seed 10 --k_shots 0 \
  --test_data_path data_views/test --save_path $out --eval_metrics I-AUROC I-AP I-F1max P-AUROC P-AP P-F1max > $out/console.log 2>&1 && metrics $out && stamp DONE $out || stamp FAILED $out
# CLIP-based comparisons
for m in anomalyclip bayespfl; do out=runs/ext-$m/test; stamp START $out
  $PY eval_external_$m.py --out $out --split test > $out.log 2>&1 && metrics $out && stamp DONE $out || stamp FAILED $out; done
out=runs/ext-multiads/test; stamp START $out
$PY multiads_bridge.py eval --checkpoint runs/ext-multiads/epoch_10.pth --out $out --split test > $out.log 2>&1 && metrics $out && stamp DONE $out || stamp FAILED $out
# fully supervised comparisons
out=runs/segformer-b2/test-epoch40; stamp START $out
$SEGPY train_segformer.py --out runs/segformer-b2 --eval-only --split test --eval-out $out > $out.log 2>&1 && metrics $out && stamp DONE $out || stamp FAILED $out
out=runs/ext-wpformer/test; stamp START $out
$WPPY eval_external_seg.py wpformer --out $out --split test > $out.log 2>&1 && metrics $out && stamp DONE $out || stamp FAILED $out
out=runs/ext-mixercseg/test; stamp START $out
$MXPY eval_external_seg.py mixercseg --out $out --split test > $out.log 2>&1 && metrics $out && stamp DONE $out || stamp FAILED $out
# false-alarm area at matched recall
stamp START compare_fp test
$PY compare_fp.py runs/ablation-v2-no-nuisance/test-epoch20 runs/ablation-v2-no-nuisance-s11/test-epoch20 runs/ablation-v2-no-nuisance-s12/test-epoch20 runs/abl-v2-no-nu-gate/test-epoch20 runs/abl-v2-gamma0/test-epoch20 runs/abl-v2-gamma1/test-epoch20 runs/abl-v2-no-residual/test-epoch20 runs/nuisance-v2/test-epoch20 runs/nuisance-v0/test-epoch20 runs/segformer-b2/test-epoch40 runs/ext-anomalyclip/test runs/ext-bayespfl/test runs/ext-multiads/test runs/ext-wpformer/test runs/ext-mixercseg/test --split test --suffix _test > runs/compare_fp_test.log 2>&1 && stamp DONE compare_fp || stamp FAILED compare_fp
stamp QUEUE_DONE
