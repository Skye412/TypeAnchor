#!/usr/bin/env bash
# Wait until the foreign training job on the GPU (Tf_MoeClip train_ext_step2.py) has exited, then run the two evaluation
# queues one after the other.  Usage: nohup bash scripts/run_after_gpu_free.sh > runs/run_after_gpu_free.log 2>&1 &
cd "$(dirname "$0")/.."
stamp(){ echo "=== $(date '+%F %T') $*"; }
stamp WAITING for train_ext_step2.py to finish
while pgrep -f "train_ext_step2.py" > /dev/null; do sleep 120; done
stamp GPU FREE
bash scripts/queue_external_seg.sh > runs/queue_external_seg.log 2>&1
stamp external_seg finished
bash scripts/queue_testsplit.sh > runs/queue_testsplit.log 2>&1
stamp testsplit finished
stamp ALL_DONE
