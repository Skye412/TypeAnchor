#!/usr/bin/env bash
# Re-run of the parts of scripts/queue_external_seg.sh and scripts/queue_testsplit.sh that failed on 2026-11-08: MixerCSeg could not run
# under autocast (fp32 now), and P-AUPRO of the 809-tile test split ran out of GPU memory (now --aupro-device hybrid).  Inference
# outputs that already exist are reused; only the metrics are recomputed for them.
set -uo pipefail
cd "$(dirname "$0")/.."
PY=/home/skye/miniconda3/envs/adaptclip/bin/python; MXPY=/home/skye/miniconda3/envs/MixerCSeg/bin/python
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
C=/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM; S=/home/skye/data/Skye/databases/Bridge512_balance_S2DS; D=/home/skye/data/Skye/databases/Bridge512_dacl10k_val4
EX=eval_exclude_normals.txt
stamp(){ echo "=== $(date '+%F %T') $*"; }
mc(){ $PY metrics_multiclass.py "$@" --aupro-device cuda; }
mch(){ $PY metrics_multiclass.py "$@" --aupro-device hybrid; }
metrics_test(){ $PY metrics_nuisance.py $1 test >> $1.log 2>&1 && mch --run $1 --split test >> $1.log 2>&1; }
# --- MixerCSeg: val (raw + Cleaned-Val), S2DS, dacl10k, fp32 inference
R=runs/ext-mixercseg; out=$R/val; stamp START $out
$MXPY eval_external_seg.py mixercseg --out $out > $out.log 2>&1 \
 && $PY metrics_nuisance.py $out >> $out.log 2>&1 && mc --run $out >> $out.log 2>&1 \
 && $PY metrics_nuisance.py $out --exclude $EX --suffix _clean >> $out.log 2>&1 && mc --run $out --exclude $EX --suffix _clean >> $out.log 2>&1 \
 && stamp DONE $out || stamp FAILED $out
for pair in "s2ds-test $S" "dacl10k-test $D"; do set -- $pair; out=$R/$1; d=$2; stamp START $out
  $MXPY eval_external_seg.py mixercseg --out $out --data $d --split test > $out.log 2>&1 \
  && $PY metrics_nuisance.py $out test --data $d >> $out.log 2>&1 && mc --run $out --data $d --split test >> $out.log 2>&1 \
  && stamp DONE $out || stamp FAILED $out; done
# --- test split: metrics only, inference already on disk
for out in runs/ablation-v2-no-nuisance/test-epoch20 runs/ablation-v2-no-nuisance-s11/test-epoch20 runs/ablation-v2-no-nuisance-s12/test-epoch20 runs/abl-v2-no-nu-gate/test-epoch20 runs/abl-v2-gamma0/test-epoch20 runs/abl-v2-gamma1/test-epoch20 runs/abl-v2-no-residual/test-epoch20 runs/nuisance-v2/test-epoch20 runs/nuisance-v0/test-epoch20 runs/ext-anomalyclip/test runs/ext-bayespfl/test runs/ext-multiads/test runs/segformer-b2/test-epoch40 runs/ext-wpformer/test; do
  stamp START metrics $out; [ "$(ls $out/maps | wc -l)" = 809 ] && metrics_test $out && stamp DONE $out || stamp FAILED $out; done
# --- MixerCSeg test: inference + metrics
out=runs/ext-mixercseg/test; stamp START $out
$MXPY eval_external_seg.py mixercseg --out $out --split test > $out.log 2>&1 && metrics_test $out && stamp DONE $out || stamp FAILED $out
# --- AdaptCLIP baseline test: image/pixel metrics by its own evaluator on the CPU, maps saved, P-AUPRO by metrics_multiclass (hybrid)
out=runs/baseline-v1/test-zero-gpu; mkdir -p $out; stamp START $out
EVAL_DEVICE=cpu SAVE_MAPS=1 $PY test.py --dataset codebrim --checkpoint_path runs/baseline-v1/epoch_15.pth --features_list 6 12 18 24 --image_size 518 --batch_size 4 --n_ctx 12 --vl_reduction 4 --pq_mid_dim 128 --visual_learner --textual_learner --pq_learner --pq_context --seed 10 --k_shots 0 \
  --test_data_path data_views/test --save_path $out --eval_metrics I-AUROC I-AP I-F1max P-AUROC P-AP P-F1max > $out/console.log 2>&1 && metrics_test $out && stamp DONE $out || stamp FAILED $out
# --- false-alarm area at matched recall
stamp START compare_fp test
$PY compare_fp.py runs/ablation-v2-no-nuisance/test-epoch20 runs/ablation-v2-no-nuisance-s11/test-epoch20 runs/ablation-v2-no-nuisance-s12/test-epoch20 runs/abl-v2-no-nu-gate/test-epoch20 runs/abl-v2-gamma0/test-epoch20 runs/abl-v2-gamma1/test-epoch20 runs/abl-v2-no-residual/test-epoch20 runs/nuisance-v2/test-epoch20 runs/nuisance-v0/test-epoch20 runs/segformer-b2/test-epoch40 runs/ext-anomalyclip/test runs/ext-bayespfl/test runs/ext-multiads/test runs/ext-wpformer/test runs/ext-mixercseg/test runs/baseline-v1/test-zero-gpu --split test --suffix _test > runs/compare_fp_test.log 2>&1 && stamp DONE compare_fp || stamp FAILED compare_fp
stamp QUEUE_DONE
