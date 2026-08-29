#!/bin/bash
# Run SFT only, doing full fine-tuning (no LoRA), no RLVR, no Eval.
# It uses the existing training/sft/train.py script which handles SFT training.
# We pass --no-use-lora to disable LoRA adapters and do full SFT.

set -e

# Change to the root of the repository
cd "$(dirname "$0")/.."

echo "==========================================================="
echo " Starting Full SFT Experiment (No LoRA) "
echo "==========================================================="

# Feel free to adjust these parameters to your liking
# We pass --no-use-lora which was added to the configuration 
# to trigger a full fine-tuning run.
python3 -m training.sft.train \
    --no-use-lora \
    --num-train-epochs 1.0 \
    --per-device-train-batch_size 2 \
    --gradient-accumulation-steps 4 \
    --learning-rate 2e-5 \
    --report-to none

echo "==========================================================="
echo " Full SFT complete. Run the eval suite independently using:"
echo " python3 -m training.eval.run_suite"
echo "==========================================================="
