#!/usr/bin/env bash
# Sequential queue (one GPU): v2 no-nuisance ablation (seed 10), then extra seeds for v2 and the ablation.
# Each run ~1.5 h with the feature cache. Usage: nohup bash scripts/queue_v2.sh > runs/queue_v2.log 2>&1 &
set -uo pipefail
cd "$(dirname "$0")/.."
C=/home/skye/data/Skye/feature_cache
run(){ echo "=== $(date '+%F %T') START $2"; bash scripts/train_ablation.sh "$@" > "$2/console.log" 2>&1 && echo "=== $(date '+%F %T') DONE $2" || echo "=== $(date '+%F %T') FAILED $2"; }
mkdir -p runs/ablation-v2-no-nuisance runs/nuisance-v2-s11 runs/nuisance-v2-s12 runs/ablation-v2-no-nuisance-s11 runs/ablation-v2-no-nuisance-s12
run no-nuisance runs/ablation-v2-no-nuisance --arch v2 --cache-dir $C
run v2 runs/nuisance-v2-s11 --arch v2 --cache-dir $C --seed 11
run no-nuisance runs/ablation-v2-no-nuisance-s11 --arch v2 --cache-dir $C --seed 11
run v2 runs/nuisance-v2-s12 --arch v2 --cache-dir $C --seed 12
run no-nuisance runs/ablation-v2-no-nuisance-s12 --arch v2 --cache-dir $C --seed 12
echo "=== $(date '+%F %T') QUEUE_DONE"
