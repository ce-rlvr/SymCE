"""
Training-time diagnostics:

- ``sft_holdout_probe``     — post-SFT generation probe. For N held-out v2 records,
                              generate K samples each, score every completion
                              through the oracle, and surface tag-parse rate,
                              witness-parse rate, Pass@1/Pass@K, and reason
                              distribution. Lets us catch "the SFT didn't learn
                              the tag" *before* a 3-day RLVR run.

- ``rollup_rollouts_jsonl`` — post-RLVR aggregation. Reads the per-rollout JSONL
                              that ``OracleRolloutLogger`` writes during GRPO and
                              produces a ``rollouts_summary.json``-shaped dict
                              with per-step bins, reason distribution, parse /
                              format rates, and the PLAN §P4 group-variance gate
                              (% of groups with within-group reward std > 0).

Both functions return plain dicts so the caller can serialise them however it
likes (we also persist a short ``run_summary.md`` alongside the JSON).
"""

from __future__ import annotations

import json
import logging
import math
import warnings
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Optional

from tqdm import tqdm

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Rollout-JSONL rollup (RLVR)
# ─────────────────────────────────────────────────────────────────────────────

def rollup_rollouts_jsonl(
    rollouts_path: Path,
    *,
    output_path: Optional[Path] = None,
    step_bucket: int = 50,
) -> dict[str, Any]:
    """Aggregate per-rollout ``RewardBreakdown`` entries into a summary dict.

    Each input line is one of::

        {
          "_rollout_idx": int,
          "global_step": int,
          "in_batch_idx": int,          # which prompt within the optimizer batch
          "reward": float,
          "reason": str,
          "breakdown": {
            "format_ok": bool,
            "parse_ok": bool,
            "q_neg": int,
            "s_hyp": int,
            "n_hyp": int,
            "n_conditions": int,
            "oracle_elapsed_ms": int,
            "is_none": bool,
            ...
          },
          ...
        }

    A *group* in GRPO is the set of G rollouts produced from a single prompt at a
    single optimizer step — i.e. all rows sharing ``(global_step, prompt_user)``.
    Earlier versions of this rollup keyed groups on ``(global_step, in_batch_idx)``,
    which incorrectly treated every row as its own singleton group (the G
    generations of one prompt land at consecutive ``in_batch_idx`` values, not
    the same one). PLAN §P4 gates a smoke run on the fraction of groups with
    reward std > 0.
    """
    rollouts_path = Path(rollouts_path)
    if not rollouts_path.exists():
        return {"rollouts_path": str(rollouts_path), "missing": True, "total": 0}

    n_total = 0
    n_format_ok = 0
    n_parse_ok = 0
    n_q_neg = 0
    n_is_none = 0
    rewards: list[float] = []
    reasons: Counter = Counter()
    elapsed_ms: list[int] = []
    sum_hyp_ratio = 0.0
    n_hyp_records = 0

    # group_key = (global_step, prompt_user) -> list of rewards.
    # Falls back to (global_step, in_batch_idx) only for legacy rollout files
    # that did not record the prompt_user field.
    groups: dict[tuple[int, Any], list[float]] = defaultdict(list)
    # per-step rollup
    per_step: dict[int, dict[str, Any]] = defaultdict(lambda: {
        "n": 0, "reward_sum": 0.0, "format_ok": 0, "parse_ok": 0, "q_neg": 0,
    })

    with open(rollouts_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                logger.warning("Skipping malformed line in %s", rollouts_path)
                continue

            n_total += 1
            reward = float(row.get("reward", 0.0))
            rewards.append(reward)
            reason = row.get("reason") or "unknown"
            reasons[reason] += 1

            bd = row.get("breakdown") or {}
            if bd.get("format_ok"):
                n_format_ok += 1
            if bd.get("parse_ok"):
                n_parse_ok += 1
            if int(bd.get("q_neg") or 0) == 1:
                n_q_neg += 1
            if bd.get("is_none"):
                n_is_none += 1
            n_hyp = int(bd.get("n_hyp") or 0)
            if n_hyp > 0:
                sum_hyp_ratio += float(bd.get("s_hyp") or 0) / n_hyp
                n_hyp_records += 1
            ms = bd.get("oracle_elapsed_ms")
            if isinstance(ms, int) and ms > 0:
                elapsed_ms.append(ms)

            step = int(row.get("global_step") or 0)
            prompt_user = row.get("prompt_user")
            group_key: tuple[int, Any]
            if isinstance(prompt_user, str) and prompt_user:
                group_key = (step, prompt_user)
            else:
                group_key = (step, int(row.get("in_batch_idx") or 0))
            groups[group_key].append(reward)

            bucket = (step // step_bucket) * step_bucket
            ps = per_step[bucket]
            ps["n"] += 1
            ps["reward_sum"] += reward
            if bd.get("format_ok"):
                ps["format_ok"] += 1
            if bd.get("parse_ok"):
                ps["parse_ok"] += 1
            if int(bd.get("q_neg") or 0) == 1:
                ps["q_neg"] += 1

    if n_total == 0:
        return {"rollouts_path": str(rollouts_path), "total": 0}

    # Group-variance gate
    n_groups = len(groups)
    n_groups_nontrivial = sum(1 for g in groups.values() if len(g) >= 2)
    n_groups_std_pos = sum(
        1 for g in groups.values() if len(g) >= 2 and _stddev(g) > 1e-12
    )
    group_std_pos_rate = (
        n_groups_std_pos / n_groups_nontrivial if n_groups_nontrivial > 0 else 0.0
    )

    # Per-step bucket: tidy ordering and ratios
    by_step: list[dict[str, Any]] = []
    for bucket in sorted(per_step):
        ps = per_step[bucket]
        n = ps["n"]
        by_step.append({
            "step_bucket_start": bucket,
            "n_rollouts": n,
            "mean_reward": round(ps["reward_sum"] / n, 4) if n else 0.0,
            "format_ok_rate": round(ps["format_ok"] / n, 4) if n else 0.0,
            "parse_ok_rate":  round(ps["parse_ok"] / n, 4)  if n else 0.0,
            "q_neg_rate":     round(ps["q_neg"] / n, 4)     if n else 0.0,
        })

    summary = {
        "rollouts_path": str(rollouts_path),
        "total": n_total,
        "n_steps_covered": len({k[0] for k in groups}),
        "n_groups": n_groups,
        "n_groups_nontrivial": n_groups_nontrivial,
        "group_std_pos_rate": round(group_std_pos_rate, 4),
        "mean_reward": round(sum(rewards) / n_total, 4),
        "reward_stddev": round(_stddev(rewards), 4),
        "format_ok_rate": round(n_format_ok / n_total, 4),
        "parse_ok_rate":  round(n_parse_ok  / n_total, 4),
        "q_neg_rate":     round(n_q_neg     / n_total, 4),
        "none_rate":      round(n_is_none   / n_total, 4),
        "mean_hyp_satisfaction": (
            round(sum_hyp_ratio / n_hyp_records, 4) if n_hyp_records > 0 else 0.0
        ),
        "reason_counts": dict(reasons),
        "median_oracle_ms": _median(elapsed_ms),
        "p95_oracle_ms":    _percentile(elapsed_ms, 0.95),
        "max_oracle_ms":    max(elapsed_ms) if elapsed_ms else 0,
        "by_step_bucket":   by_step,
        "step_bucket_size": step_bucket,
        # PLAN §P4 advisory gate (informational; we do not raise here).
        "plan_p4_group_std_gate_pass": bool(group_std_pos_rate >= 0.70),
    }
    if output_path is not None:
        Path(output_path).write_text(json.dumps(summary, indent=2, default=str))
    return summary


# ─────────────────────────────────────────────────────────────────────────────
# SFT post-train held-out probe
# ─────────────────────────────────────────────────────────────────────────────

def sft_holdout_probe(
    *,
    model,
    tokenizer,
    probe_records: list[dict],
    k_samples: int = 8,
    max_new_tokens: int = 512,
    temperature: float = 1.0,
    base_seed: int = 1234,
    oracle_timeout: float = 8.0,
    output_path: Optional[Path] = None,
) -> dict[str, Any]:
    """Generate K samples per probe record and score each through the oracle.

    The probe answers three questions in one shot:
      1. **Tag-parse rate** (= mean ``format_ok`` over completions). If this is
         below ~0.80, downstream RLVR will spend its first few hundred steps
         re-learning the tag rather than the witness — a clear flag to revisit
         the SFT data or pretokenisation.
      2. **Witness-parse rate** (= mean ``parse_ok`` among well-formatted
         completions). Distinguishes "model can't even produce the syntax" from
         "model produces a witness expression but it doesn't evaluate" — the
         former is fatal, the latter is the typical pre-RLVR state.
      3. **Oracle Pass@1 / Pass@K** on the slice. Direct comparison point
         against the eval harness's strict ``reason == "success"`` metric.

    The model is left in whatever mode the caller hands it in. The caller is
    expected to flip Unsloth to inference mode (``FastLanguageModel.for_inference``)
    before invoking — we deliberately do not flip it back because the caller
    typically saves the LoRA adapter right after.
    """
    # Lazy imports so importing this module on a CPU box doesn't drag torch.
    import torch
    from training.common.prompts import V2_SYSTEM_PROMPT
    from training.rlvr.reward_oracle import (
        ORACLE_REWARD_WEIGHTS_DEFAULT,
        compute_reward_oracle,
    )
    from training.eval.eval_runner import build_eval_user_message

    if not probe_records:
        return {"n_prompts": 0, "skipped": True, "reason": "no records"}

    weights = dict(ORACLE_REWARD_WEIGHTS_DEFAULT)
    sample_dumps: list[dict[str, Any]] = []
    reason_counts: Counter = Counter()
    n_format_ok = 0
    n_parse_ok = 0
    n_pass = 0       # per-completion strict pass
    n_per_prompt_pass1 = 0
    n_per_prompt_passk = 0
    total_completions = 0
    sum_reward = 0.0

    # Suppress generation warnings
    warnings.filterwarnings("ignore", message=".*max_new_tokens.*")
    warnings.filterwarnings("ignore", message=".*attention mask API.*")

    for i, record in enumerate(tqdm(probe_records, desc="Held-out Probe")):
        user_msg = build_eval_user_message(record)
        messages = [
            {"role": "system", "content": V2_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]
        prompt_text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True,
        )
        inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)

        any_pass = False
        completions_for_prompt: list[dict[str, Any]] = []
        
        # Generate all k_samples in one batched forward pass
        batched_inputs = {
            key: val.expand(k_samples, -1) for key, val in inputs.items()
        }
        
        torch.manual_seed(base_seed + 1000 * i)
        with torch.no_grad():
            batched_out_ids = model.generate(
                **batched_inputs,
                max_new_tokens=max_new_tokens,
                max_length=None,
                pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
                do_sample=temperature > 0.0,
                temperature=max(temperature, 1e-3),
                use_cache=True,
            )

        for k in range(k_samples):
            new_tokens = batched_out_ids[k][inputs["input_ids"].shape[1]:]
            text = tokenizer.decode(new_tokens, skip_special_tokens=True)

            bd = compute_reward_oracle(
                record=record,
                completion_text=text,
                weights=weights,
                task_mode="counterexample_only",
                timeout_seconds=oracle_timeout,
            )
            total_completions += 1
            sum_reward += float(bd.total)
            if bd.format_ok:
                n_format_ok += 1
            if bd.parse_ok:
                n_parse_ok += 1
            reason_counts[bd.reason] += 1
            passed = bd.reason == "success"
            if passed:
                n_pass += 1
                any_pass = True
            if k == 0 and passed:
                n_per_prompt_pass1 += 1
            completions_for_prompt.append({
                "k": k,
                "reason": bd.reason,
                "reward": round(float(bd.total), 4),
                "format_ok": bd.format_ok,
                "parse_ok": bd.parse_ok,
                "witness_expr": bd.witness_expr,
                "completion": text[:1200],  # truncate; full record exists in stdout
            })

        if any_pass:
            n_per_prompt_passk += 1
        if i < 3:
            sample_dumps.append({
                "theorem_id": record.get("theorem_id"),
                "domain": record.get("domain"),
                "user_message": user_msg,
                "samples": completions_for_prompt,
            })

    n_prompts = len(probe_records)
    summary = {
        "n_prompts": n_prompts,
        "k_samples": k_samples,
        "total_completions": total_completions,
        "tag_parse_rate":       round(n_format_ok / total_completions, 4),
        "witness_parse_ok_rate": round(n_parse_ok  / total_completions, 4),
        "mean_reward":          round(sum_reward / total_completions, 4),
        # Pass@1 = mean over prompts of "first sample passed"
        "oracle_pass_at_1":     round(n_per_prompt_pass1 / n_prompts, 4),
        # Pass@K = mean over prompts of "any of K samples passed"
        f"oracle_pass_at_{k_samples}": round(n_per_prompt_passk / n_prompts, 4),
        "reason_counts": dict(reason_counts),
        "samples_for_inspection": sample_dumps,
        "advisory_gate_tag_parse_rate_min": 0.80,
        "advisory_gate_passed": (
            (n_format_ok / total_completions) >= 0.80
            if total_completions else False
        ),
    }
    if output_path is not None:
        Path(output_path).write_text(json.dumps(summary, indent=2, default=str))
    return summary


# ─────────────────────────────────────────────────────────────────────────────
# Tiny stats helpers
# ─────────────────────────────────────────────────────────────────────────────

def _stddev(xs: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return 0.0
    m = sum(xs) / n
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (n - 1))


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
    idx = min(len(s) - 1, max(0, int(round(q * (len(s) - 1)))))
    return float(s[idx])


# ─────────────────────────────────────────────────────────────────────────────
# Run summary (markdown)
# ─────────────────────────────────────────────────────────────────────────────

def write_run_summary_md(
    output_path: Path,
    *,
    title: str,
    sections: dict[str, dict[str, Any]],
) -> None:
    """Render a short, skim-friendly ``run_summary.md``.

    ``sections`` is ``{"Section title": {"key": value, …}, …}``. Values are
    rendered via repr; nested dicts get a flat indented dump.
    """
    lines: list[str] = [f"# {title}", ""]
    for section, kv in sections.items():
        lines.append(f"## {section}")
        lines.append("")
        if not kv:
            lines.append("_(no data)_")
            lines.append("")
            continue
        for k, v in kv.items():
            if isinstance(v, dict):
                lines.append(f"- **{k}**:")
                for kk, vv in v.items():
                    lines.append(f"    - `{kk}`: {vv}")
            elif isinstance(v, list) and len(v) > 10:
                lines.append(f"- **{k}**: list of {len(v)} entries (truncated)")
            else:
                lines.append(f"- **{k}**: {v}")
        lines.append("")
    Path(output_path).write_text("\n".join(lines))
