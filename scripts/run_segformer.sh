#!/usr/bin/env bash
# Fully supervised reference baseline: SegFormer-B2, same training tiles and class masks as our heads.
# Trains in the MixerCSeg env (mmseg 0.30), evaluates with the adaptclip-env metric scripts on
# CODEBRIM val (raw + Cleaned-Val) and the S2DS test split (447 tiles, zero-shot w.r.t. S2DS).
# Usage: nohup bash scripts/run_segformer.sh [seed] > runs/segformer-b2.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
SEED=${1:-10}; OUT=runs/segformer-b2$([ "$SEED" = 10 ] || echo "-s$SEED")
SEGPY=/home/skye/miniconda3/envs/MixerCSeg/bin/python
ADPY=/home/skye/miniconda3/envs/adaptclip/bin/python
S=/home/skye/data/Skye/databases/Bridge512_balance_S2DS
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
stamp(){ echo "=== $(date '+%F %T') $*"; }
mkdir -p $OUT; git rev-parse HEAD > $OUT/revision.txt
stamp START train $OUT
$SEGPY train_segformer.py --out $OUT --epochs 40 --seed $SEED > $OUT/console.log 2>&1 && stamp DONE train || { stamp FAILED train; exit 1; }
V=$OUT/val-epoch40
$ADPY metrics_nuisance.py $V > $V.metrics.log 2>&1 && $ADPY metrics_multiclass.py --run $V >> $V.metrics.log 2>&1 \
 && $ADPY metrics_nuisance.py $V --exclude eval_exclude_normals.txt --suffix _clean >> $V.metrics.log 2>&1 \
 && $ADPY metrics_multiclass.py --run $V --exclude eval_exclude_normals.txt --suffix _clean >> $V.metrics.log 2>&1 && stamp DONE val metrics || stamp FAILED val metrics
T=$OUT/s2ds-test
$SEGPY train_segformer.py --out $OUT --eval-only --eval-data $S --split test --eval-out $T > $T.log 2>&1 \
 && $ADPY metrics_nuisance.py $T test --data $S >> $T.log 2>&1 \
 && { $ADPY metrics_multiclass.py --run $T --data $S --split test --aupro-device cuda >> $T.log 2>&1 || $ADPY metrics_multiclass.py --run $T --data $S --split test >> $T.log 2>&1; } && stamp DONE s2ds test || stamp FAILED s2ds test
stamp ALL_DONE
