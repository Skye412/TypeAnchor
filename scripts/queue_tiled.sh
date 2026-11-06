#!/usr/bin/env bash
# Crack resolution diagnostic: tiled inference of the final model (6-anchor v2, seed 10) on CODEBRIM val, no retraining.
# Usage: nohup bash scripts/queue_tiled.sh > runs/queue_tiled.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
PY=/home/skye/miniconda3/envs/adaptclip/bin/python
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
CK=runs/ablation-v2-no-nuisance/epoch_20.pth; EX=eval_exclude_normals.txt
stamp(){ echo "=== $(date '+%F %T') $*"; }
while pgrep -f "[q]ueue_dacl10k.sh" > /dev/null; do sleep 20; done      # one inference job on the GPU at a time
run(){ # $1 out, rest: extra args
  local out=$1; shift; stamp START $out
  $PY eval_tiled.py --checkpoint $CK --out $out "$@" > $out.log 2>&1 \
  && $PY metrics_nuisance.py $out >> $out.log 2>&1 && $PY metrics_nuisance.py $out --exclude $EX --suffix _clean >> $out.log 2>&1 \
  && { $PY metrics_multiclass.py --run $out --aupro-device cuda >> $out.log 2>&1 || $PY metrics_multiclass.py --run $out >> $out.log 2>&1; } \
  && { $PY metrics_multiclass.py --run $out --exclude $EX --suffix _clean --aupro-device cuda >> $out.log 2>&1 || $PY metrics_multiclass.py --run $out --exclude $EX --suffix _clean >> $out.log 2>&1; } \
  && stamp DONE $out || stamp FAILED $out
}
run runs/ablation-v2-no-nuisance/val-tiled2
run runs/ablation-v2-no-nuisance/val-tiled2-blend --blend 0.5
run runs/ablation-v2-no-nuisance/val-tiled2-tilerefs --tile-refs
stamp QUEUE_DONE
