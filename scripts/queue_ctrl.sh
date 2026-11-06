#!/usr/bin/env bash
# Control for scripts/queue_detail.sh: the final model (6-anchor v2, seed 10) fine-tuned 10 more epochs from its epoch 20
# with the full v2 loss and WITHOUT the detail branch, to tell whether the cross-dataset changes of v2-detail-joint come from extra training.
# Usage: nohup bash scripts/queue_ctrl.sh > runs/queue_ctrl.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
PY=/home/skye/miniconda3/envs/adaptclip/bin/python
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
C=/home/skye/data/Skye/feature_cache; INIT=runs/ablation-v2-no-nuisance/epoch_20.pth; EX=eval_exclude_normals.txt
S=/home/skye/data/Skye/databases/Bridge512_balance_S2DS; D=/home/skye/data/Skye/databases/Bridge512_dacl10k_val4
stamp(){ echo "=== $(date '+%F %T') $*"; }
mc(){ $PY metrics_multiclass.py "$@" --aupro-device cuda || $PY metrics_multiclass.py "$@"; }
evalset(){ # $1 checkpoint, $2 out dir, $3 data root ('' = CODEBRIM val), $4 split
  local ck=$1 out=$2 d=${3:-} sp=${4:-val}; stamp START $out
  if [ -z "$d" ]; then
    $PY eval_nuisance.py --checkpoint $ck --out $out --save-typed > $out.log 2>&1 \
    && $PY metrics_nuisance.py $out >> $out.log 2>&1 && mc --run $out >> $out.log 2>&1 \
    && $PY metrics_nuisance.py $out --exclude $EX --suffix _clean >> $out.log 2>&1 && mc --run $out --exclude $EX --suffix _clean >> $out.log 2>&1 \
    && stamp DONE $out || stamp FAILED $out
  else
    $PY eval_nuisance.py --checkpoint $ck --out $out --data $d --split $sp --save-typed > $out.log 2>&1 \
    && $PY metrics_nuisance.py $out $sp --data $d >> $out.log 2>&1 && mc --run $out --data $d --split $sp >> $out.log 2>&1 \
    && stamp DONE $out || stamp FAILED $out
  fi
}
run(){ # $1 out dir, $2 epochs, rest: extra training args
  local out=$1 ep=$2; shift 2; mkdir -p $out; git rev-parse HEAD > $out/revision.txt; git status --short > $out/dirty.txt
  stamp TRAIN $out
  $PY train_nuisance.py --anchor-set no-nuisance --arch v2 --cache-dir $C --bank runs/nuisance-v0/normal_globals.pt --seed 10 --out $out --epochs $ep --init $INIT "$@" > $out/console.log 2>&1 || { stamp FAILED train $out; return; }
  evalset $out/epoch_$ep.pth $out/val-epoch$ep
  evalset $out/epoch_$ep.pth $out/s2ds-test $S test
  evalset $out/epoch_$ep.pth $out/dacl10k-test $D test
}
run runs/v2-more10 10
stamp QUEUE_DONE
