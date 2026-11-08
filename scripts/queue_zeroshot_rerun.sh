#!/usr/bin/env bash
# Re-run of the zero-shot CLIP items of scripts/queue_extra_baselines.sh (first attempt failed on an anchor-name assertion).
# Inference runs at once (light); the metrics wait until the DeepLabV3 training in the other queue has finished, so the
# P-AUPRO computation does not compete for GPU memory.  Usage: nohup bash scripts/queue_zeroshot_rerun.sh > runs/queue_zeroshot_rerun.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
PY=/home/skye/miniconda3/envs/adaptclip/bin/python
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
C=/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM; S=/home/skye/data/Skye/databases/Bridge512_balance_S2DS; D=/home/skye/data/Skye/databases/Bridge512_dacl10k_val4
EX=eval_exclude_normals.txt
stamp(){ echo "=== $(date '+%F %T') $*"; }
mc(){ $PY metrics_multiclass.py "$@"; }
metrics(){ $PY metrics_nuisance.py $1 $2 --data $3 >> $1.log 2>&1 && mc --run $1 --split $2 --data $3 --aupro-device $4 >> $1.log 2>&1; }
metrics_val(){ $PY metrics_nuisance.py $1 >> $1.log 2>&1 && mc --run $1 --aupro-device cuda >> $1.log 2>&1 \
  && $PY metrics_nuisance.py $1 --exclude $EX --suffix _clean >> $1.log 2>&1 && mc --run $1 --exclude $EX --suffix _clean --aupro-device cuda >> $1.log 2>&1; }
R=runs/zeroshot-clip; mkdir -p $R
stamp START inference
$PY eval_zeroshot.py --out $R/val > $R/val.log 2>&1 && stamp DONE infer val || stamp FAILED infer val
$PY eval_zeroshot.py --out $R/test --split test > $R/test.log 2>&1 && stamp DONE infer test || stamp FAILED infer test
$PY eval_zeroshot.py --out $R/s2ds-test --data $S --split test > $R/s2ds-test.log 2>&1 && stamp DONE infer s2ds || stamp FAILED infer s2ds
$PY eval_zeroshot.py --out $R/dacl10k-test --data $D --split test > $R/dacl10k-test.log 2>&1 && stamp DONE infer dacl10k || stamp FAILED infer dacl10k
stamp WAITING for DeepLab training to finish
while ! grep -qE "(DONE|FAILED) train runs/deeplabv3-r50" runs/queue_extra_baselines.log; do sleep 120; done
stamp START metrics
metrics_val $R/val && stamp DONE $R/val || stamp FAILED $R/val
metrics $R/test test $C hybrid && stamp DONE $R/test || stamp FAILED $R/test
metrics $R/s2ds-test test $S cuda && stamp DONE $R/s2ds-test || stamp FAILED $R/s2ds-test
metrics $R/dacl10k-test test $D cuda && stamp DONE $R/dacl10k-test || stamp FAILED $R/dacl10k-test
stamp QUEUE_DONE
