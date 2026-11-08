#!/usr/bin/env bash
# Serial re-run of the three metric steps that OOMed when queue_extra_baselines.sh and queue_zeroshot_rerun.sh computed
# P-AUPRO at the same time.  Usage: nohup bash scripts/queue_extra_rerun.sh > runs/queue_extra_rerun.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
PY=/home/skye/miniconda3/envs/adaptclip/bin/python
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
C=/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM; S=/home/skye/data/Skye/databases/Bridge512_balance_S2DS
stamp(){ echo "=== $(date '+%F %T') $*"; }
metrics(){ $PY metrics_nuisance.py $1 $2 --data $3 >> $1.log 2>&1 && $PY metrics_multiclass.py --run $1 --split $2 --data $3 --aupro-device $4 >> $1.log 2>&1; }
for spec in "runs/zeroshot-clip/test test $C hybrid" "runs/deeplabv3-r50/test-epoch40 test $C hybrid" "runs/deeplabv3-r50/s2ds-test test $S cuda"; do
  set -- $spec; stamp START $1; metrics $1 $2 $3 $4 && stamp DONE $1 || stamp FAILED $1
done
stamp QUEUE_DONE
