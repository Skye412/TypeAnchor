#!/usr/bin/env bash
# MultiADS (official code, third_party/MultiADS) trained on CODEBRIM train, then evaluated with this repository's protocol on
# CODEBRIM val (raw + Cleaned-Val), S2DS test and the dacl10k strict subset.  See multiads_bridge.py.
# Usage: [R=runs/ext-multiads-lr1e-4 EXTRA='--lr 1e-4'] nohup bash scripts/queue_multiads.sh > runs/queue_multiads.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
PY=/home/skye/miniconda3/envs/adaptclip/bin/python
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
EX=eval_exclude_normals.txt; R=${R:-runs/ext-multiads}; CK=$R/epoch_10.pth   # R = output dir, EXTRA = extra training arguments
S=/home/skye/data/Skye/databases/Bridge512_balance_S2DS; D=/home/skye/data/Skye/databases/Bridge512_dacl10k_val4
stamp(){ echo "=== $(date '+%F %T') $*"; }
mc(){ $PY metrics_multiclass.py "$@" --aupro-device cuda; }
mkdir -p $R; git rev-parse HEAD > $R/revision.txt; git -C third_party/MultiADS rev-parse HEAD > $R/multiads_revision.txt
stamp TRAIN $R
$PY multiads_bridge.py train --out $R ${EXTRA:-} > $R/console.log 2>&1 || { stamp FAILED train; stamp QUEUE_DONE; exit 1; }
out=$R/val; stamp START $out
$PY multiads_bridge.py eval --checkpoint $CK --out $out > $out.log 2>&1 \
&& $PY metrics_nuisance.py $out >> $out.log 2>&1 && mc --run $out >> $out.log 2>&1 \
&& $PY metrics_nuisance.py $out --exclude $EX --suffix _clean >> $out.log 2>&1 && mc --run $out --exclude $EX --suffix _clean >> $out.log 2>&1 \
&& stamp DONE $out || stamp FAILED $out
for pair in "s2ds-test $S" "dacl10k-test $D"; do
  set -- $pair; out=$R/$1; d=$2; stamp START $out
  $PY multiads_bridge.py eval --checkpoint $CK --out $out --data $d --split test > $out.log 2>&1 \
  && $PY metrics_nuisance.py $out test --data $d >> $out.log 2>&1 && mc --run $out --data $d --split test >> $out.log 2>&1 \
  && stamp DONE $out || stamp FAILED $out
done
stamp QUEUE_DONE
