"""
Rollout/training-time tokeniser parity check (PLAN Section P4 risk mitigation).

GRPOTrainer computes per-token logprobs at training time using the HF
tokenizer; when rollouts come from vLLM, vLLM uses its own tokeniser cache.
If the two disagree on any chat-template special token, BOS/EOS handling,
or whitespace, the logprob alignment breaks silently and the advantage
signal becomes noise.

This script enforces two invariants over a sample of v2 RLVR prompts:

1. **Chat-template determinism.** ``tokenizer.apply_chat_template`` on the
   prompt is deterministic across calls (no hidden RNG, no inserted
   timestamps), and round-tripping ``ids -> decode -> encode`` is the
   identity (or, where it isn't exactly, the mismatch is logged so it can
   be inspected). This is the parity check that is meaningful regardless
   of whether vLLM is loaded.

2. **vLLM/HF tokeniser id-equality** *(only if vLLM is importable and
   ``--check-vllm`` is set).* Load the same model under vLLM and compare
   ``vllm_tokenizer.encode(s) == hf_tokenizer.encode(s)`` for every chat-
   template-rendered prompt in the sample.

Usage (from repo root, pfe-rlvr-env active):

    python -m tools.check_rollout_tokeniser_parity \\
        --rlvr-prompts data/rlvr_prompts.jsonl \\
        --sft-checkpoint checkpoints/sft/qwen25-math-1_5b-r16-bf16-v2-p4smoke/lora \\
        --num-prompts 50

Exit codes:
    0 - all parity checks pass.
    1 - at least one parity check failed (details printed).
    2 - usage / I/O error.
"""

from __future__ import annotations

import argparse
import json
import logging
import random
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


logger = logging.getLogger("p4_parity")


def _load_prompts(jsonl_path: Path, n: int, seed: int) -> list[list[dict]]:
    """Read ``n`` randomly sampled prompts from a v2 RLVR JSONL file."""
    if not jsonl_path.exists():
        raise FileNotFoundError(f"RLVR prompts file not found: {jsonl_path}")
    prompts: list[list[dict]] = []
    with jsonl_path.open() as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            rec = json.loads(raw)
            msgs = rec.get("messages") or []
            # RLVR is prompt-only; drop any accidental assistant turn.
            prompts.append([m for m in msgs if m.get("role") in ("system", "user")])
    if not prompts:
        raise ValueError(f"No prompts found in {jsonl_path}")
    rng = random.Random(seed)
    if n >= len(prompts):
        return prompts
    return rng.sample(prompts, n)


def _check_chat_template_parity(prompts: list[list[dict]], tokenizer) -> tuple[int, int]:
    """For each prompt: apply chat template, encode, decode, encode again.

    Returns (n_pass, n_fail). Mismatches are logged at WARNING level with a
    truncated snippet of the first divergence point.
    """
    n_pass = 0
    n_fail = 0
    for i, msgs in enumerate(prompts):
        rendered = tokenizer.apply_chat_template(
            msgs, tokenize=False, add_generation_prompt=True,
        )
        # apply_chat_template called twice should be string-equal (determinism).
        rendered_again = tokenizer.apply_chat_template(
            msgs, tokenize=False, add_generation_prompt=True,
        )
        if rendered != rendered_again:
            logger.warning(
                "prompt %d: chat-template output is non-deterministic across calls",
                i,
            )
            n_fail += 1
            continue

        ids1 = tokenizer(rendered, add_special_tokens=False).input_ids
        # encode -> decode -> encode must be the identity, otherwise the rollout
        # text vLLM emits will not re-tokenise to the same ids the trainer used.
        decoded = tokenizer.decode(ids1, skip_special_tokens=False)
        ids2 = tokenizer(decoded, add_special_tokens=False).input_ids

        if ids1 == ids2:
            n_pass += 1
            continue

        # Find the first divergence point for a useful error message.
        diff_at = next(
            (j for j, (a, b) in enumerate(zip(ids1, ids2)) if a != b),
            min(len(ids1), len(ids2)),
        )
        logger.warning(
            "prompt %d: round-trip mismatch at token %d (len %d -> %d). "
            "First diverging context: %r",
            i, diff_at, len(ids1), len(ids2),
            decoded[max(0, diff_at - 20): diff_at + 20],
        )
        n_fail += 1
    return n_pass, n_fail


def _check_vllm_parity(prompts: list[list[dict]], hf_tokenizer, model_path: str) -> tuple[int, int]:
    """Optional: compare HF tokeniser ids vs vLLM's tokeniser ids.

    Only runs if ``vllm`` is importable. The vLLM tokeniser is the same
    AutoTokenizer that the trainer uses, but loaded via vLLM's path; this
    catches the edge case where vLLM ships with a stale cache or different
    revision pin.
    """
    try:
        from vllm.transformers_utils.tokenizer import get_tokenizer
    except Exception as exc:
        logger.warning("vLLM not importable (%s); skipping vLLM parity check.", exc)
        return 0, 0

    vllm_tok = get_tokenizer(model_path)

    n_pass = 0
    n_fail = 0
    for i, msgs in enumerate(prompts):
        rendered = hf_tokenizer.apply_chat_template(
            msgs, tokenize=False, add_generation_prompt=True,
        )
        hf_ids = hf_tokenizer(rendered, add_special_tokens=False).input_ids
        vllm_ids = vllm_tok(rendered, add_special_tokens=False).input_ids
        if hf_ids == vllm_ids:
            n_pass += 1
        else:
            diff_at = next(
                (j for j, (a, b) in enumerate(zip(hf_ids, vllm_ids)) if a != b),
                min(len(hf_ids), len(vllm_ids)),
            )
            logger.warning(
                "prompt %d: HF/vLLM tokeniser disagree at position %d "
                "(HF len=%d, vLLM len=%d)", i, diff_at, len(hf_ids), len(vllm_ids),
            )
            n_fail += 1
    return n_pass, n_fail


def main() -> int:
    p = argparse.ArgumentParser(
        description="Rollout/training-time tokeniser parity check (PLAN Section P4).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--rlvr-prompts", default="data/rlvr_prompts.jsonl",
        help="Path to a v2 RLVR prompts JSONL file.",
    )
    p.add_argument(
        "--sft-checkpoint", required=True,
        help="Path to the SFT LoRA adapter directory (the tokenizer there is "
             "what RLVR loads at training time).",
    )
    p.add_argument("--num-prompts", type=int, default=50)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--check-vllm", action="store_true",
        help="Additionally compare HF tokeniser ids to vLLM's tokeniser ids "
             "for the same chat-template-rendered prompt. Requires `vllm` to "
             "be importable.",
    )
    args = p.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="[parity] %(levelname)s %(message)s",
    )

    rlvr_path = (_REPO_ROOT / args.rlvr_prompts).resolve()
    sft_path = (_REPO_ROOT / args.sft_checkpoint).resolve()

    print(f"[parity] RLVR prompts: {rlvr_path}")
    print(f"[parity] SFT ckpt:     {sft_path}")
    print(f"[parity] N prompts:    {args.num_prompts} (seed={args.seed})")

    try:
        prompts = _load_prompts(rlvr_path, args.num_prompts, args.seed)
    except (FileNotFoundError, ValueError) as exc:
        print(f"[parity] ERROR loading prompts: {exc}", file=sys.stderr)
        return 2
    print(f"[parity] sampled {len(prompts)} prompts.")

    from transformers import AutoTokenizer  # noqa: E402  (heavy import deferred)

    if not sft_path.exists():
        print(f"[parity] ERROR: SFT checkpoint not found at {sft_path}", file=sys.stderr)
        return 2
    hf_tokenizer = AutoTokenizer.from_pretrained(str(sft_path))

    # Apply the same chat template the trainer applies.
    from training.common.chat_template import apply_chat_template  # noqa: E402
    hf_tokenizer = apply_chat_template(
        hf_tokenizer,
        checkpoint_path=sft_path,
        chat_template="auto",
    )

    n_pass, n_fail = _check_chat_template_parity(prompts, hf_tokenizer)
    print(f"[parity] chat-template round-trip: pass={n_pass} fail={n_fail}")

    if args.check_vllm:
        vp, vf = _check_vllm_parity(prompts, hf_tokenizer, str(sft_path))
        print(f"[parity] vLLM vs HF tokeniser:   pass={vp} fail={vf}")
        if vf > 0:
            return 1

    if n_fail > 0:
        print(f"[parity] FAIL: {n_fail} / {len(prompts)} prompts round-trip mismatch.")
        return 1
    print(f"[parity] OK: all {len(prompts)} prompts pass round-trip parity.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
