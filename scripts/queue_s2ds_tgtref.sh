#!/usr/bin/env bash
# Target-domain normal references on S2DS (no S2DS defect labels are used anywhere):
#   ours (v0, 6-anchor v2): references retrieved from the 267 S2DS *train-split* normals (full bank), and a 4-normal
#                           few-shot variant (same information budget as the baseline's 4-shot);
#   baseline-v1:            official AdaptCLIP 4-shot with normal prompts drawn from the S2DS train-split normals.
# All evaluated on the S2DS test split (447 tiles: 73 normal / 374 anomaly), same metrics as scripts/queue_s2ds.sh.
# Usage: nohup bash scripts/queue_s2ds_tgtref.sh > runs/queue_s2ds_tgtref.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
source /home/skye/miniconda3/etc/profile.d/conda.sh
conda activate adaptclip
export CUDA_VISIBLE_DEVICES=0 PYTHONUNBUFFERED=1
S=/home/skye/data/Skye/databases/Bridge512_balance_S2DS
BANK=runs/banks/s2ds_train_normals.pt
stamp(){ echo "=== $(date '+%F %T') $*"; }
evalx(){ # $1 checkpoint $2 out $3.. extra eval args
  local ck=$1 out=$2; shift 2
  stamp START $out
  python eval_nuisance.py --checkpoint "$ck" --out "$out" --data $S --split test --ref-data $S --bank $BANK --save-typed "$@" > "$out.log" 2>&1 \
  && python metrics_nuisance.py "$out" test --data $S >> "$out.log" 2>&1 \
  && { python metrics_multiclass.py --run "$out" --data $S --split test --aupro-device cuda >> "$out.log" 2>&1 || python metrics_multiclass.py --run "$out" --data $S --split test >> "$out.log" 2>&1; } \
  && stamp DONE $out || stamp FAILED $out
}
for m in nuisance-v0 ablation-v2-no-nuisance; do
  evalx runs/$m/epoch_20.pth runs/$m/s2ds-test-tgtref-full
  evalx runs/$m/epoch_20.pth runs/$m/s2ds-test-tgtref-4shot --ref-subset 4 --ref-seed 10
done
python compare_fp.py runs/nuisance-v0/s2ds-test-tgtref-full runs/ablation-v2-no-nuisance/s2ds-test-tgtref-full runs/nuisance-v0/s2ds-test-tgtref-4shot runs/ablation-v2-no-nuisance/s2ds-test-tgtref-4shot --data $S --split test --suffix _s2ds_tgtref > runs/compare_fp_s2ds_tgtref.log 2>&1 && stamp DONE compare_fp
mkdir -p runs/baseline-v1/s2ds-test-4shot
stamp START baseline 4-shot
python test.py --dataset codebrim --checkpoint_path runs/baseline-v1/epoch_15.pth --features_list 6 12 18 24 --image_size 518 --batch_size 4 --n_ctx 12 --vl_reduction 4 --pq_mid_dim 128 --visual_learner --textual_learner --pq_learner --pq_context --seed 10 --k_shots 4 \
  --test_data_path data_views_s2ds_splits/test --save_path runs/baseline-v1/s2ds-test-4shot > runs/baseline-v1/s2ds-test-4shot/console.log 2>&1 && stamp DONE baseline 4-shot || stamp FAILED baseline 4-shot
stamp QUEUE_DONE
