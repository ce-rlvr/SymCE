"""
Master pipeline: theorem extraction -> mutation -> LLM generation -> verification.

Output is a JSONL file at data/algebra_counterexamples.jsonl where every line
is a verified (false_conjecture, counterexample_code, verification_trace) record.

Failed attempts are written to data/algebra_counterexamples_failures.jsonl for
debugging and reward-model analysis.

Usage:
    python pipeline.py                          # hardcoded fallback theorems
    python pipeline.py --config configs/default.yaml
    python pipeline.py --config configs/default.yaml --max-retries 5
    python pipeline.py --use-lean               # LeanDojo extraction (needs Lean 4)
    python pipeline.py --output data/out.jsonl
    python pipeline.py --dry-run                # skip LLM calls, test structure only

Configuration priority (highest first):
    1. CLI flag explicitly provided on the command line
    2. Values from --config <path>.yaml under the [pipeline] section
    3. Dataclass defaults
"""

import argparse
import csv
import json
import logging
import random
import re
import sys
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field, fields
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from src.extract_theorems import get_theorems
from src.generator_llm import start_generation_session, correct_from_session
from src.mutate_and_prompt import build_prompt, get_droppable_hypotheses, mutate_theorem
from src.verifier import execute_and_verify
from training.common.config_loader import load_config_for_section

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Pipeline configuration
# ---------------------------------------------------------------------------


@dataclass
class PipelineConfig:
    # Theorem source
    use_lean: bool = False
    input_theorems: Optional[str] = None

    # Generation
    output: str = "data/algebra_counterexamples.jsonl"
    max_retries: int = 3
    workers: int = 1
    dry_run: bool = False

    # Attempts logging (None => default next to --output)
    attempts_log: Optional[str] = None
    attempts_csv: Optional[str] = None

    # Split flow
    only_split: bool = False
    skip_split: bool = False
    split_seed: int = 42
    sft_size: int = 1300
    test_size: int = 300
    sft_output: Optional[str] = None
    rlvr_output: Optional[str] = None
    test_output: Optional[str] = None


# ---------------------------------------------------------------------------
# Record I/O  (thread-safe writes when --workers > 1)
# ---------------------------------------------------------------------------

_write_lock = threading.Lock()

SFT_RLVR_SYSTEM_PROMPT = (
    "You are an expert mathematical programmer. "
    "Given a false mathematical conjecture, write a Python script using SymPy or Z3 "
    "to computationally prove it is false. "
    "You must define a counterexample, verify the remaining hypotheses hold, "
    "and explicitly assert that the conclusion is False."
)

_ATTEMPT_CSV_FIELDS = [
    "theorem_id",
    "theorem_name",
    "attempt_number",
    "attempt_status",
    "dropped_hypothesis_name",
    "remaining_hypotheses_count",
    "verification_success",
    "negation_form_ok",
    "safety_ok",
    "timed_out",
    "syntax_error",
    "runtime_error",
    "exit_code",
    "error_message",
    "stderr_preview",
    "timestamp",
]


def _append_jsonl(path: Path, record: dict) -> None:
    """Append one JSON record to a JSONL file (thread-safe)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with _write_lock:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def _count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    with open(path, encoding="utf-8") as fh:
        return sum(1 for _ in fh)


def _attempt_to_csv_row(record: dict) -> dict:
    verification = record.get("verification_result", {}) or {}
    stderr_text = verification.get("stderr", "") or ""
    return {
        "theorem_id": record.get("theorem_id", ""),
        "theorem_name": record.get("theorem_name", ""),
        "attempt_number": record.get("attempt_number", ""),
        "attempt_status": record.get("attempt_status", ""),
        "dropped_hypothesis_name": record.get("dropped_hypothesis_name", ""),
        "remaining_hypotheses_count": len(record.get("remaining_hypotheses", [])),
        "verification_success": verification.get("success", False),
        "negation_form_ok": verification.get("negation_form_ok", False),
        "safety_ok": verification.get("safety_ok", False),
        "timed_out": verification.get("timed_out", False),
        "syntax_error": verification.get("syntax_error", False),
        "runtime_error": verification.get("runtime_error", False),
        "exit_code": verification.get("exit_code", ""),
        "error_message": verification.get("error_message", ""),
        "stderr_preview": stderr_text.replace("\n", "\\n")[:200],
        "timestamp": record.get("timestamp", ""),
    }


def _append_attempt_csv(path: Path, record: dict) -> None:
    """Append one attempt row to a CSV file (thread-safe, writes header once)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    row = _attempt_to_csv_row(record)
    with _write_lock:
        needs_header = not path.exists() or path.stat().st_size == 0
        with open(path, "a", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=_ATTEMPT_CSV_FIELDS)
            if needs_header:
                writer.writeheader()
            writer.writerow(row)


_HEADER_RE = re.compile(r"^\[FALSE CONJECTURE[^\]]*\]\n", re.MULTILINE)


def _strip_conjecture_header(text: str) -> str:
    """Remove the internal bookkeeping header from a false_conjecture string.

    Old records stored in JSONL before the leakage fix may start with:
        [FALSE CONJECTURE - dropped hypothesis: 'hN']
    Stripping it makes the user-facing text leakage-free for re-splits of
    existing data without requiring a full regeneration run.
    """
    return _HEADER_RE.sub("", text, count=1).strip()


def _load_seen_pairs(path: Path) -> set[str]:
    """Return the set of 'theorem_id:hypothesis_name' pairs already in path.

    Used to resume multi-hypothesis expansion runs without re-processing
    completed (theorem, dropped_hypothesis) variants.
    """
    if not path.exists():
        return set()
    seen: set[str] = set()
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                tid = record.get("theorem_id")
                hname = record.get("dropped_hypothesis_name")
                if tid and hname:
                    seen.add(f"{tid}:{hname}")
                elif tid:
                    # Legacy records without hypothesis name: key on theorem_id
                    # alone so they are not re-processed at the theorem level.
                    seen.add(f"{tid}:__unknown__")
            except json.JSONDecodeError:
                pass
    return seen


# ---------------------------------------------------------------------------
# Per-theorem processing
# ---------------------------------------------------------------------------


def _run_single_variant(
    theorem: dict,
    mutation: dict,
    output_path: Path,
    attempts_path: Path | None,
    attempts_csv_path: Path | None,
    failures_path: Path,
    ill_defined_path: Path | None = None,
    true_statements_path: Path | None = None,
    max_retries: int = 3,
    dry_run: bool = False,
) -> dict:
    """
    Run the generate -> verify retry loop for one specific (theorem, dropped_hypothesis) pair.

    Returns {"attempts": int, "success": bool, "execution_success": bool}.
    """
    hyp_name = mutation["dropped_hypothesis"]["name"]
    label = f"{theorem['id']}:{hyp_name}"

    user_prompt = build_prompt(mutation)
    variant_stats = {"attempts": 0, "success": False, "execution_success": False, "ill_defined": False, "statement_true": False}
    last_record: dict | None = None
    chat_session = None
    last_code = ""
    last_error = ""

    logger.info(f"[{label}] Starting (dropped '{hyp_name}')")

    for attempt in range(1, max_retries + 1):
        variant_stats["attempts"] += 1
        logger.info(f"[{label}] Attempt {attempt}/{max_retries}...")

        if dry_run:
            code = "# DRY RUN PLACEHOLDER\nprint('dry run - no LLM call made')\n"
        elif attempt == 1:
            try:
                chat_session, code = start_generation_session(user_prompt)
            except RuntimeError as exc:
                logger.error(f"[{label}] LLM failed: {exc}")
                break
        else:
            try:
                code = correct_from_session(chat_session, last_code, last_error)
            except RuntimeError as exc:
                logger.error(f"[{label}] LLM correction failed: {exc}")
                break

        if code == "[ILL_DEFINED]":
            logger.warning(f"[{label}] Model states the variant is ILL_DEFINED")
            variant_stats["ill_defined"] = True
            verification = {"success": False, "error_message": "ILL_DEFINED", "negation_form_ok": False}
            last_record = _build_record(theorem, mutation, code, verification, attempt)
            last_record["attempt_status"] = "ill_defined"
            if ill_defined_path and not dry_run:
                _append_jsonl(ill_defined_path, last_record)
            return variant_stats
        elif code == "[STATEMENT_IS_TRUE]":
            logger.warning(f"[{label}] Model states the variant is STATEMENT_IS_TRUE")
            variant_stats["statement_true"] = True
            verification = {"success": False, "error_message": "STATEMENT_IS_TRUE", "negation_form_ok": False}
            last_record = _build_record(theorem, mutation, code, verification, attempt)
            last_record["attempt_status"] = "statement_true"
            if true_statements_path and not dry_run:
                _append_jsonl(true_statements_path, last_record)
            return variant_stats

        verification = execute_and_verify(code)
        last_record = _build_record(theorem, mutation, code, verification, attempt)

        if verification.get("success"):
            if dry_run or verification.get("negation_form_ok"):
                last_record["attempt_status"] = "success"
            else:
                last_record["attempt_status"] = "execution_only"
        else:
            last_record["attempt_status"] = "failed"

        if attempts_path is not None and not dry_run:
            _append_jsonl(attempts_path, last_record)
        if attempts_csv_path is not None and not dry_run:
            _append_attempt_csv(attempts_csv_path, last_record)

        if verification["success"]:
            variant_stats["execution_success"] = True
            negation_ok = verification["negation_form_ok"]
            logger.info(
                f"[{label}] SUCCESS on attempt {attempt} "
                f"(negation_form_ok={negation_ok})"
            )
            if dry_run or negation_ok:
                if not dry_run:
                    _append_jsonl(output_path, last_record)
                variant_stats["success"] = True
                return variant_stats

            logger.warning(
                f"[{label}] Execution passed but negation-form check failed; "
                "retrying with strict correction prompt."
            )
            last_code = code
            last_error = (
                "Negation-form check failed. The script executed successfully but is "
                "logically invalid for this task. You must assert the conclusion is "
                "FALSE using one of: assert not <expr>, assert <lhs> != <rhs>, "
                "assert <expr> == False, or assert <expr> is False."
            )
            continue

        last_code = code
        last_error = verification.get("stderr") or verification.get("error_message", "")
        logger.warning(f"[{label}] Attempt {attempt} failed: {verification['error_message']}")
        if verification["stderr"]:
            logger.debug(f"  stderr: {verification['stderr'][:300]}")

    if last_record is not None and not dry_run:
        _append_jsonl(failures_path, last_record)
        logger.info(f"[{label}] All {max_retries} attempts failed.")

    return variant_stats


def process_theorem(
    theorem: dict,
    output_path: Path,
    attempts_path: Path | None,
    attempts_csv_path: Path | None,
    failures_path: Path,
    ill_defined_path: Path | None = None,
    true_statements_path: Path | None = None,
    max_retries: int = 3,
    dry_run: bool = False,
    seen_pairs: set[str] | None = None,
) -> dict:
    """
    Run the full mutation -> generate -> verify loop for ALL droppable hypotheses.

    Each (theorem, dropped_hypothesis) pair is processed as an independent record.
    Already-completed pairs (tracked by seen_pairs) are skipped to support resumable runs.

    Returns a stats dict:
        {
            theorem_id, theorem_name,
            variants_total,    # total droppable hypotheses
            variants_attempted, # newly processed this run
            variants_successful, variants_failed,
            attempts,          # total LLM calls across all variants
            skipped,           # True if theorem has no droppable hypotheses
            skip_reason,
        }
    """
    seen_pairs = seen_pairs or set()
    stats = {
        "theorem_id": theorem["id"],
        "theorem_name": theorem["name"],
        "attempts": 0,
        "variants_total": 0,
        "variants_attempted": 0,
        "variants_successful": 0,
        "variants_failed": 0,
        "variants_ill_defined": 0,
        "variants_statement_true": 0,
        "skipped": False,
        "skip_reason": "",
    }

    droppable = get_droppable_hypotheses(theorem)
    if not droppable:
        stats["skipped"] = True
        stats["skip_reason"] = "No droppable hypotheses"
        if attempts_path is not None and not dry_run:
            skip_record = _build_skip_record(theorem, stats["skip_reason"])
            _append_jsonl(attempts_path, skip_record)
        if attempts_csv_path is not None and not dry_run:
            skip_record = _build_skip_record(theorem, stats["skip_reason"])
            _append_attempt_csv(attempts_csv_path, skip_record)
        logger.info(f"[{theorem['id']}] Skipped, no droppable hypotheses")
        return stats

    stats["variants_total"] = len(droppable)

    for drop_index in range(len(droppable)):
        mutation = mutate_theorem(theorem, drop_index=drop_index)
        if mutation is None:
            continue

        hyp_name = mutation["dropped_hypothesis"]["name"]
        pair_key = f"{theorem['id']}:{hyp_name}"
        if pair_key in seen_pairs:
            logger.debug(f"[{theorem['id']}] Skipping already-done variant: {hyp_name}")
            continue

        stats["variants_attempted"] += 1
        variant_stats = _run_single_variant(
            theorem,
            mutation,
            output_path=output_path,
            attempts_path=attempts_path,
            attempts_csv_path=attempts_csv_path,
            failures_path=failures_path,
            ill_defined_path=ill_defined_path,
            true_statements_path=true_statements_path,
            max_retries=max_retries,
            dry_run=dry_run,
        )
        stats["attempts"] += variant_stats["attempts"]
        if variant_stats["success"]:
            stats["variants_successful"] += 1
        elif variant_stats.get("ill_defined"):
            stats["variants_ill_defined"] += 1
        elif variant_stats.get("statement_true"):
            stats["variants_statement_true"] += 1
        else:
            stats["variants_failed"] += 1

    return stats


def _build_record(
    theorem: dict,
    mutation: dict,
    code: str,
    verification: dict,
    attempt: int,
) -> dict:
    """Construct the JSONL record for one generation attempt."""
    return {
        "theorem_id": theorem["id"],
        "theorem_name": theorem["name"],
        "domain": theorem.get("domain", "Algebra"),
        "original_full_statement": theorem["full_statement"],
        "dropped_hypothesis": mutation["dropped_hypothesis"]["text"],
        "dropped_hypothesis_name": mutation["dropped_hypothesis"]["name"],
        "remaining_hypotheses": [h["text"] for h in mutation["remaining_hypotheses"]],
        "conclusion": mutation["conclusion"],
        # Clean prompt (no dropped-hypothesis name) - used in training and eval.
        "false_conjecture": mutation["false_conjecture"],
        # Internal version with bookkeeping header - for debugging only, never fed to the model.
        "false_conjecture_annotated": mutation.get("false_conjecture_annotated", ""),
        "counterexample_code": code,
        "verification_result": verification,
        "negation_form_validated": verification.get("negation_form_ok", False),
        "attempt_number": attempt,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        # P1c (original-theorem bounded-search validation) populates this field.
        # null here means "not yet checked"; P1 only carries the field through.
        "original_theorem_validated": theorem.get("original_theorem_validated"),
    }


def _build_skip_record(theorem: dict, reason: str) -> dict:
    """Construct a synthetic attempts-log record for skipped theorems."""
    return {
        "theorem_id": theorem["id"],
        "theorem_name": theorem["name"],
        "domain": theorem.get("domain", "Algebra"),
        "original_full_statement": theorem.get("full_statement", ""),
        "dropped_hypothesis": "",
        "dropped_hypothesis_name": "",
        "remaining_hypotheses": [],
        "conclusion": theorem.get("conclusion", ""),
        "false_conjecture": "",
        "counterexample_code": "",
        "verification_result": {
            "success": False,
            "error_message": reason,
        },
        "negation_form_validated": False,
        "attempt_number": 0,
        "attempt_status": "skipped",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Pipeline runner
# ---------------------------------------------------------------------------


def run_pipeline(
    theorems: list[dict],
    output_path: Path,
    attempts_path: Path | None = None,
    attempts_csv_path: Path | None = None,
    ill_defined_path: Path | None = None,
    true_statements_path: Path | None = None,
    max_retries: int = 3,
    dry_run: bool = False,
    num_workers: int = 1,
) -> dict:
    """
    Iterate over theorems, process each, and aggregate stats.

    Theorems already present in output_path (by theorem_id) are skipped so
    re-runs don't produce duplicate records.

    When num_workers > 1, theorems are processed in parallel using a thread
    pool - each theorem gets its own Gemini chat session, so there is no
    shared mutable state between workers.

    Returns:
        {
            total,
            already_done,
            successful,
            failed,
            skipped,
            execution_only,
            total_attempts,
        }
    """
    failures_path = output_path.parent / (output_path.stem + "_failures.jsonl")

    # Track (theorem_id, hypothesis_name) pairs already written to the output.
    # This allows resumable multi-hypothesis expansion: each theorem may have
    # multiple droppable hypotheses, and each (theorem, hypothesis) pair is an
    # independent record.
    seen_pairs = _load_seen_pairs(output_path)

    agg = {
        "total": len(theorems),
        "already_done_pairs": len(seen_pairs),
        "successful": 0,
        "failed": 0,
        "ill_defined": 0,
        "statement_true": 0,
        "skipped": 0,
        "total_attempts": 0,
    }

    if seen_pairs:
        logger.info(
            f"Resuming, {len(seen_pairs)} (theorem, hypothesis) pair(s) "
            f"already in {output_path.name}"
        )

    logger.info(
        f"Starting pipeline, {len(theorems)} theorem(s), "
        f"workers={num_workers}, max_retries={max_retries}"
    )

    def _process_and_update(theorem: dict) -> dict:
        return process_theorem(
            theorem,
            output_path=output_path,
            attempts_path=attempts_path,
            attempts_csv_path=attempts_csv_path,
            failures_path=failures_path,
            ill_defined_path=ill_defined_path,
            true_statements_path=true_statements_path,
            max_retries=max_retries,
            dry_run=dry_run,
            seen_pairs=seen_pairs,
        )

    if num_workers > 1:
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            future_to_thm = {
                executor.submit(_process_and_update, thm): thm for thm in theorems
            }
            for future in as_completed(future_to_thm):
                try:
                    stats = future.result()
                except Exception as exc:
                    thm = future_to_thm[future]
                    logger.error(f"[{thm['id']}] Unhandled exception: {exc}")
                    agg["failed"] += 1
                    continue
                agg["total_attempts"] += stats["attempts"]
                if stats["skipped"]:
                    agg["skipped"] += 1
                else:
                    agg["successful"] += stats["variants_successful"]
                    agg["failed"] += stats["variants_failed"]
                    agg["ill_defined"] += stats.get("variants_ill_defined", 0)
                    agg["statement_true"] += stats.get("variants_statement_true", 0)
    else:
        for i, theorem in enumerate(theorems, 1):
            logger.info(f"--- Theorem {i}/{len(theorems)}: {theorem['name']} ---")
            stats = _process_and_update(theorem)
            agg["total_attempts"] += stats["attempts"]
            if stats["skipped"]:
                agg["skipped"] += 1
            else:
                agg["successful"] += stats["variants_successful"]
                agg["failed"] += stats["variants_failed"]
                agg["ill_defined"] += stats.get("variants_ill_defined", 0)
                agg["statement_true"] += stats.get("variants_statement_true", 0)

    logger.info(
        f"Pipeline complete, {agg['successful']} new successes, "
        f"{agg['failed']} failed variants, {agg['ill_defined']} ill-defined variants, "
        f"{agg['statement_true']} true variants, {agg['skipped']} skipped theorems, "
        f"{agg['already_done_pairs']} pairs already done"
    )
    return agg


# ---------------------------------------------------------------------------
# Dataset statistics
# ---------------------------------------------------------------------------


def compute_and_export_dataset_stats(output_path: Path) -> dict:
    """Compute summary statistics for the verified JSONL and write dataset_stats.json.

    Exports: total records, unique theorems, avg variants per theorem,
    avg attempt number, per-domain breakdown, and variant distribution.
    """
    if not output_path.exists():
        return {}

    records: list[dict] = []
    with open(output_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    if not records:
        return {}

    theorem_ids: set[str] = set()
    domain_counts: Counter = Counter()
    attempt_numbers: list[int] = []
    variants_per_theorem: Counter = Counter()
    hypotheses_per_theorem: Counter = Counter()

    for rec in records:
        tid = rec.get("theorem_id", "")
        theorem_ids.add(tid)
        domain_counts[rec.get("domain", "Unknown")] += 1
        attempt_numbers.append(rec.get("attempt_number", 1))
        variants_per_theorem[tid] += 1

    n_theorems = len(theorem_ids)
    n_records = len(records)
    avg_variants = n_records / n_theorems if n_theorems > 0 else 0.0
    avg_attempts = sum(attempt_numbers) / len(attempt_numbers) if attempt_numbers else 0.0
    vcounts = list(variants_per_theorem.values())

    stats = {
        "total_verified_records": n_records,
        "unique_source_theorems": n_theorems,
        "avg_variants_per_theorem": round(avg_variants, 2),
        "avg_attempt_number_per_record": round(avg_attempts, 2),
        "by_domain": dict(sorted(domain_counts.items())),
        "theorem_variant_distribution": {
            "min": min(vcounts) if vcounts else 0,
            "max": max(vcounts) if vcounts else 0,
            "mean": round(avg_variants, 2),
        },
    }

    stats_path = output_path.parent / "dataset_stats.json"
    with open(stats_path, "w", encoding="utf-8") as fh:
        json.dump(stats, fh, indent=2, ensure_ascii=False)
    logger.info(f"Dataset statistics written to {stats_path}")
    return stats


# ---------------------------------------------------------------------------
# Data split  (SFT / RLVR / test)
# ---------------------------------------------------------------------------


def _record_to_user_message(record: dict) -> str:
    """Build a leakage-free user message from a verified record.

    Reconstructs the conjecture from structured fields when available, and
    falls back to stripping the header from the stored false_conjecture string.
    This handles both old records (with the '[FALSE CONJECTURE ...]' header) and
    new records (already clean) transparently.
    """
    remaining = record.get("remaining_hypotheses", [])
    conclusion = record.get("conclusion", "")
    if remaining and conclusion:
        bulleted = "\n - ".join(remaining)
        return (
            f"Claim: For all mathematical objects satisfying:\n"
            f" - {bulleted}\n"
            f"the following conclusion holds:\n"
            f"  {conclusion}"
        )
    # Fallback: strip any header from the stored conjecture string
    return _strip_conjecture_header(record.get("false_conjecture", ""))


def _record_to_sft_message(record: dict) -> dict:
    """Wrap a verified record as a chat-format SFT example (no hypothesis leakage)."""
    return {
        "messages": [
            {"role": "system", "content": SFT_RLVR_SYSTEM_PROMPT},
            {"role": "user", "content": _record_to_user_message(record)},
            {
                "role": "assistant",
                "content": f"```python\n{record['counterexample_code']}\n```",
            },
        ]
    }


def _record_to_rlvr_message(record: dict) -> dict:
    """Wrap a verified record as a prompt-only RLVR example (no assistant turn, no leakage)."""
    return {
        "messages": [
            {"role": "system", "content": SFT_RLVR_SYSTEM_PROMPT},
            {"role": "user", "content": _record_to_user_message(record)},
        ]
    }


def split_dataset(
    source_path: Path,
    sft_path: Path,
    rlvr_path: Path,
    test_path: Path,
    sft_size: int = 1300,
    test_size: int = 300,
    seed: int = 42,
) -> dict:
    """
    Split the verified JSONL into SFT, RLVR, and test sets.

    Uses a stratified split by domain so each domain is proportionally
    represented in all three output sets. SFT is written in chat messages
    format (system + user + assistant). RLVR omits the assistant turn.
    The test set keeps the full original record for rich evaluation.

    Returns a stats dict: total, sft, rlvr, test counts, and per-domain breakdown.
    """
    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    records: list[dict] = []
    with open(source_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    if len(records) == 0:
        raise ValueError(f"No records found in {source_path}")

    # Deduplicate by false_conjecture content (keeps first occurrence per unique text).
    # Source data may contain records with identical conjecture text but different IDs.
    seen_conjectures: set[str] = set()
    deduped: list[dict] = []
    for rec in records:
        key = rec.get("false_conjecture", "")
        if key not in seen_conjectures:
            seen_conjectures.add(key)
            deduped.append(rec)
    n_dupes = len(records) - len(deduped)
    if n_dupes:
        logger.info(f"Removed {n_dupes} duplicate records (same false_conjecture text)")
    records = deduped

    total = len(records)
    if sft_size + test_size > total:
        raise ValueError(
            f"sft_size ({sft_size}) + test_size ({test_size}) = {sft_size + test_size} "
            f"exceeds total records ({total})"
        )

    rng = random.Random(seed)

    by_domain: dict[str, list[dict]] = defaultdict(list)
    for rec in records:
        by_domain[rec.get("domain", "Unknown")].append(rec)

    sft_records: list[dict] = []
    test_records: list[dict] = []
    rlvr_records: list[dict] = []
    domain_stats: dict[str, dict] = {}

    for domain, domain_recs in sorted(by_domain.items()):
        rng.shuffle(domain_recs)
        n = len(domain_recs)
        proportion = n / total

        n_sft = min(max(0, round(proportion * sft_size)), n)
        n_test = min(max(0, round(proportion * test_size)), n - n_sft)
        n_rlvr = n - n_sft - n_test

        sft_records.extend(domain_recs[:n_sft])
        test_records.extend(domain_recs[n_sft : n_sft + n_test])
        rlvr_records.extend(domain_recs[n_sft + n_test :])
        domain_stats[domain] = {"total": n, "sft": n_sft, "test": n_test, "rlvr": n_rlvr}

    # Rounding across domains may land a few records off target - correct against RLVR pool.
    def _adjust(target: list[dict], pool: list[dict], desired: int) -> None:
        diff = len(target) - desired
        if diff > 0:
            pool.extend(target[desired:])
            del target[desired:]
        elif diff < 0:
            needed = -diff
            target.extend(pool[:needed])
            del pool[:needed]

    _adjust(sft_records, rlvr_records, sft_size)
    _adjust(test_records, rlvr_records, test_size)

    rng.shuffle(sft_records)
    rng.shuffle(rlvr_records)
    rng.shuffle(test_records)

    for path in (sft_path, rlvr_path, test_path):
        path.parent.mkdir(parents=True, exist_ok=True)

    with open(sft_path, "w", encoding="utf-8") as fh:
        for rec in sft_records:
            fh.write(json.dumps(_record_to_sft_message(rec), ensure_ascii=False) + "\n")

    with open(rlvr_path, "w", encoding="utf-8") as fh:
        for rec in rlvr_records:
            fh.write(json.dumps(_record_to_rlvr_message(rec), ensure_ascii=False) + "\n")

    with open(test_path, "w", encoding="utf-8") as fh:
        for rec in test_records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    return {
        "total": total,
        "sft": len(sft_records),
        "rlvr": len(rlvr_records),
        "test": len(test_records),
        "domain_stats": domain_stats,
    }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    """
    Build the argparse parser for pipeline.py.

    Every flag's argparse default is None so that CLI-vs-config-file resolution
    can detect "explicitly provided" values. Real defaults live in PipelineConfig.
    """
    parser = argparse.ArgumentParser(
        description="Generate verified algebraic counterexample dataset (Phase 1)"
    )
    parser.add_argument(
        "--config",
        default=None,
        metavar="PATH",
        help=(
            "Optional YAML config file. The [pipeline] section overrides "
            "dataclass defaults; CLI flags below override the config file."
        ),
    )
    parser.add_argument("--use-lean", default=None, action=argparse.BooleanOptionalAction,
                        help="Extract theorems from Lean 4 Mathlib via LeanDojo (default: False)")
    parser.add_argument("--input-theorems", default=None, metavar="PATH",
                        help="Path to a JSON file containing an array of theorem dicts.")
    parser.add_argument("--output", default=None, metavar="PATH",
                        help="Output JSONL file (default: data/algebra_counterexamples.jsonl)")
    parser.add_argument("--max-retries", type=int, default=None, metavar="N",
                        help="Max LLM attempts per theorem (default: 3)")
    parser.add_argument("--dry-run", default=None, action=argparse.BooleanOptionalAction,
                        help="Skip LLM calls - useful for testing pipeline structure")
    parser.add_argument("--workers", type=int, default=None, metavar="N",
                        help="Number of parallel workers for theorem processing (default: 1)")
    parser.add_argument("--attempts-log", default=None, metavar="PATH",
                        help="Optional JSONL file recording every generation attempt")
    parser.add_argument("--attempts-csv", default=None, metavar="PATH",
                        help="Optional CSV file recording every generation attempt")
    # Data-split flags
    parser.add_argument("--only-split", default=None, action=argparse.BooleanOptionalAction,
                        help="Skip generation; only re-split the existing output JSONL")
    parser.add_argument("--skip-split", default=None, action=argparse.BooleanOptionalAction,
                        help="Run generation but skip the data-split step at the end")
    parser.add_argument("--split-seed", type=int, default=None, metavar="N",
                        help="Random seed for the stratified split (default: 42)")
    parser.add_argument("--sft-size", type=int, default=None, metavar="N",
                        help="Number of records in the SFT set (default: 1300)")
    parser.add_argument("--test-size", type=int, default=None, metavar="N",
                        help="Number of records in the test set (default: 300)")
    parser.add_argument("--sft-output", default=None, metavar="PATH",
                        help="SFT output path (default: <output_dir>/sft_data.jsonl)")
    parser.add_argument("--rlvr-output", default=None, metavar="PATH",
                        help="RLVR prompts output path (default: <output_dir>/rlvr_prompts.jsonl)")
    parser.add_argument("--test-output", default=None, metavar="PATH",
                        help="Test set output path (default: <output_dir>/test_set.jsonl)")
    return parser


def _resolve_config(argv: list[str] | None = None) -> PipelineConfig:
    """Parse CLI + optional YAML config and return a populated PipelineConfig."""
    args = _build_parser().parse_args(argv)
    # Map argparse `dest` names back to dataclass field names.
    # argparse already handles --some-flag -> some_flag automatically.
    cfg = load_config_for_section(
        cfg_class=PipelineConfig,
        section="pipeline",
        config_path=args.config,
        cli_namespace=args,
    )
    return cfg


def main() -> None:
    cfg = _resolve_config()

    output_path = Path(cfg.output)
    output_dir = output_path.parent

    sft_path = Path(cfg.sft_output) if cfg.sft_output else output_dir / "sft_data.jsonl"
    rlvr_path = Path(cfg.rlvr_output) if cfg.rlvr_output else output_dir / "rlvr_prompts.jsonl"
    test_path = Path(cfg.test_output) if cfg.test_output else output_dir / "test_set.jsonl"

    agg = None

    if not cfg.only_split:
        if cfg.attempts_log:
            attempts_path = Path(cfg.attempts_log)
        else:
            attempts_path = output_path.parent / (output_path.stem + "_attempts.jsonl")

        if cfg.attempts_csv:
            attempts_csv_path = Path(cfg.attempts_csv)
        else:
            attempts_csv_path = output_path.parent / (output_path.stem + "_attempts.csv")

        ill_defined_path = output_path.parent / (output_path.stem + "_ill_defined.jsonl")
        true_statements_path = output_path.parent / (output_path.stem + "_true_statements.jsonl")

        theorems = get_theorems(use_lean=cfg.use_lean, input_file=cfg.input_theorems)
        if not theorems:
            logger.error("No theorems loaded - nothing to process. Exiting.")
            sys.exit(1)

        logger.info(f"Loaded {len(theorems)} theorems")

        agg = run_pipeline(
            theorems,
            output_path=output_path,
            attempts_path=attempts_path,
            attempts_csv_path=attempts_csv_path,
            ill_defined_path=ill_defined_path,
            true_statements_path=true_statements_path,
            max_retries=cfg.max_retries,
            dry_run=cfg.dry_run,
            num_workers=cfg.workers,
        )

        successful_records = _count_jsonl(output_path)
        dataset_stats = compute_and_export_dataset_stats(output_path)

        width = 60
        print(f"\n{'=' * width}")
        print("Pipeline Results")
        print(f"{'=' * width}")
        print(f"  Theorems in bank        : {agg['total']}")
        print(f"  Already-done pairs      : {agg['already_done_pairs']}")
        print(f"  New successes           : {agg['successful']}")
        print(f"  Failed variants         : {agg['failed']}")
        print(f"  Ill-defined variants    : {agg['ill_defined']}")
        print(f"  True-statement variants : {agg['statement_true']}")
        print(f"  Skipped (no hyps)       : {agg['skipped']}")
        print(f"  Total LLM attempts      : {agg['total_attempts']}")
        print(f"  Total verified records  : {successful_records}")
        if dataset_stats:
            print(f"  Unique source theorems  : {dataset_stats['unique_source_theorems']}")
            print(f"  Avg variants/theorem    : {dataset_stats['avg_variants_per_theorem']}")
        print(f"  Output file             : {output_path}")
        print(f"  Attempts JSONL          : {attempts_path}")
        print(f"  Attempts CSV            : {attempts_csv_path}")
        print(f"{'=' * width}\n")

    if not cfg.skip_split:
        logger.info("Running stratified data split (SFT / RLVR / test)...")
        try:
            split_stats = split_dataset(
                source_path=output_path,
                sft_path=sft_path,
                rlvr_path=rlvr_path,
                test_path=test_path,
                sft_size=cfg.sft_size,
                test_size=cfg.test_size,
                seed=cfg.split_seed,
            )
        except (FileNotFoundError, ValueError) as exc:
            logger.error(f"Data split failed: {exc}")
            sys.exit(1)

        width = 60
        print(f"\n{'=' * width}")
        print("Data Split Results")
        print(f"{'=' * width}")
        print(f"  Source records     : {split_stats['total']}")
        print(f"  SFT records        : {split_stats['sft']}")
        print(f"  RLVR records       : {split_stats['rlvr']}")
        print(f"  Test records       : {split_stats['test']}")
        print(f"\n  Domain breakdown:")
        for domain, ds in sorted(split_stats["domain_stats"].items()):
            print(
                f"    {domain:<20}: {ds['total']:4d} total  "
                f"|  sft={ds['sft']:4d}  test={ds['test']:4d}  rlvr={ds['rlvr']:4d}"
            )
        print(f"\n  SFT output         : {sft_path}")
        print(f"  RLVR output        : {rlvr_path}")
        print(f"  Test output        : {test_path}")
        print(f"{'=' * width}\n")


if __name__ == "__main__":
    main()
