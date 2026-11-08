#!/usr/bin/env bash
# Two extra per-type baselines for the paper's Tables 2 and 4: zero-shot frozen CLIP with the hand prompts (eval_zeroshot.py)
# and a second fully supervised network, DeepLabV3-R50 (train_deeplab.py).  Evaluated on CODEBRIM val (raw + Cleaned-Val),
# CODEBRIM test, S2DS test and dacl10k with the repository protocol.  Usage: nohup bash scripts/queue_extra_baselines.sh > runs/queue_extra_baselines.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
PY=/home/skye/miniconda3/envs/adaptclip/bin/python; SEGPY=/home/skye/miniconda3/envs/MixerCSeg/bin/python
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
C=/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM; S=/home/skye/data/Skye/databases/Bridge512_balance_S2DS; D=/home/skye/data/Skye/databases/Bridge512_dacl10k_val4
EX=eval_exclude_normals.txt
stamp(){ echo "=== $(date '+%F %T') $*"; }
mc(){ $PY metrics_multiclass.py "$@"; }
# $1 out dir, $2 split, $3 data, $4 aupro device
metrics(){ $PY metrics_nuisance.py $1 $2 --data $3 >> $1.log 2>&1 && mc --run $1 --split $2 --data $3 --aupro-device $4 >> $1.log 2>&1; }
metrics_val(){ $PY metrics_nuisance.py $1 >> $1.log 2>&1 && mc --run $1 --aupro-device cuda >> $1.log 2>&1 \
  && $PY metrics_nuisance.py $1 --exclude $EX --suffix _clean >> $1.log 2>&1 && mc --run $1 --exclude $EX --suffix _clean --aupro-device cuda >> $1.log 2>&1; }
# ---- zero-shot CLIP ----
R=runs/zeroshot-clip; mkdir -p $R
out=$R/val; stamp START $out; $PY eval_zeroshot.py --out $out > $out.log 2>&1 && metrics_val $out && stamp DONE $out || stamp FAILED $out
out=$R/test; stamp START $out; $PY eval_zeroshot.py --out $out --split test > $out.log 2>&1 && metrics $out test $C hybrid && stamp DONE $out || stamp FAILED $out
out=$R/s2ds-test; stamp START $out; $PY eval_zeroshot.py --out $out --data $S --split test > $out.log 2>&1 && metrics $out test $S cuda && stamp DONE $out || stamp FAILED $out
out=$R/dacl10k-test; stamp START $out; $PY eval_zeroshot.py --out $out --data $D --split test > $out.log 2>&1 && metrics $out test $D cuda && stamp DONE $out || stamp FAILED $out
# ---- DeepLabV3-R50 ----
R=runs/deeplabv3-r50; mkdir -p $R; stamp START train $R
$SEGPY train_deeplab.py --out $R --epochs 40 > $R/train.log 2>&1 && stamp DONE train $R || stamp FAILED train $R
out=$R/val-epoch40; stamp START $out; metrics_val $out && stamp DONE $out || stamp FAILED $out
out=$R/test-epoch40; stamp START $out; $SEGPY train_deeplab.py --out $R --eval-only --split test --eval-out $out > $out.log 2>&1 && metrics $out test $C hybrid && stamp DONE $out || stamp FAILED $out
out=$R/s2ds-test; stamp START $out; $SEGPY train_deeplab.py --out $R --eval-only --split test --eval-data $S --eval-out $out > $out.log 2>&1 && metrics $out test $S cuda && stamp DONE $out || stamp FAILED $out
out=$R/dacl10k-test; stamp START $out; $SEGPY train_deeplab.py --out $R --eval-only --split test --eval-data $D --eval-out $out > $out.log 2>&1 && metrics $out test $D cuda && stamp DONE $out || stamp FAILED $out
stamp QUEUE_DONE
