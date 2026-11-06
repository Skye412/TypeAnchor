#!/usr/bin/env bash
# Recompute every binary pixel metric after the union-GT fix (eval_filter.union_mask, 2026-11-05).
# Old outputs are in runs/metrics_backup_L127_bug_20261105.tar.
# Usage: nohup bash scripts/recompute_all.sh > runs/recompute_all.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
PY=/home/skye/miniconda3/envs/adaptclip/bin/python
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
C=/home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM
S=/home/skye/data/Skye/databases/Bridge512_balance_S2DS
SA=/home/skye/data/Skye/databases/Bridge512_balance_S2DS_all
EXC=eval_exclude_normals.txt; EXS=s2ds_exclude_trainval.txt
stamp(){ echo "=== $(date '+%F %T') $*"; }
mc(){ # metrics_multiclass with GPU AUPRO, CPU fallback
  $PY metrics_multiclass.py "$@" --aupro-device cuda > /dev/null 2>&1 || $PY metrics_multiclass.py "$@" > /dev/null 2>&1
}
one(){ # $1 run dir, $2 data root, $3 split, [$4 exclude, $5 suffix]
  local r=$1 d=$2 sp=$3 ex=${4:-} sf=${5:-}; local extra=(); [ -n "$ex" ] && extra=(--exclude "$ex" --suffix "$sf")
  $PY metrics_nuisance.py "$r" "$sp" --data "$d" "${extra[@]}" > /dev/null 2>&1 || { stamp FAILED nuisance "$r$sf"; return; }
  if [ -d "$r/typed" ]; then mc --run "$r" --data "$d" --split "$sp" "${extra[@]}" || { stamp FAILED multiclass "$r$sf"; return; }; fi
  stamp DONE "$r$sf"
}
for r in $(find runs -maxdepth 3 -name predictions.csv | sort | xargs -n1 dirname); do
  case "$r" in
    */s2ds-all) one "$r" $SA all $EXS _test ;;                 # 447-tile test subset only (full 2,226 AUPRO is too heavy)
    */s2ds-test*) one "$r" $S test ;;
    *) one "$r" $C val; one "$r" $C val $EXC _clean ;;
  esac
done
V="runs/nuisance-v0/val-epoch20 runs/ablation-no-nuisance/val-epoch20 runs/nuisance-v1-fix/val-epoch20 runs/nuisance-v2/val-epoch20 runs/ablation-v2-no-nuisance/val-epoch20 runs/ablation-v2-no-nuisance-s11/val-epoch20 runs/ablation-v2-no-nuisance-s12/val-epoch20 runs/nuisance-v2-s11/val-epoch20 runs/nuisance-v2-s12/val-epoch20 runs/abl-v2-no-nu-gate/val-epoch20 runs/abl-v2-gamma0/val-epoch20 runs/abl-v2-gamma1/val-epoch20 runs/abl-v2-no-residual/val-epoch20 runs/segformer-b2/val-epoch40"
$PY compare_fp.py $V --suffix _fixed_raw > runs/compare_fp_fixed_raw.log 2>&1 && stamp DONE compare_fp raw
$PY compare_fp.py $V --exclude $EXC --suffix _fixed_clean > runs/compare_fp_fixed_clean.log 2>&1 && stamp DONE compare_fp clean
T="runs/nuisance-v0/s2ds-test-tgtref-full runs/ablation-v2-no-nuisance/s2ds-test-tgtref-full runs/nuisance-v0/s2ds-test-tgtref-4shot runs/ablation-v2-no-nuisance/s2ds-test-tgtref-4shot runs/segformer-b2/s2ds-test"
$PY compare_fp.py $T --data $S --split test --suffix _fixed_s2ds_test > runs/compare_fp_fixed_s2ds_test.log 2>&1 && stamp DONE compare_fp s2ds test
$PY compare_fp.py runs/nuisance-v0/s2ds-all runs/ablation-v2-no-nuisance/s2ds-all --data $SA --split all --exclude $EXS --suffix _fixed_s2ds_all_test > runs/compare_fp_fixed_s2ds_all_test.log 2>&1 && stamp DONE compare_fp s2ds all-test
stamp ALL_DONE
