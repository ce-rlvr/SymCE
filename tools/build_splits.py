"""
Standalone CLI that builds the v2.0 SFT / RLVR / test split files from a
migrated dataset (``data/algebra_counterexamples_v2.jsonl`` by default).

Design context:

- ``pipeline.py:split_dataset`` is left alone because the in-pipeline path for
  v2 records (Section P1b) is also deferred; coupling the splitter to the fresh-run
  pipeline before P1b would entangle two unrelated workstreams. This tool
  reads the migrated JSONL directly.
- Strict eligibility (``canonical_witness != null`` AND
  ``witness_passes_verifier == True``) is required for SFT and test outputs.
- RLVR uses a loose pool (strict ∪ verifier-only records): the oracle reward
  only needs ``verifier.module_path`` + the condition metadata, which all v2
  records carry.
- Each SFT target is round-trip-validated through P2's
  ``compute_reward_oracle`` as a hard gate: if a target the rule-based
  builder produces does not actually score positive against the verifier,
  we drop it and log the reason. This catches verifier-corpus regressions
  the migration step would not otherwise surface.
- Reasoning is built deterministically by ``tools/sft_target_builder``
  (no Gemini call); over-budget targets are truncated, not dropped.

Outputs:
- ``data/sft_data.jsonl``    - ``{"messages": [system, user, assistant]}``
- ``data/rlvr_prompts.jsonl`` - ``{"messages": [system, user], ...verifier metadata}``
- ``data/test_set.jsonl``    - full v2 record schema preserved.
- ``data/dataset_stats.json`` - counts, domain breakdown, oracle pass rate,
  token-length histogram, drop-reason breakdown, truncation rate.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

# Ensure repo root on sys.path so the script can be invoked from any cwd.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from training.common.prompts import V2_SYSTEM_PROMPT, build_v2_user_message  # noqa: E402
from training.rlvr.reward_oracle import (                # noqa: E402
    compute_reward_oracle,
    parse_counterexample_tag,
)
from tools.sft_target_builder import (                   # noqa: E402
    BuildResult,
    build_sft_target,
    truncate_target_to_fit,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("build_splits")


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def _load_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    with path.open(encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                logger.warning("line %d: skipping malformed JSON (%s)", i, exc)
    return records


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _normalize_path_key(path_value: str | None) -> str:
    if not path_value:
        return ""
    try:
        return str(Path(path_value).expanduser().resolve())
    except Exception:
        return str(Path(path_value).expanduser())


def _load_witness_schema_map(path: Path | None) -> dict[str, str]:
    if path is None or not path.exists():
        return {}

    schema_map: dict[str, str] = {}
    with path.open(encoding="utf-8") as fh:
        for line_no, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                rec = json.loads(raw)
            except json.JSONDecodeError as exc:
                logger.warning("witness schema line %d: skipping malformed JSON (%s)", line_no, exc)
                continue

            schema = (rec.get("witness_schema") or rec.get("schema") or "").strip()
            if not schema:
                continue

            for candidate_key in (rec.get("module_path"), rec.get("file"), rec.get("path")):
                key = _normalize_path_key(candidate_key)
                if key:
                    schema_map[key] = schema
    return schema_map


def _attach_witness_schema(record: dict, schema_map: dict[str, str]) -> dict:
    schema = (record.get("witness_schema") or "").strip()
    if schema:
        return record

    verifier = record.get("verifier") or {}
    for candidate_key in (
        verifier.get("module_path"),
        record.get("verifier_module_path"),
        record.get("module_path"),
    ):
        key = _normalize_path_key(candidate_key)
        if key and key in schema_map:
            record["witness_schema"] = schema_map[key]
            break
    return record


# ---------------------------------------------------------------------------
# Tokeniser
# ---------------------------------------------------------------------------

def _make_token_counter(model_name_or_path: str | None) -> Callable[[str], int]:
    """Return a ``str -> int`` token counter using the Qwen tokenizer.

    Falls back to a whitespace-word approximation if transformers is
    unavailable or the model files cannot be loaded (e.g. offline dev).
    """
    if model_name_or_path is None:
        # Whitespace approximation. Roughly correct order of magnitude for
        # the validation gate; we still report it in stats so the user
        # knows whether the real tokeniser was used.
        logger.warning(
            "No tokenizer specified - using whitespace approximation. "
            "Pass --tokenizer to use the Qwen tokenizer for the real check."
        )
        def _approx(text: str) -> int:
            # 1 token ~ 0.75 words for English; this is a rough proxy.
            return int(len(text.split()) * 1.33)
        return _approx

    try:
        from transformers import AutoTokenizer  # type: ignore
    except ImportError:
        logger.warning(
            "transformers not installed; falling back to whitespace approx."
        )
        return _make_token_counter(None)

    try:
        tok = AutoTokenizer.from_pretrained(model_name_or_path)
    except Exception as exc:
        logger.warning(
            "Could not load tokenizer %r (%s); falling back to approx.",
            model_name_or_path, exc,
        )
        return _make_token_counter(None)

    def _count(text: str) -> int:
        # ``add_special_tokens=False`` so the count reflects the message body
        # rather than the chat-template wrappers. We add a fixed margin for
        # those wrappers downstream.
        return len(tok.encode(text, add_special_tokens=False))

    logger.info("Using tokenizer: %s", model_name_or_path)
    return _count


# ---------------------------------------------------------------------------
# Record shaping
# ---------------------------------------------------------------------------

def _record_to_user_message(record: dict) -> str:
    """Mirror of the shared v2 user-message builder.

    The shared helper keeps the witness schema hint aligned between split
    generation and eval-time reconstruction.
    """
    return build_v2_user_message(record)


def _verifier_meta_for_loader(record: dict) -> dict:
    """Flat per-record verifier metadata that the RLVR loader will surface as
    Dataset columns and TRL will forward to the reward fn as kwargs.
    """
    v = record.get("verifier") or {}
    return {
        "verifier_module_path": v.get("module_path"),
        "n_hyp": v.get("n_hyp"),
        "neg_q_index": v.get("neg_q_index"),
        "n_conditions": v.get("n_conditions"),
        "theorem_id": record.get("theorem_id"),
    }


def _sft_messages(user_msg: str, assistant_target: str) -> dict:
    return {
        "messages": [
            {"role": "system", "content": V2_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": assistant_target},
        ]
    }


def _rlvr_messages(user_msg: str, record: dict) -> dict:
    base = {
        "messages": [
            {"role": "system", "content": V2_SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]
    }
    base.update(_verifier_meta_for_loader(record))
    return base


# ---------------------------------------------------------------------------
# Stratified splitting (over the strict pool only)
# ---------------------------------------------------------------------------

@dataclass
class SplitAllocation:
    sft: list[dict] = field(default_factory=list)
    test: list[dict] = field(default_factory=list)
    rlvr_strict: list[dict] = field(default_factory=list)


def _stratified_split(
    strict_pool: list[dict],
    sft_size: int,
    test_size: int,
    seed: int,
) -> tuple[SplitAllocation, dict]:
    """Stratified-by-domain split.

    Allocation rule: per domain ``d`` with count ``n_d``, draw
    ``round(n_d / N * sft_size)`` SFT and ``round(n_d / N * test_size)`` test
    records, plus a small rounding correction at the end so the totals match
    requested sizes exactly (drawn from / returned to RLVR-strict).
    """
    rng = random.Random(seed)
    by_domain: dict[str, list[dict]] = defaultdict(list)
    for rec in strict_pool:
        by_domain[rec.get("domain", "Unknown")].append(rec)

    total = len(strict_pool)
    if total == 0:
        raise ValueError("strict pool is empty; cannot build splits")
    if sft_size + test_size > total:
        raise ValueError(
            f"sft_size ({sft_size}) + test_size ({test_size}) = "
            f"{sft_size + test_size} exceeds strict-pool size ({total})"
        )

    alloc = SplitAllocation()
    domain_stats: dict[str, dict] = {}
    for domain, recs in sorted(by_domain.items()):
        rng.shuffle(recs)
        n = len(recs)
        prop = n / total
        n_sft = min(max(0, round(prop * sft_size)), n)
        n_test = min(max(0, round(prop * test_size)), n - n_sft)
        n_rlvr = n - n_sft - n_test
        alloc.sft.extend(recs[:n_sft])
        alloc.test.extend(recs[n_sft : n_sft + n_test])
        alloc.rlvr_strict.extend(recs[n_sft + n_test :])
        domain_stats[domain] = {
            "strict_total": n, "sft": n_sft, "test": n_test,
            "rlvr_strict": n_rlvr,
        }

    # Rounding correction against the RLVR-strict pool so totals match.
    def _adjust(target: list[dict], pool: list[dict], desired: int) -> None:
        diff = len(target) - desired
        if diff > 0:
            pool.extend(target[desired:])
            del target[desired:]
        elif diff < 0:
            needed = -diff
            target.extend(pool[:needed])
            del pool[:needed]

    _adjust(alloc.sft, alloc.rlvr_strict, sft_size)
    _adjust(alloc.test, alloc.rlvr_strict, test_size)

    rng.shuffle(alloc.sft)
    rng.shuffle(alloc.test)
    rng.shuffle(alloc.rlvr_strict)
    return alloc, domain_stats


# ---------------------------------------------------------------------------
# SFT target building (with oracle validation + truncation)
# ---------------------------------------------------------------------------

@dataclass
class SFTBuildOutcome:
    record: dict
    target: Optional[str]
    user_msg: str
    skip_reason: Optional[str]
    truncated: bool
    user_tokens: int
    target_tokens: int
    oracle_reward: Optional[float]


def _build_one_sft(
    record: dict,
    token_counter: Callable[[str], int],
    max_user_tokens: int,
    max_target_tokens: int,
    oracle_timeout: float,
) -> SFTBuildOutcome:
    user_msg = _record_to_user_message(record)
    user_tokens = token_counter(user_msg)

    br: BuildResult = build_sft_target(record)
    if br.target is None:
        return SFTBuildOutcome(
            record=record, target=None, user_msg=user_msg,
            skip_reason=br.skip_reason, truncated=False,
            user_tokens=user_tokens, target_tokens=0, oracle_reward=None,
        )

    target = br.target
    truncated = False
    if token_counter(target) > max_target_tokens:
        target, truncated = truncate_target_to_fit(
            target,
            witness=str(record.get("canonical_witness", "")),
            token_counter=token_counter,
            max_tokens=max_target_tokens,
        )

    # Sanity: tag must still parse after potential truncation.
    parsed = parse_counterexample_tag(target)
    if not parsed.format_ok or parsed.payload != (record.get("canonical_witness") or "").strip():
        return SFTBuildOutcome(
            record=record, target=None, user_msg=user_msg,
            skip_reason="tag_unparseable_after_truncation", truncated=truncated,
            user_tokens=user_tokens, target_tokens=token_counter(target),
            oracle_reward=None,
        )

    # Hard gate: round-trip oracle reward must be positive.
    try:
        bd = compute_reward_oracle(
            record=record,
            completion_text=target,
            task_mode="counterexample_only",
            timeout_seconds=oracle_timeout,
        )
    except Exception as exc:
        return SFTBuildOutcome(
            record=record, target=None, user_msg=user_msg,
            skip_reason=f"oracle_exception:{type(exc).__name__}",
            truncated=truncated, user_tokens=user_tokens,
            target_tokens=token_counter(target), oracle_reward=None,
        )

    if bd.total <= 0:
        return SFTBuildOutcome(
            record=record, target=None, user_msg=user_msg,
            skip_reason=f"oracle_nonpositive_reward({bd.reason})",
            truncated=truncated, user_tokens=user_tokens,
            target_tokens=token_counter(target), oracle_reward=bd.total,
        )

    return SFTBuildOutcome(
        record=record, target=target, user_msg=user_msg,
        skip_reason=None, truncated=truncated,
        user_tokens=user_tokens, target_tokens=token_counter(target),
        oracle_reward=bd.total,
    )


# ---------------------------------------------------------------------------
# Stats helpers
# ---------------------------------------------------------------------------

def _token_histogram(token_counts: list[int]) -> dict:
    if not token_counts:
        return {"count": 0}
    sorted_c = sorted(token_counts)
    def pct(p: float) -> int:
        if not sorted_c:
            return 0
        idx = max(0, min(len(sorted_c) - 1, int(round(p * (len(sorted_c) - 1)))))
        return sorted_c[idx]
    return {
        "count": len(sorted_c),
        "min": sorted_c[0], "p50": pct(0.5), "p95": pct(0.95),
        "p99": pct(0.99), "max": sorted_c[-1],
        "mean": round(sum(sorted_c) / len(sorted_c), 1),
    }


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def build_splits(
    input_path: Path,
    sft_path: Path,
    rlvr_path: Path,
    test_path: Path,
    stats_path: Path,
    *,
    witness_schema_path: Path | None,
    sft_size: int,
    test_size: int,
    seed: int,
    tokenizer_model: str | None,
    max_user_tokens: int,
    max_target_tokens: int,
    oracle_timeout: float,
    oracle_workers: int,
) -> dict:
    if not input_path.exists():
        raise FileNotFoundError(f"Input not found: {input_path}")

    logger.info("Loading %s", input_path)
    records = _load_jsonl(input_path)
    logger.info("Loaded %d records", len(records))

    if not records:
        raise ValueError("Input is empty")

    schema_map = _load_witness_schema_map(witness_schema_path)
    if schema_map:
        logger.info("Loaded %d witness schema entries from %s", len(schema_map), witness_schema_path)
        for record in records:
            _attach_witness_schema(record, schema_map)

    n_with_schema = sum(1 for record in records if (record.get("witness_schema") or "").strip())
    logger.info("Witness schemas attached to %d/%d records", n_with_schema, len(records))

    # Partition into strict + loose pools.
    strict_pool: list[dict] = []
    loose_only_pool: list[dict] = []
    for r in records:
        verifier_ok = bool((r.get("verifier") or {}).get("module_path"))
        witness_ok = bool(r.get("canonical_witness")) and bool(r.get("witness_passes_verifier"))
        if verifier_ok and witness_ok:
            strict_pool.append(r)
        elif verifier_ok:
            loose_only_pool.append(r)
        # records without any verifier are silently dropped (none in current sample)
    logger.info(
        "Pool sizes - strict=%d (sft/test/rlvr-strict), loose-only=%d (rlvr-loose)",
        len(strict_pool), len(loose_only_pool),
    )

    alloc, domain_stats = _stratified_split(strict_pool, sft_size, test_size, seed)
    logger.info(
        "Initial split - sft=%d, test=%d, rlvr_strict=%d",
        len(alloc.sft), len(alloc.test), len(alloc.rlvr_strict),
    )

    token_counter = _make_token_counter(tokenizer_model)

    # Build SFT targets in parallel
    logger.info("Building & oracle-validating SFT targets (workers=%d)...", oracle_workers)
    if oracle_workers > 1 and len(alloc.sft) > 1:
        with ThreadPoolExecutor(max_workers=oracle_workers) as pool:
            outcomes = list(pool.map(
                lambda r: _build_one_sft(
                    r, token_counter, max_user_tokens,
                    max_target_tokens, oracle_timeout,
                ),
                alloc.sft,
            ))
    else:
        outcomes = [
            _build_one_sft(r, token_counter, max_user_tokens, max_target_tokens, oracle_timeout)
            for r in alloc.sft
        ]

    sft_records_out: list[dict] = []
    rebatch_to_rlvr: list[dict] = []
    skip_reasons: Counter = Counter()
    truncation_count = 0
    sft_target_tokens: list[int] = []
    sft_user_tokens: list[int] = []
    sft_oracle_rewards: list[float] = []
    long_user_msgs = 0
    for o in outcomes:
        if o.target is None:
            skip_reasons[o.skip_reason or "unknown"] += 1
            rebatch_to_rlvr.append(o.record)  # still usable for RLVR
            continue
        if o.truncated:
            truncation_count += 1
        if o.user_tokens > max_user_tokens:
            long_user_msgs += 1
            logger.warning(
                "user prompt %s exceeds budget: %d > %d tokens (kept anyway; cannot truncate user)",
                o.record.get("theorem_id"), o.user_tokens, max_user_tokens,
            )
        sft_records_out.append(_sft_messages(o.user_msg, o.target))
        sft_target_tokens.append(o.target_tokens)
        sft_user_tokens.append(o.user_tokens)
        if o.oracle_reward is not None:
            sft_oracle_rewards.append(o.oracle_reward)

    logger.info(
        "SFT build complete - kept=%d, dropped=%d (%s), truncated=%d, over-budget-user=%d",
        len(sft_records_out), len(rebatch_to_rlvr), dict(skip_reasons),
        truncation_count, long_user_msgs,
    )

    # Build RLVR records
    # RLVR pool = remaining strict (RLVR-strict) + records that were SFT-eligible
    # but failed the oracle gate + the loose-only pool.
    rlvr_pool = alloc.rlvr_strict + rebatch_to_rlvr + loose_only_pool
    # Shuffle once more for the merged pool (deterministic via seed offset).
    random.Random(seed + 1).shuffle(rlvr_pool)
    rlvr_records_out: list[dict] = []
    rlvr_user_tokens: list[int] = []
    for r in rlvr_pool:
        user_msg = _record_to_user_message(r)
        rlvr_records_out.append(_rlvr_messages(user_msg, r))
        rlvr_user_tokens.append(token_counter(user_msg))

    # Test records (raw v2 schema preserved)
    # Re-validate that each test record's canonical witness still scores
    # positive - same logic the SFT gate uses. Records that fail are pushed
    # back into RLVR (where they belong as known-tricky prompts).
    test_records_out: list[dict] = []
    test_pushback_to_rlvr: list[dict] = []
    test_oracle_rewards: list[float] = []
    for r in alloc.test:
        try:
            bd = compute_reward_oracle(
                record=r,
                completion_text=f"<reasoning>n/a</reasoning>\n[COUNTEREXAMPLE: {r.get('canonical_witness')}]",
                task_mode="counterexample_only",
                timeout_seconds=oracle_timeout,
            )
        except Exception as exc:
            logger.warning(
                "test record %s oracle exception (%s); pushing back to RLVR",
                r.get("theorem_id"), exc,
            )
            test_pushback_to_rlvr.append(r)
            continue
        if bd.total <= 0:
            logger.warning(
                "test record %s oracle reward %.3f (%s); pushing back to RLVR",
                r.get("theorem_id"), bd.total, bd.reason,
            )
            test_pushback_to_rlvr.append(r)
            continue
        test_records_out.append(r)
        test_oracle_rewards.append(bd.total)

    if test_pushback_to_rlvr:
        for r in test_pushback_to_rlvr:
            user_msg = _record_to_user_message(r)
            rlvr_records_out.append(_rlvr_messages(user_msg, r))
            rlvr_user_tokens.append(token_counter(user_msg))

    # Write outputs
    _write_jsonl(sft_path, sft_records_out)
    _write_jsonl(rlvr_path, rlvr_records_out)
    _write_jsonl(test_path, test_records_out)
    logger.info("Wrote SFT  -> %s (%d records)", sft_path, len(sft_records_out))
    logger.info("Wrote RLVR -> %s (%d records)", rlvr_path, len(rlvr_records_out))
    logger.info("Wrote test -> %s (%d records)", test_path, len(test_records_out))

    # Stats sidecar
    stats = {
        "input_path": str(input_path),
        "input_records": len(records),
        "witness_schema_path": str(witness_schema_path) if witness_schema_path else None,
        "input_records_with_witness_schema": n_with_schema,
        "pools": {
            "strict": len(strict_pool),
            "loose_only": len(loose_only_pool),
        },
        "split_sizes": {
            "sft_target": sft_size,
            "test_target": test_size,
            "sft_actual": len(sft_records_out),
            "test_actual": len(test_records_out),
            "rlvr_actual": len(rlvr_records_out),
        },
        "domain_breakdown_strict_pool": domain_stats,
        "sft_drops": dict(skip_reasons),
        "sft_truncated_count": truncation_count,
        "sft_user_prompt_over_budget_count": long_user_msgs,
        "test_pushed_back_to_rlvr": len(test_pushback_to_rlvr),
        "tokenizer": tokenizer_model or "whitespace_approx",
        "max_user_tokens": max_user_tokens,
        "max_target_tokens": max_target_tokens,
        "sft_target_tokens": _token_histogram(sft_target_tokens),
        "sft_user_tokens": _token_histogram(sft_user_tokens),
        "rlvr_user_tokens": _token_histogram(rlvr_user_tokens),
        "sft_oracle_rewards": _token_histogram([int(r * 1000) for r in sft_oracle_rewards]),
        "test_oracle_rewards": _token_histogram([int(r * 1000) for r in test_oracle_rewards]),
        "seed": seed,
    }
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    with stats_path.open("w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=2, ensure_ascii=False)
    logger.info("Stats   -> %s", stats_path)
    return stats


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Build v2.0 SFT / RLVR / test splits from a migrated v2 dataset.",
    )
    p.add_argument("--input", default="data/algebra_counterexamples_v2.jsonl",
                   help="Migrated v2 JSONL (default: data/algebra_counterexamples_v2.jsonl)")
    p.add_argument("--sft-output",  default="data/sft_data.jsonl")
    p.add_argument("--rlvr-output", default="data/rlvr_prompts.jsonl")
    p.add_argument("--test-output", default="data/test_set.jsonl")
    p.add_argument("--stats-output", default="data/dataset_stats.json")
    p.add_argument(
        "--witness-schema-input",
        default="data/witness_schemas.jsonl",
        help=(
            "Optional JSONL sidecar with witness schema strings keyed by verifier "
            "module_path/file. If present, its schema is merged into the input v2 records."
        ),
    )
    p.add_argument("--sft-size",  type=int, default=80,
                   help="Target SFT pool size (default: 80 for the sample)")
    p.add_argument("--test-size", type=int, default=40,
                   help="Target test pool size (default: 40 for the sample)")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--tokenizer", default="unsloth/Qwen3-4B",
        help=(
            "HF model / local path for the tokenizer used in token-budget "
            "checks. Use '' (empty string) to force the whitespace approx."
        ),
    )
    p.add_argument("--max-user-tokens",   type=int, default=1024)
    p.add_argument("--max-target-tokens", type=int, default=1024)
    p.add_argument("--oracle-timeout", type=float, default=8.0)
    p.add_argument("--oracle-workers", type=int, default=4)
    return p


def main() -> None:
    args = _build_parser().parse_args()
    tokenizer = args.tokenizer if args.tokenizer != "" else None
    try:
        build_splits(
            input_path=Path(args.input),
            sft_path=Path(args.sft_output),
            rlvr_path=Path(args.rlvr_output),
            test_path=Path(args.test_output),
            stats_path=Path(args.stats_output),
            witness_schema_path=Path(args.witness_schema_input) if args.witness_schema_input else None,
            sft_size=args.sft_size,
            test_size=args.test_size,
            seed=args.seed,
            tokenizer_model=tokenizer,
            max_user_tokens=args.max_user_tokens,
            max_target_tokens=args.max_target_tokens,
            oracle_timeout=args.oracle_timeout,
            oracle_workers=args.oracle_workers,
        )
    except (FileNotFoundError, ValueError) as exc:
        logger.error("Build failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
