#!/usr/bin/env bash
# P4 wiring smoke orchestrator.
#
# Sequence:
#   1. Train SFT-v2 smoke checkpoint on data/sft_data_v2.jsonl.
#      Output: runs/sft/<auto-name>/lora  (discovered from the freshest
#      runs/sft/* leaf so the timestamped naming is invisible to the caller).
#   2. Run RLVR-v2 smoke with reward_mode=oracle, max_steps=20 on
#      data/rlvr_prompts_v2.jsonl, resuming from the SFT run discovered above.
#      Output: runs/rlvr/<auto-name>/
#   3. Run tokeniser-parity check on 50 random prompts using the SFT checkpoint.
#
# Pair with configs/p4_smoke.yaml. Run from the repo root with pfe-rlvr-env
# active. Stops on the first failure (set -euo pipefail).
#
# Usage:
#   bash tools/run_p4_smoke.sh [--skip-sft] [--skip-rlvr] [--skip-parity]

set -euo pipefail

# Unsloth's startup statistics call to HF can stall up to 120 s on flaky
# networks and abort the run. We don't need it; disable.
export UNSLOTH_DISABLE_STATISTICS=1

CONFIG="configs/p4_smoke.yaml"

SKIP_SFT=0
SKIP_RLVR=0
SKIP_PARITY=0
for arg in "$@"; do
    case "$arg" in
        --skip-sft)    SKIP_SFT=1 ;;
        --skip-rlvr)   SKIP_RLVR=1 ;;
        --skip-parity) SKIP_PARITY=1 ;;
        *) echo "unknown flag: $arg" >&2; exit 2 ;;
    esac
done

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "=================================================================="
echo "P4 smoke: SFT-v2 → RLVR-v2 (oracle) → tokeniser parity"
echo "Repo:   $REPO_ROOT"
echo "Config: $CONFIG"
echo "=================================================================="

if [[ "$SKIP_SFT" -eq 0 ]]; then
    echo
    echo "── [1/3] SFT-v2 smoke ───────────────────────────────────────────────"
    python -m training.sft.train --config "$CONFIG"
else
    echo "── [1/3] SFT-v2 smoke ─ SKIPPED"
fi

# Find the most-recently-created SFT run dir under runs/sft/. Used for both
# the RLVR sft_checkpoint and the tokeniser-parity check below.
SFT_RUN_DIR="$(ls -dt runs/sft/*/ 2>/dev/null | head -1 || true)"
if [[ -n "$SFT_RUN_DIR" ]]; then
    SFT_LORA="${SFT_RUN_DIR%/}/lora"
else
    SFT_LORA="checkpoints/sft/qwen3-4b-r16-bf16-v2-p4smoke/lora"  # legacy fallback
fi
echo "[discover] SFT LoRA → $SFT_LORA"

if [[ "$SKIP_RLVR" -eq 0 ]]; then
    echo
    echo "── [2/3] RLVR-v2 smoke (max_steps=20, reward_mode=oracle, G=4) ──────"
    python -m training.rlvr.train --config "$CONFIG" --sft-checkpoint "$SFT_LORA"
else
    echo "── [2/3] RLVR-v2 smoke ─ SKIPPED"
fi

if [[ "$SKIP_PARITY" -eq 0 ]]; then
    echo
    echo "── [3/3] Tokeniser parity check ─────────────────────────────────────"
    python -m tools.check_rollout_tokeniser_parity \
        --rlvr-prompts data/rlvr_prompts_v2.jsonl \
        --sft-checkpoint "$SFT_LORA" \
        --num-prompts 50
else
    echo "── [3/3] Tokeniser parity check ─ SKIPPED"
fi

# Latest RLVR run dir for the final pointer printout.
RLVR_RUN_DIR="$(ls -dt runs/rlvr/*/ 2>/dev/null | head -1 || true)"

echo
echo "=================================================================="
echo "P4 smoke complete."
if [[ -n "$RLVR_RUN_DIR" ]]; then
    echo "  RLVR rollout telemetry:"
    echo "    ${RLVR_RUN_DIR%/}/rollouts.jsonl"
    echo "    ${RLVR_RUN_DIR%/}/rollouts_summary.json"
    echo "  RLVR train log:"
    echo "    ${RLVR_RUN_DIR%/}/train_log.csv"
    echo "  Run summary:"
    echo "    ${RLVR_RUN_DIR%/}/run_summary.md"
fi
echo "=================================================================="
