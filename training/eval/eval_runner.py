"""
Evaluation harness: Pass@K accuracy on the held-out test set.

Supports two record schemas — auto-detected on the first non-empty line:

- **v1 (legacy)** records carry a ``counterexample_code`` field; the model is
  expected to emit a fenced SymPy/Z3 script that ``src.verifier`` executes.
  Reward / Pass@1 use the legacy ``_classify`` table from
  ``training/rlvr/reward.py``.

- **v2** records carry a ``verifier`` block with a ``module_path``; the model
  is expected to emit a ``[COUNTEREXAMPLE: <expr>]`` tag and the independent
  per-theorem verifier scores the witness via ``src.oracle.sandbox.run_oracle``
  (the same path the RLVR trainer uses in P4). Pass@1 = strict success
  (``q_neg == 1`` AND ``s_hyp == n_hyp``); the looser ``conclusion_pass_at_1``
  (``q_neg`` alone) is reported alongside.

Usage (from repo root, with pfe-rlvr-env active):

  # Evaluate the base model (greedy, Pass@1) — auto-detects schema
  python -m training.eval.eval_runner \\
      --model Qwen/Qwen2.5-Math-1.5B \\
      --model-type base \\
      --test-file data/test_set_v2.jsonl

  # Evaluate an SFT LoRA adapter (Pass@8 via sampling)
  python -m training.eval.eval_runner \\
      --model Qwen/Qwen2.5-Math-1.5B \\
      --lora-adapter checkpoints/sft/qwen25-math-1_5b-r16-bf16-v2-smoke/lora \\
      --model-type sft --n-samples 8 --temperature 1.0

  # Cheap pre-GPU sanity: substitute each record's canonical_witness for
  # the model output and run the oracle (skips model loading entirely).
  python -m training.eval.eval_runner \\
      --use-canonical-witness \\
      --test-file data/test_set_v2.jsonl

  # Compare multiple runs side by side; seeds (same model_type) are
  # auto-grouped to mean ± std with a bootstrap CI on Pass@1 vs the first group.
  python -m training.eval.eval_runner --compare \\
      training/eval/results/eval_base.json \\
      training/eval/results/eval_sft_seed0.json \\
      training/eval/results/eval_sft_seed1.json

Outputs (v2 layout — runs/eval/):
  - runs/eval/<ts>__<producer_run_id>__<testset>__<model_type>/eval_result.json
  - runs/eval/<ts>__<producer_run_id>__<testset>__<model_type>/eval_summary.json
  - runs/eval/<ts>__<producer_run_id>__<testset>__<model_type>/run_summary.md
  - runs/eval/<ts>__<producer_run_id>__<testset>__<model_type>/status.json
  - runs/index.jsonl appended with phase=eval entry

``producer_run_id`` is auto-derived from --lora-adapter / --model when those
point inside runs/ (the leaf is taken); otherwise it can be passed via
--producer-run-id. ``runs/eval/`` may also receive comparison_table.md from
``--compare``.
"""

from __future__ import annotations

import argparse
import json
import logging
import random
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import torch

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.verifier import execute_and_verify  # noqa: E402
from training.common.prompts import V2_SYSTEM_PROMPT, build_v2_user_message  # noqa: E402
from training.common.run_dir import (  # noqa: E402
    REPO_ROOT,
    RUNS_ROOT,
    build_run_dir,
    dataset_fingerprint,
    finalise_run,
    write_run_metadata,
)
from training.rlvr.reward import _classify, REWARD_WEIGHTS, extract_code  # noqa: E402
from training.rlvr.reward_oracle import (  # noqa: E402
    ORACLE_REWARD_WEIGHTS_DEFAULT,
    RewardBreakdown,
    compute_reward_oracle,
    parse_counterexample_tag,
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)

# v1 system prompt — kept here so legacy evals remain byte-identical.
V1_SYSTEM_PROMPT = (
    "You are an expert mathematical programmer. "
    "Given a false mathematical conjecture, write a Python script using SymPy or Z3 "
    "to computationally prove it is false. "
    "You must define a counterexample, verify the remaining hypotheses hold, "
    "and explicitly assert that the conclusion is False."
)

# Legacy results dir (kept readable for backwards-compat with old --compare
# invocations and migration_legacy_checkpoints.py). The v2 path writes into
# runs/eval/ under a per-launch subdirectory; see _build_eval_run_dir below.
RESULTS_DIR = _REPO_ROOT / "training" / "eval" / "results"

EvalFormat = str  # "v1" | "v2"


def _derive_producer_run_id(model: str | None, lora_adapter: str | None) -> str:
    """Best-effort: pull the producer run leaf from a runs/ path."""
    for candidate in (lora_adapter, model):
        if not candidate:
            continue
        path = Path(candidate)
        try:
            rel = path.resolve().relative_to(REPO_ROOT.resolve())
        except ValueError:
            continue
        parts = rel.parts
        # runs/{phase}/{run_id}/[lora|merged|...]
        if len(parts) >= 3 and parts[0] == "runs":
            return parts[2]
        # checkpoints/{phase}/{run_id}/[lora|merged|...] (legacy)
        if len(parts) >= 3 and parts[0] == "checkpoints":
            return f"legacy__{parts[2]}"
    # Fallback: shorten model path
    base = (lora_adapter or model or "unknown").replace("/", "_").strip("_")
    return base[:60] or "unknown"


# ─────────────────────────────────────────────────────────────────────────────
# Schema detection + record loading
# ─────────────────────────────────────────────────────────────────────────────

def _is_v2_record(rec: dict) -> bool:
    """A record is v2-shaped iff it carries a verifier module path.

    We deliberately check ``verifier.module_path`` (not just the presence of a
    ``verifier`` key) because the migration script may emit a ``verifier``
    placeholder on records that failed mid-migration.
    """
    v = rec.get("verifier")
    return isinstance(v, dict) and bool(v.get("module_path"))


def _detect_eval_format(records: list[dict]) -> EvalFormat:
    """Detect format from the first record. Mixed-shape files raise.

    The mixed-shape check is intentionally strict — silently mixing v1 and v2
    records would yield meaningless aggregate numbers because the scoring
    paths produce incomparable success labels.
    """
    if not records:
        raise ValueError("Cannot detect eval format from empty record list")
    first_is_v2 = _is_v2_record(records[0])
    for i, rec in enumerate(records[1:], start=2):
        if _is_v2_record(rec) != first_is_v2:
            raise ValueError(
                f"Mixed v1/v2 records in test file (line {i}). "
                "Use --reward-mode to force a single format if this is intentional, "
                "but the standard test JSONLs should not contain both shapes."
            )
    return "v2" if first_is_v2 else "v1"


def load_test_records(
    test_path: Path,
    limit: Optional[int] = None,
    drop_v2_unusable: bool = True,
) -> tuple[list[dict], EvalFormat, dict]:
    """Load records from a JSONL file. Returns (records, eval_format, load_stats).

    ``drop_v2_unusable`` (default True) filters out v2 records where
    ``migration_failed=true`` or ``witness_passes_verifier=false``. These
    records have no usable verifier path; the PLAN flags them as excluded
    from RLVR/test pools.

    ``load_stats`` is a small dict carrying the counts we surface in the
    summary JSON so the filter rule is auditable per run.
    """
    raw: list[dict] = []
    with open(test_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                raw.append(json.loads(line))
            except json.JSONDecodeError:
                logger.warning("Skipping malformed JSONL line in %s", test_path)

    eval_format = _detect_eval_format(raw)
    n_before = len(raw)
    n_filtered_migration = 0
    n_filtered_witness = 0

    if eval_format == "v2" and drop_v2_unusable:
        kept: list[dict] = []
        for r in raw:
            if r.get("migration_failed") is True:
                n_filtered_migration += 1
                continue
            if r.get("witness_passes_verifier") is False:
                n_filtered_witness += 1
                continue
            kept.append(r)
        raw = kept

    if limit is not None:
        raw = raw[:limit]

    return raw, eval_format, {
        "n_before_filter": n_before,
        "n_filtered_migration_failed": n_filtered_migration,
        "n_filtered_witness_not_passing": n_filtered_witness,
        "n_after_filter": len(raw),
        "eval_format": eval_format,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Prompt construction (leakage-free, shared across v1/v2)
# ─────────────────────────────────────────────────────────────────────────────

def build_eval_user_message(record: dict) -> str:
    """Build the clean, leakage-free user message from a test record."""
    return build_v2_user_message(record)


def build_messages(record: dict, eval_format: EvalFormat) -> list[dict]:
    """Return the [system, user] message list with the per-format system prompt."""
    system = V2_SYSTEM_PROMPT if eval_format == "v2" else V1_SYSTEM_PROMPT
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": build_eval_user_message(record)},
    ]


# ─────────────────────────────────────────────────────────────────────────────
# Model loading + generation (HF / Unsloth backend, unchanged from v1)
# ─────────────────────────────────────────────────────────────────────────────

def load_model_and_tokenizer(
    model_path: str,
    lora_adapter: Optional[str] = None,
    max_seq_length: int = 2048,
    dtype_str: str = "bfloat16",
    chat_template: str = "auto",
):
    """Load a model for evaluation using Unsloth (compatible with LoRA checkpoints)."""
    from unsloth import FastLanguageModel

    from training.common.chat_template import apply_chat_template

    dtype_map = {"bfloat16": torch.bfloat16, "float16": torch.float16, "float32": torch.float32}
    dtype = dtype_map[dtype_str]

    if lora_adapter:
        load_path = lora_adapter
        logger.info("Loading LoRA adapter: %s", load_path)
    else:
        load_path = model_path
        logger.info("Loading model: %s", load_path)

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=load_path,
        max_seq_length=max_seq_length,
        dtype=dtype,
        load_in_4bit=False,
    )
    tokenizer = apply_chat_template(
        tokenizer,
        model_name=model_path,
        chat_template=chat_template,
        checkpoint_path=Path(lora_adapter) if lora_adapter else None,
    )
    FastLanguageModel.for_inference(model)

    return model, tokenizer


def generate_completion(
    model,
    tokenizer,
    messages: list[dict],
    max_new_tokens: int = 1024,
    temperature: float = 0.0,
    seed: int = 42,
) -> str:
    """Generate one completion for the given messages."""
    import warnings
    warnings.filterwarnings("ignore", message=".*max_new_tokens.*")
    warnings.filterwarnings("ignore", message=".*attention mask API.*")

    if temperature == 0.0:
        do_sample = False
        temp_arg = 1.0
    else:
        do_sample = True
        temp_arg = temperature

    prompt_text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True,
    )
    inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)

    gen_kwargs = dict(
        max_new_tokens=max_new_tokens,
        max_length=None,
        pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
        do_sample=do_sample,
        temperature=temp_arg,
        use_cache=True,
    )
    if do_sample:
        torch.manual_seed(seed)

    with torch.no_grad():
        out_ids = model.generate(**inputs, **gen_kwargs)

    new_tokens = out_ids[0][inputs["input_ids"].shape[1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True)


def generate_completions_for_record(
    model,
    tokenizer,
    messages: list[dict],
    n_samples: int = 1,
    max_new_tokens: int = 1024,
    temperature: float = 0.0,
    base_seed: int = 42,
) -> list[str]:
    """Generate n_samples completions (different seeds for sampling diversity).

    HISTORICAL BUG (fixed here): calling this with ``temperature == 0.0`` and
    ``n_samples > 1`` previously expanded the prompt to N copies under greedy
    decoding, producing N byte-identical completions. Pass@5 silently
    collapsed to Pass@1 across the whole pipeline. The fix collapses to a
    single sample with a clear warning — set temperature > 0 (e.g. 0.7) if
    you actually want diverse samples for Pass@K estimation.
    """
    import warnings
    warnings.filterwarnings("ignore", message=".*max_new_tokens.*")
    warnings.filterwarnings("ignore", message=".*attention mask API.*")

    if temperature == 0.0 and n_samples > 1:
        logger.warning(
            "generate_completions_for_record: greedy (temperature=0) with "
            "n_samples=%d would produce %d identical completions and "
            "silently collapse Pass@K to Pass@1. Forcing n_samples=1; set "
            "temperature > 0 (e.g. 0.7) for true Pass@K sampling.",
            n_samples, n_samples,
        )
        n_samples = 1

    if temperature == 0.0:
        do_sample = False
        temp_arg = 1.0
    else:
        do_sample = True
        temp_arg = temperature

    prompt_text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True,
    )
    inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)

    batched_inputs = {
        key: val.expand(n_samples, -1) for key, val in inputs.items()
    }

    gen_kwargs = dict(
        max_new_tokens=max_new_tokens,
        max_length=None,
        pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
        do_sample=do_sample,
        temperature=temp_arg,
        use_cache=True,
    )
    if do_sample:
        torch.manual_seed(base_seed)

    with torch.no_grad():
        out_ids = model.generate(**batched_inputs, **gen_kwargs)

    completions = []
    prompt_len = inputs["input_ids"].shape[1]
    for k in range(n_samples):
        new_tokens = out_ids[k][prompt_len:]
        text = tokenizer.decode(new_tokens, skip_special_tokens=True)
        completions.append(text)
    return completions


# ─────────────────────────────────────────────────────────────────────────────
# Per-completion scoring — v1 (legacy) path
# ─────────────────────────────────────────────────────────────────────────────

def _score_one_legacy(text: str) -> dict:
    code = extract_code(text)
    if code is None:
        return {
            "completion": text,
            "code": None,
            "reward_reason": "no_code",
            "reward": REWARD_WEIGHTS["no_code"],
            "passed": False,
            "verification_result": {},
        }
    try:
        vresult = execute_and_verify(code)
    except Exception as exc:
        logger.exception("Verifier error: %s", exc)
        vresult = {"success": False, "error_message": repr(exc)}

    reason = _classify(vresult)
    passed = (reason == "success")
    return {
        "completion": text,
        "code": code,
        "reward_reason": reason,
        "reward": REWARD_WEIGHTS.get(reason, REWARD_WEIGHTS["default"]),
        "passed": passed,
        "verification_result": {
            k: vresult.get(k)
            for k in (
                "success", "exit_code", "timed_out", "syntax_error",
                "runtime_error", "negation_form_ok", "safety_ok", "error_message",
            )
            if k in vresult
        },
    }


# ─────────────────────────────────────────────────────────────────────────────
# Per-completion scoring — v2 (oracle) path
# ─────────────────────────────────────────────────────────────────────────────

def _score_one_oracle(
    record: dict,
    text: str,
    weights: dict[str, float],
    timeout_seconds: float,
) -> dict:
    """Score one v2 completion against the record's independent verifier."""
    bd: RewardBreakdown = compute_reward_oracle(
        record=record,
        completion_text=text,
        weights=weights,
        task_mode="counterexample_only",
        timeout_seconds=timeout_seconds,
    )
    # Strict Pass@1: q_neg==1 AND s_hyp==n_hyp (i.e. reason == "success").
    strict_pass = (bd.reason == "success")
    return {
        "completion": text,
        "witness_expr": bd.witness_expr,
        "reason": bd.reason,
        "reward": bd.total,
        "format_ok": bd.format_ok,
        "parse_ok": bd.parse_ok,
        "is_none": bd.is_none,
        "gave_up": bd.gave_up,
        "s_hyp": bd.s_hyp,
        "n_hyp": bd.n_hyp,
        "q_neg": bd.q_neg,
        "n_conditions": bd.n_conditions,
        "conditions": bd.conditions,
        "oracle_error": bd.oracle_error,
        "oracle_timed_out": bd.oracle_timed_out,
        "oracle_elapsed_ms": bd.oracle_elapsed_ms,
        "passed": strict_pass,
        # Diagnostic-friendly: conclusion-only pass (q_neg without all-hyps).
        "conclusion_passed": bool(bd.q_neg == 1),
    }


def score_completion_set(
    completions: list[str],
    eval_format: EvalFormat,
    *,
    record: dict | None = None,
    oracle_weights: dict[str, float] | None = None,
    oracle_timeout: float = 8.0,
    n_workers: int = 4,
) -> list[dict]:
    """Score completions in parallel for the chosen format."""
    if eval_format == "v1":
        if len(completions) > 1 and n_workers > 1:
            with ThreadPoolExecutor(max_workers=min(n_workers, len(completions))) as pool:
                return list(pool.map(_score_one_legacy, completions))
        return [_score_one_legacy(c) for c in completions]

    if record is None:
        raise ValueError("Oracle scoring requires the v2 record")
    weights = oracle_weights or dict(ORACLE_REWARD_WEIGHTS_DEFAULT)

    def _fn(c: str) -> dict:
        return _score_one_oracle(record, c, weights, oracle_timeout)

    if len(completions) > 1 and n_workers > 1:
        with ThreadPoolExecutor(max_workers=min(n_workers, len(completions))) as pool:
            return list(pool.map(_fn, completions))
    return [_fn(c) for c in completions]


# ─────────────────────────────────────────────────────────────────────────────
# Pass@K estimator
# ─────────────────────────────────────────────────────────────────────────────

def _median(xs: list[int]) -> float:
    if not xs:
        return 0.0
    s = sorted(xs)
    mid = len(s) // 2
    if len(s) % 2 == 1:
        return float(s[mid])
    return round((s[mid - 1] + s[mid]) / 2, 1)


def _percentile(xs: list[int], q: float) -> float:
    if not xs:
        return 0.0
    s = sorted(xs)
    # Nearest-rank percentile; clamp to last index.
    idx = min(len(s) - 1, max(0, int(round(q * (len(s) - 1)))))
    return float(s[idx])


def pass_at_k(n: int, c: int, k: int) -> float:
    """Unbiased Pass@K estimator: 1 - C(n-c, k)/C(n, k)."""
    if n - c < k:
        return 1.0
    from math import comb
    return 1.0 - comb(n - c, k) / comb(n, k)


# ─────────────────────────────────────────────────────────────────────────────
# Main evaluation loop
# ─────────────────────────────────────────────────────────────────────────────

def _canonical_witness_completion(record: dict) -> str:
    """Wrap the record's canonical_witness in the v2 tag so the same parser is exercised."""
    cw = record.get("canonical_witness")
    if not cw:
        return ""
    return f"[COUNTEREXAMPLE: {cw}]"


def run_eval(
    test_records: list[dict],
    eval_format: EvalFormat,
    *,
    model=None,
    tokenizer=None,
    use_canonical_witness: bool = False,
    n_samples: int = 1,
    max_new_tokens: int = 1024,
    temperature: float = 0.0,
    seed: int = 42,
    reward_workers: int = 4,
    oracle_weights: dict[str, float] | None = None,
    oracle_timeout: float = 8.0,
) -> tuple[list[dict], dict]:
    """Evaluate on the full test set. Returns (per_record_results, summary_dict).

    When ``use_canonical_witness`` is True (v2 only), each record's
    ``canonical_witness`` is wrapped in a ``[COUNTEREXAMPLE: …]`` tag and used
    in place of model generation. Lets us validate the oracle wiring without
    loading a model.
    """
    if use_canonical_witness and eval_format != "v2":
        raise ValueError("--use-canonical-witness requires a v2 test file")
    if not use_canonical_witness and (model is None or tokenizer is None):
        raise ValueError("model + tokenizer required unless --use-canonical-witness")

    per_record: list[dict] = []
    domain_stats: dict[str, dict] = defaultdict(lambda: {"total": 0, "passed": 0})

    for i, record in enumerate(test_records):
        tid = record.get("theorem_id", f"record_{i}")
        domain = record.get("domain", "Unknown")
        logger.info("[%d/%d] %s (%s)", i + 1, len(test_records), tid, domain)

        if use_canonical_witness:
            completions = [_canonical_witness_completion(record)] * n_samples
            gen_time = 0.0
        else:
            messages = build_messages(record, eval_format)
            t0 = time.time()
            completions = generate_completions_for_record(
                model, tokenizer, messages,
                n_samples=n_samples,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                base_seed=seed,
            )
            gen_time = time.time() - t0

        scores = score_completion_set(
            completions, eval_format,
            record=record,
            oracle_weights=oracle_weights,
            oracle_timeout=oracle_timeout,
            n_workers=reward_workers,
        )
        n_correct = sum(1 for s in scores if s["passed"])
        pass1 = bool(scores[0]["passed"])
        passK = (
            pass_at_k(n=n_samples, c=n_correct, k=n_samples)
            if n_samples > 1 else float(pass1)
        )

        domain_stats[domain]["total"] += 1
        domain_stats[domain]["passed"] += int(pass1)

        per_record.append({
            "theorem_id": tid,
            "theorem_name": record.get("theorem_name", ""),
            "domain": domain,
            "prompt_user": build_eval_user_message(record),
            "samples": scores,
            "n_correct": n_correct,
            "pass_at_1": float(pass1),
            "pass_at_k": passK,
            "generation_seconds": round(gen_time, 2),
        })

    summary = _aggregate_summary(per_record, eval_format, n_samples, domain_stats)
    return per_record, summary


# ─────────────────────────────────────────────────────────────────────────────
# Summary aggregation
# ─────────────────────────────────────────────────────────────────────────────

def _aggregate_summary(
    per_record: list[dict],
    eval_format: EvalFormat,
    n_samples: int,
    domain_stats: dict[str, dict],
) -> dict:
    """Build the format-specific summary dict.

    v1 keys (kept for backwards compat with existing result files):
        pass_at_1, pass_at_<n>, no_code_rate, syntax_failure_rate, ...
    v2 keys (new):
        pass_at_1, pass_at_<n>, conclusion_pass_at_1, mean_hyp_satisfaction,
        mean_reward, format_ok_rate, parse_error_rate, none_rate,
        success_rate, neg_q_only_rate, hyp_only_rate, partial_rate, by_domain.
    """
    total = len(per_record)
    overall_pass1 = sum(r["pass_at_1"] for r in per_record) / total if total > 0 else 0.0
    overall_passK = sum(r["pass_at_k"] for r in per_record) / total if total > 0 else 0.0

    by_domain = {
        domain: {
            "total": ds["total"],
            "pass_at_1": round(ds["passed"] / ds["total"], 4) if ds["total"] > 0 else 0.0,
        }
        for domain, ds in sorted(domain_stats.items())
    }

    summary: dict[str, Any] = {
        "eval_format": eval_format,
        "total": total,
        "n_samples_per_problem": n_samples,
        "pass_at_1": round(overall_pass1, 4),
        f"pass_at_{n_samples}": round(overall_passK, 4),
        "by_domain": by_domain,
    }

    if eval_format == "v1":
        reason_counts: dict[str, int] = defaultdict(int)
        for rec in per_record:
            reason_counts[rec["samples"][0]["reward_reason"]] += 1

        def _rate(key: str) -> float:
            return round(reason_counts.get(key, 0) / total, 4) if total > 0 else 0.0

        summary.update({
            "no_code_rate": _rate("no_code"),
            "syntax_failure_rate": _rate("syntax_error"),
            "timeout_rate": _rate("timed_out"),
            "runtime_failure_rate": _rate("runtime_error"),
            "execution_ok_no_negation_rate": _rate("execution_ok_no_negation"),
            "negation_invalid_rate": _rate("negation_invalid"),
            "safety_invalid_rate": _rate("safety_invalid"),
        })
        return summary

    # ── v2 metrics ──────────────────────────────────────────────────────────
    reason_counts = defaultdict(int)
    sum_hyp_ratio = 0.0
    n_hyp_records = 0   # records with n_hyp > 0 (denominator for mean_hyp_satisfaction)
    sum_reward = 0.0
    n_format_ok = 0
    n_parse_error = 0
    n_none = 0
    n_conclusion_pass = 0
    oracle_ms_samples: list[int] = []

    for rec in per_record:
        s0 = rec["samples"][0]
        reason_counts[s0["reason"]] += 1
        sum_reward += float(s0["reward"])
        if s0.get("format_ok"):
            n_format_ok += 1
        # parse-error rate: oracle was called but witness eval failed in namespace.
        if s0["reason"] == "oracle_parse_error":
            n_parse_error += 1
        if s0.get("is_none"):
            n_none += 1
        if s0.get("conclusion_passed"):
            n_conclusion_pass += 1
        n_hyp = int(s0.get("n_hyp", 0) or 0)
        if n_hyp > 0:
            sum_hyp_ratio += float(s0.get("s_hyp", 0)) / n_hyp
            n_hyp_records += 1
        ms = s0.get("oracle_elapsed_ms")
        if isinstance(ms, int) and ms > 0:
            oracle_ms_samples.append(ms)

    def _rate(num: int) -> float:
        return round(num / total, 4) if total > 0 else 0.0

    summary.update({
        "conclusion_pass_at_1": _rate(n_conclusion_pass),
        "mean_hyp_satisfaction": (
            round(sum_hyp_ratio / n_hyp_records, 4) if n_hyp_records > 0 else 0.0
        ),
        "mean_reward": round(sum_reward / total, 4) if total > 0 else 0.0,
        "format_ok_rate": _rate(n_format_ok),
        "parse_error_rate": _rate(n_parse_error),
        "none_rate": _rate(n_none),
        "reason_counts": dict(reason_counts),
        "success_rate": _rate(reason_counts.get("success", 0)),
        "neg_q_only_rate": _rate(reason_counts.get("neg_q_only", 0)),
        "hyp_only_rate": _rate(reason_counts.get("hyp_only", 0)),
        "partial_rate": _rate(reason_counts.get("partial", 0)),
        "no_tag_rate": _rate(reason_counts.get("no_tag", 0)),
        "median_oracle_ms": _median(oracle_ms_samples),
        "p95_oracle_ms": _percentile(oracle_ms_samples, 0.95),
    })
    return summary


# ─────────────────────────────────────────────────────────────────────────────
# --compare mode: side-by-side table + seed aggregation
# ─────────────────────────────────────────────────────────────────────────────

def _bootstrap_pass1_ci(
    a: list[float], b: list[float], n_boot: int = 2000, seed: int = 42,
) -> tuple[float, float, float]:
    """Bootstrap 95% CI on mean(a) - mean(b). Returns (delta, lo, hi).

    Each input is a list of per-seed Pass@1 means. We resample seed-level
    means with replacement; if either input is a single seed, we degrade to
    'no CI' (returns (delta, delta, delta)).
    """
    if not a or not b:
        return 0.0, 0.0, 0.0
    if len(a) < 2 or len(b) < 2:
        delta = (sum(a) / len(a)) - (sum(b) / len(b))
        return delta, delta, delta
    rng = random.Random(seed)
    deltas = []
    for _ in range(n_boot):
        ra = [a[rng.randrange(len(a))] for _ in a]
        rb = [b[rng.randrange(len(b))] for _ in b]
        deltas.append(sum(ra) / len(ra) - sum(rb) / len(rb))
    deltas.sort()
    delta = sum(a) / len(a) - sum(b) / len(b)
    lo = deltas[int(0.025 * n_boot)]
    hi = deltas[int(0.975 * n_boot)]
    return delta, lo, hi


def _load_result_file(path: str) -> dict:
    with open(path) as fh:
        return json.load(fh)


def print_comparison_table(result_files: list[str]) -> str | None:
    """Load multiple result JSONs and print a side-by-side summary.

    Auto-groups by ``meta.model_type``: when ≥2 files share a model_type,
    they are treated as seeds and reported as mean ± std. The first group
    (in input order) is used as the baseline for the bootstrap 95% CI on
    Pass@1 difference. v1 and v2 columns are handled uniformly via the keys
    present in each ``summary`` block.

    Also returns a markdown rendering of the same table so the caller can
    persist it.
    """
    if not result_files:
        print("(no result files supplied)")
        return None

    # Group by model_type, preserving first-seen order.
    groups: dict[str, list[dict]] = {}
    order: list[str] = []
    for path in result_files:
        data = _load_result_file(path)
        meta = data.get("meta", {})
        summary = data.get("summary", {})
        mt = str(meta.get("model_type", "unknown"))
        if mt not in groups:
            groups[mt] = []
            order.append(mt)
        groups[mt].append({"path": path, "meta": meta, "summary": summary})

    # Detect format mix; we still print the table, but warn so the user knows
    # the Pass@1 numbers across formats are not literally comparable.
    formats_seen = {
        entry["summary"].get("eval_format", "v1")
        for entries in groups.values()
        for entry in entries
    }
    if len(formats_seen) > 1:
        print(
            "\n  WARNING: result files mix eval_format values "
            f"({sorted(formats_seen)}); Pass@1 is comparable only within a format.\n"
        )

    rows: list[dict] = []
    baseline_pass1: list[float] | None = None
    baseline_label: str | None = None

    for mt in order:
        entries = groups[mt]
        n_seeds = len(entries)
        pass1s = [float(e["summary"].get("pass_at_1", 0.0)) for e in entries]
        mean_p1 = sum(pass1s) / n_seeds
        std_p1 = (
            (sum((p - mean_p1) ** 2 for p in pass1s) / (n_seeds - 1)) ** 0.5
            if n_seeds >= 2 else 0.0
        )

        row: dict[str, Any] = {
            "label": f"{mt} (n={n_seeds})",
            "pass1_mean": mean_p1,
            "pass1_std": std_p1,
            "pass1_seeds": pass1s,
            "total": entries[0]["summary"].get("total", 0),
            "format": entries[0]["summary"].get("eval_format", "v1"),
        }

        if row["format"] == "v2":
            conc_passes = [
                float(e["summary"].get("conclusion_pass_at_1", 0.0)) for e in entries
            ]
            row["conclusion_pass1"] = sum(conc_passes) / n_seeds
            mean_r = [float(e["summary"].get("mean_reward", 0.0)) for e in entries]
            row["mean_reward"] = sum(mean_r) / n_seeds
            row["parse_error"] = sum(
                float(e["summary"].get("parse_error_rate", 0.0)) for e in entries
            ) / n_seeds
            row["none_rate"] = sum(
                float(e["summary"].get("none_rate", 0.0)) for e in entries
            ) / n_seeds
        else:
            row["no_code"] = sum(
                float(e["summary"].get("no_code_rate", 0.0)) for e in entries
            ) / n_seeds
            row["syntax_err"] = sum(
                float(e["summary"].get("syntax_failure_rate", 0.0)) for e in entries
            ) / n_seeds

        if baseline_pass1 is None:
            baseline_pass1 = pass1s
            baseline_label = mt
            row["delta_vs_baseline"] = None
        else:
            delta, lo, hi = _bootstrap_pass1_ci(pass1s, baseline_pass1)
            row["delta_vs_baseline"] = (delta, lo, hi)

        rows.append(row)

    # Print
    width = 96
    print("\n" + "=" * width)
    print("Evaluation Comparison" + (f" (baseline: {baseline_label})" if baseline_label else ""))
    print("=" * width)
    header = f"{'Model / Run':<28} {'Pass@1 (mean±std)':<22} {'Δ vs baseline (95% CI)':<26} {'N':>5}"
    print(header)
    print("-" * width)
    for row in rows:
        delta_str = "(baseline)"
        if row["delta_vs_baseline"] is not None:
            delta, lo, hi = row["delta_vs_baseline"]
            if lo == hi == delta:
                delta_str = f"{delta:+.3f} (single seed)"
            else:
                delta_str = f"{delta:+.3f} [{lo:+.3f}, {hi:+.3f}]"
        p1 = f"{row['pass1_mean']:.3f} ± {row['pass1_std']:.3f}"
        print(f"{row['label']:<28} {p1:<22} {delta_str:<26} {row['total']:>5}")
    print("-" * width)
    # v2-specific second block
    if any(r["format"] == "v2" for r in rows):
        print(
            f"{'Model / Run':<28} {'conclusion@1':<14} {'mean_reward':<14} "
            f"{'parse_err':<10} {'none':<8}"
        )
        for row in rows:
            if row["format"] != "v2":
                continue
            print(
                f"{row['label']:<28} "
                f"{row.get('conclusion_pass1', 0.0):<14.3f} "
                f"{row.get('mean_reward', 0.0):<14.3f} "
                f"{row.get('parse_error', 0.0):<10.3f} "
                f"{row.get('none_rate', 0.0):<8.3f}"
            )
        print("-" * width)
    # v1-specific second block
    if any(r["format"] == "v1" for r in rows):
        print(f"{'Model / Run':<28} {'no_code':<10} {'syntax_err':<12}")
        for row in rows:
            if row["format"] != "v1":
                continue
            print(
                f"{row['label']:<28} "
                f"{row.get('no_code', 0.0):<10.3f} "
                f"{row.get('syntax_err', 0.0):<12.3f}"
            )
        print("-" * width)
    print()

    # Markdown rendering — one row per group + delta column
    md_lines = [
        "# Evaluation comparison",
        "",
        f"_Baseline: `{baseline_label}` (first group in input order)_",
        "",
        "| Model / Run | Pass@1 (mean ± std) | Δ vs baseline (95% CI) | N |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        delta_str = "_(baseline)_"
        if row["delta_vs_baseline"] is not None:
            delta, lo, hi = row["delta_vs_baseline"]
            if lo == hi == delta:
                delta_str = f"{delta:+.3f} (single seed)"
            else:
                delta_str = f"{delta:+.3f} [{lo:+.3f}, {hi:+.3f}]"
        md_lines.append(
            f"| `{row['label']}` | {row['pass1_mean']:.3f} ± {row['pass1_std']:.3f} "
            f"| {delta_str} | {row['total']} |"
        )

    if any(r["format"] == "v2" for r in rows):
        md_lines += [
            "",
            "## v2 details",
            "",
            "| Model / Run | conclusion@1 | mean_reward | parse_err | none |",
            "| --- | --- | --- | --- | --- |",
        ]
        for row in rows:
            if row["format"] != "v2":
                continue
            md_lines.append(
                f"| `{row['label']}` | {row.get('conclusion_pass1', 0.0):.3f} "
                f"| {row.get('mean_reward', 0.0):+.3f} "
                f"| {row.get('parse_error', 0.0):.3f} "
                f"| {row.get('none_rate', 0.0):.3f} |"
            )
    md_lines += ["", "## Source files", ""]
    for path in result_files:
        md_lines.append(f"- `{path}`")
    return "\n".join(md_lines) + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Evaluate a model checkpoint on the held-out test set (Pass@K).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--model", default=None,
                   help="HuggingFace model ID or path to merged checkpoint.")
    p.add_argument("--lora-adapter", default=None, metavar="PATH",
                   help="Optional LoRA adapter directory (loaded on top of --model).")
    p.add_argument("--model-type", default="unknown",
                   choices=["base", "sft", "rlvr", "calibration", "unknown"],
                   help="Label for the results (base / sft / rlvr / calibration).")
    p.add_argument("--test-file", default="data/test_set.jsonl", metavar="PATH",
                   help="Path to a v1 or v2 test JSONL (auto-detected).")
    p.add_argument("--output-dir", default=None, metavar="PATH",
                   help="(Legacy) flat directory for result JSON files. When unset "
                        "(the default), results land under runs/eval/<auto-name>/.")
    p.add_argument("--run-id", default=None,
                   help="Optional run identifier (default: auto-generated from timestamp).")
    p.add_argument("--producer-run-id", default=None,
                   help="Override the producer-checkpoint run-id stamped into "
                        "the eval run-dir leaf (auto-derived from --model / "
                        "--lora-adapter when those are under runs/).")
    # Generation params
    p.add_argument("--max-new-tokens", type=int, default=1024)
    p.add_argument("--temperature", type=float, default=0.0,
                   help="Sampling temperature. 0 = greedy (recommended for Pass@1).")
    p.add_argument("--n-samples", type=int, default=1,
                   help="Number of completions per problem (use N>1 for Pass@K estimation).")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--max-seq-length", type=int, default=2048)
    p.add_argument("--dtype", default="bfloat16", choices=["bfloat16", "float16", "float32"])
    p.add_argument("--chat-template", default="auto",
                   help="Unsloth chat template name (or 'auto' to infer).")
    p.add_argument("--reward-workers", type=int, default=4,
                   help="Parallel verifier subprocess workers.")
    p.add_argument("--limit", type=int, default=None,
                   help="Evaluate only the first N records (for quick smoke tests).")
    # v2-specific
    p.add_argument("--use-canonical-witness", action="store_true",
                   help="(v2 only) Skip model loading; substitute each record's "
                        "canonical_witness for the model output and run the oracle. "
                        "Used to validate the oracle wiring without GPU.")
    p.add_argument("--oracle-timeout", type=float, default=8.0,
                   help="(v2 only) Subprocess timeout for the per-rollout oracle.")
    p.add_argument("--keep-v2-unusable", action="store_true",
                   help="(v2 only) Do NOT filter records with migration_failed=true "
                        "or witness_passes_verifier=false. Off by default.")
    # Comparison mode
    p.add_argument("--compare", nargs="+", metavar="RESULTS_JSON",
                   help="Skip inference; compare existing results JSON files.")
    return p


def main() -> None:
    args = _build_parser().parse_args()

    if args.compare:
        # Compare mode writes a markdown table next to the result files for
        # easy thesis-table copy-paste.
        out_md = print_comparison_table(args.compare)
        if out_md:
            ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
            comp_dir = RUNS_ROOT / "eval" / f"{ts}__compare"
            comp_dir.mkdir(parents=True, exist_ok=True)
            (comp_dir / "comparison_table.md").write_text(out_md)
            print(f"  comparison_table.md → {comp_dir / 'comparison_table.md'}")
        return

    test_path = _REPO_ROOT / args.test_file
    if not test_path.exists():
        print(f"Error: test file not found: {test_path}", file=sys.stderr)
        sys.exit(1)

    records, eval_format, load_stats = load_test_records(
        test_path,
        limit=args.limit,
        drop_v2_unusable=not args.keep_v2_unusable,
    )
    logger.info(
        "Loaded %d records from %s (eval_format=%s, filter_stats=%s)",
        len(records), test_path.name, eval_format, load_stats,
    )

    if args.use_canonical_witness and eval_format != "v2":
        print("Error: --use-canonical-witness requires a v2 test file.", file=sys.stderr)
        sys.exit(1)

    # Model loading is skipped in canonical-witness mode (no GPU needed).
    model, tokenizer = (None, None)
    if not args.use_canonical_witness:
        if not args.model and not args.lora_adapter:
            print("Error: --model is required (unless --compare or "
                  "--use-canonical-witness is used).", file=sys.stderr)
            sys.exit(1)
        model, tokenizer = load_model_and_tokenizer(
            model_path=args.model or args.lora_adapter,
            lora_adapter=args.lora_adapter if args.model else None,
            max_seq_length=args.max_seq_length,
            dtype_str=args.dtype,
            chat_template=args.chat_template,
        )

    logger.info(
        "Evaluating — model_type=%s, eval_format=%s, n_samples=%d, "
        "temperature=%s, max_new_tokens=%d, use_canonical_witness=%s",
        args.model_type, eval_format, args.n_samples,
        args.temperature, args.max_new_tokens, args.use_canonical_witness,
    )

    t_start = time.time()
    per_record, summary = run_eval(
        records, eval_format,
        model=model, tokenizer=tokenizer,
        use_canonical_witness=args.use_canonical_witness,
        n_samples=args.n_samples,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature,
        seed=args.seed,
        reward_workers=args.reward_workers,
        oracle_timeout=args.oracle_timeout,
    )
    elapsed = time.time() - t_start

    # ── Save results ───────────────────────────────────────────────────────
    effective_model_type = (
        "calibration" if args.use_canonical_witness else args.model_type
    )
    producer_run_id = args.producer_run_id or _derive_producer_run_id(
        args.model, args.lora_adapter,
    )
    testset_tag = test_path.stem  # e.g. test_set_v2

    if args.output_dir is None:
        # New v2 layout: runs/eval/<ts>__<producer>__<testset>__<model_type>/
        ts_leaf = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        leaf = f"{ts_leaf}__{producer_run_id}__{testset_tag}__{effective_model_type}"
        out_dir = RUNS_ROOT / "eval" / leaf
        out_dir.mkdir(parents=True, exist_ok=False)
        result_filename = "eval_result.json"
        summary_filename = "eval_summary.json"
        run_id = args.run_id or leaf
        # Stamp run metadata (config = the argparse namespace, dataset fingerprint)
        write_run_metadata(
            run_dir=out_dir, cfg=vars(args), phase="eval",
            cli_namespace=args, argv=sys.argv,
            config_yaml=None,
            dataset_paths=[args.test_file],
            extra={
                "producer_run_id": producer_run_id,
                "model": args.model,
                "lora_adapter": args.lora_adapter,
                "model_type": effective_model_type,
                "use_canonical_witness": args.use_canonical_witness,
            },
        )
    else:
        # Legacy flat dir — kept for one-off custom paths.
        run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        result_filename = f"{run_id}_{effective_model_type}.json"
        summary_filename = f"{run_id}_{effective_model_type}_summary.json"

    meta = {
        "run_id": run_id,
        "producer_run_id": producer_run_id,
        "model": args.model,
        "lora_adapter": args.lora_adapter,
        "model_type": effective_model_type,
        "eval_format": eval_format,
        "use_canonical_witness": args.use_canonical_witness,
        "test_file": str(test_path),
        "test_file_fingerprint": dataset_fingerprint([args.test_file]),
        "load_stats": load_stats,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "n_records": len(records),
        "n_samples": args.n_samples,
        "temperature": args.temperature,
        "max_new_tokens": args.max_new_tokens,
        "seed": args.seed,
        "elapsed_seconds": round(elapsed, 1),
    }

    full_results = {"meta": meta, "summary": summary, "per_record": per_record}
    full_path = out_dir / result_filename
    with open(full_path, "w", encoding="utf-8") as fh:
        json.dump(full_results, fh, indent=2, ensure_ascii=False, default=str)

    summary_path = out_dir / summary_filename
    with open(summary_path, "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "summary": summary}, fh, indent=2, ensure_ascii=False, default=str)

    if args.output_dir is None:
        # Markdown skim for the run dir
        _write_eval_summary_md(out_dir, meta, summary, eval_format)
        finalise_run(out_dir, status="completed", extra={
            "pass_at_1": summary.get("pass_at_1"),
            "elapsed_seconds": round(elapsed, 1),
        })

    _print_summary(args, summary, elapsed, full_path, summary_path, eval_format)


def _write_eval_summary_md(out_dir: Path, meta: dict, summary: dict, eval_format: EvalFormat) -> None:
    """Short, copy-paste-friendly markdown summary inside the eval run dir."""
    lines = [
        f"# Eval — {meta['model_type']}",
        "",
        f"- **Producer**: `{meta.get('producer_run_id')}`",
        f"- **Model**: `{meta.get('model') or meta.get('lora_adapter')}`",
        f"- **Test file**: `{meta.get('test_file')}` ({summary['total']} records, format={eval_format})",
        f"- **n_samples**: {meta.get('n_samples')}  •  **temperature**: {meta.get('temperature')}",
        "",
        "## Headline",
        "",
        f"- **Pass@1**: {summary.get('pass_at_1'):.4f}",
    ]
    if meta.get("n_samples", 1) > 1:
        k_key = f"pass_at_{meta['n_samples']}"
        lines.append(f"- **Pass@{meta['n_samples']}**: {summary.get(k_key):.4f}")
    if eval_format == "v2":
        lines += [
            f"- **conclusion-Pass@1**: {summary.get('conclusion_pass_at_1'):.4f}",
            f"- **mean reward**: {summary.get('mean_reward'):+.4f}",
            f"- **mean hyp satisfaction**: {summary.get('mean_hyp_satisfaction'):.4f}",
            f"- **format_ok rate**: {summary.get('format_ok_rate'):.4f}",
            f"- **parse_error rate**: {summary.get('parse_error_rate'):.4f}",
            f"- **none rate**: {summary.get('none_rate'):.4f}",
            f"- **median oracle ms**: {summary.get('median_oracle_ms')}",
            "",
            "## Reason distribution",
            "",
        ]
        for reason, n in sorted(summary.get("reason_counts", {}).items(), key=lambda kv: -kv[1]):
            lines.append(f"- `{reason}`: {n}")
    lines += ["", "## By domain", ""]
    for domain, ds in sorted(summary.get("by_domain", {}).items()):
        lines.append(f"- `{domain}` (n={ds['total']}): Pass@1 = {ds['pass_at_1']:.4f}")
    (out_dir / "run_summary.md").write_text("\n".join(lines) + "\n")


def _print_summary(
    args,
    summary: dict,
    elapsed: float,
    full_path: Path,
    summary_path: Path,
    eval_format: EvalFormat,
) -> None:
    width = 70
    label = "CALIBRATION" if args.use_canonical_witness else args.model_type.upper()
    print(f"\n{'=' * width}")
    print(f"  Eval Results  [{label}]  ({eval_format})")
    print(f"{'=' * width}")
    print(f"  Model              : {args.model or args.lora_adapter or '(canonical-witness)'}")
    if args.lora_adapter and args.model:
        print(f"  LoRA adapter       : {args.lora_adapter}")
    print(f"  Test records       : {summary['total']}")
    print(f"  Samples/problem    : {summary['n_samples_per_problem']}")
    print(f"  Temperature        : {args.temperature}")
    print(f"  Elapsed            : {round(elapsed, 1)}s")
    print(f"{'─' * width}")
    print(f"  Pass@1             : {summary['pass_at_1']:.3f}  "
          f"({int(summary['pass_at_1']*summary['total'])}/{summary['total']})")
    if args.n_samples > 1:
        k_key = f"pass_at_{args.n_samples}"
        print(f"  Pass@{args.n_samples:<14}: {summary[k_key]:.3f}")

    if eval_format == "v2":
        print(f"{'─' * width}")
        print(f"  conclusion-Pass@1  : {summary['conclusion_pass_at_1']:.3f}")
        print(f"  mean reward        : {summary['mean_reward']:+.3f}")
        print(f"  mean hyp sat.      : {summary['mean_hyp_satisfaction']:.3f}")
        print(f"  format_ok rate     : {summary['format_ok_rate']:.3f}")
        print(f"  parse_error rate   : {summary['parse_error_rate']:.3f}")
        print(f"  NONE rate          : {summary['none_rate']:.3f}")
        print(f"  median oracle ms   : {summary['median_oracle_ms']}")
        print(f"{'─' * width}")
        print("  Reason counts (first sample):")
        for reason, n in sorted(summary["reason_counts"].items(), key=lambda kv: -kv[1]):
            print(f"    {reason:<24}: {n}")
    else:
        print(f"{'─' * width}")
        print(f"  No code            : {summary['no_code_rate']:.3f}")
        print(f"  Syntax error       : {summary['syntax_failure_rate']:.3f}")
        print(f"  Timeout            : {summary['timeout_rate']:.3f}")
        print(f"  Runtime error      : {summary['runtime_failure_rate']:.3f}")
        print(f"  Exec OK, no neg.   : {summary['execution_ok_no_negation_rate']:.3f}")

    print(f"{'─' * width}")
    print("  By domain:")
    for domain, ds in sorted(summary["by_domain"].items()):
        print(f"    {domain:<22}: pass@1={ds['pass_at_1']:.3f}  (n={ds['total']})")
    print(f"{'─' * width}")
    print(f"  Full results  → {full_path}")
    print(f"  Summary       → {summary_path}")
    print(f"{'=' * width}\n")


if __name__ == "__main__":
    main()
