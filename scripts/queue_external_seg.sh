#!/usr/bin/env bash
# WPFormer and MixerCSeg (fully supervised binary segmentation, checkpoints from the visualad project) re-evaluated with this
# repository's protocol on CODEBRIM val (raw + Cleaned-Val), S2DS test and the dacl10k strict subset.  See eval_external_seg.py.
# Usage: nohup bash scripts/queue_external_seg.sh > runs/queue_external_seg.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
PY=/home/skye/miniconda3/envs/adaptclip/bin/python
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
EX=eval_exclude_normals.txt
S=/home/skye/data/Skye/databases/Bridge512_balance_S2DS; D=/home/skye/data/Skye/databases/Bridge512_dacl10k_val4
stamp(){ echo "=== $(date '+%F %T') $*"; }
mc(){ $PY metrics_multiclass.py "$@" --aupro-device cuda; }
for m in wpformer mixercseg; do
  case $m in wpformer) EPY=/home/skye/miniconda3/envs/wpformer/bin/python;; mixercseg) EPY=/home/skye/miniconda3/envs/MixerCSeg/bin/python;; esac
  R=runs/ext-$m; mkdir -p $R
  out=$R/val; stamp START $out
  $EPY eval_external_seg.py $m --out $out > $out.log 2>&1 \
  && $PY metrics_nuisance.py $out >> $out.log 2>&1 && mc --run $out >> $out.log 2>&1 \
  && $PY metrics_nuisance.py $out --exclude $EX --suffix _clean >> $out.log 2>&1 && mc --run $out --exclude $EX --suffix _clean >> $out.log 2>&1 \
  && stamp DONE $out || stamp FAILED $out
  for pair in "s2ds-test $S" "dacl10k-test $D"; do
    set -- $pair; out=$R/$1; d=$2; stamp START $out
    $EPY eval_external_seg.py $m --out $out --data $d --split test > $out.log 2>&1 \
    && $PY metrics_nuisance.py $out test --data $d >> $out.log 2>&1 && mc --run $out --data $d --split test >> $out.log 2>&1 \
    && stamp DONE $out || stamp FAILED $out
  done
done
stamp QUEUE_DONE
