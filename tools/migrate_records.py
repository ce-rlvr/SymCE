"""
Migrate v1 pipeline records to the v2.0 schema with independent per-theorem verifiers.

For each record in the input JSONL, calls Gemini to generate:
  - A parametrised verifier module: data/verifiers/<domain>/<theorem_id>__<hyp_name>.py
  - A canonical witness expression evaluable in the module's namespace.

The output JSONL preserves ALL v1 fields and adds:
  - verifier.module_path (str): path to the generated .py module
  - verifier.condition_labels (list[str]): human-readable condition descriptions
  - verifier.n_conditions (int): total number of conditions
  - verifier.n_hyp (int): number of remaining-hypothesis conditions
  - verifier.neg_q_index (int): index of the negated-conclusion condition (always last)
  - canonical_witness (str | null): witness expression string
  - witness_passes_verifier (bool): True iff run_oracle returns all-True
  - verifier_generation_attempts (int): number of Gemini calls used
  - migration_failed (bool): True if verifier or witness generation failed
  - original_theorem_validated (null): placeholder for P1c; always null in migration.

Resumable: skips records already present in the output JSONL by (theorem_id, hyp_name).

Usage:
    python tools/migrate_records.py [options]
    python tools/migrate_records.py --max-records 50 --output data/algebra_counterexamples_v2.jsonl
    python tools/migrate_records.py --config configs/full_run.yaml
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Optional

# Project root on sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(_PROJECT_ROOT / ".env")

from src.oracle.verifier_generator import generate_verifier

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Config dataclass
# ---------------------------------------------------------------------------

@dataclass
class MigrationConfig:
    input_path: str = "data/algebra_counterexamples.jsonl"
    output_path: str = "data/algebra_counterexamples_v2.jsonl"
    output_path_failures: str = ""  # Empty = auto-derive from output_path
    verifiers_dir: str = "data/verifiers"
    verifier_generator_model: str = "gemini-3.1-pro-preview"
    verifier_temperature: float = 0.2
    witness_temperature: float = 0.5
    max_records: int = 0          # 0 = unlimited
    workers: int = 16
    max_verifier_retries: int = 2
    sandbox_timeout_seconds: float = 8.0
    unit_test_suite_path: str = "tests/oracle/verifier_unit_tests.jsonl"
    audit_report_path: str = "data/verifier_audit_report.json"
    min_audit_pass_rate_per_domain: float = 0.90
    domains_in_audit_gate: list = field(default_factory=lambda: [
        "GroupTheory", "RingTheory", "FieldTheory", "LinearAlgebra", "NumberTheory"
    ])
    # Record-level retry configuration for transient errors (rate limits, timeouts, etc.)
    max_record_retries: int = 7
    record_retry_base_seconds: float = 1.0
    record_retry_jitter: float = 0.2


# ---------------------------------------------------------------------------
# Resumability
# ---------------------------------------------------------------------------

def _load_seen_pairs(output_path: Path) -> set[str]:
    """Return set of 'theorem_id:hyp_name' pairs already in the output JSONL."""
    seen: set[str] = set()
    if not output_path.exists():
        return seen
    with open(output_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                tid = rec.get("theorem_id", "")
                hyp = rec.get("dropped_hypothesis_name", "__unknown__")
                seen.add(f"{tid}:{hyp}")
            except json.JSONDecodeError:
                continue
    return seen


# ---------------------------------------------------------------------------
# Exponential backoff helper for record-level retries
# ---------------------------------------------------------------------------

def _is_transient_error_msg(error_msg: str) -> bool:
    """
    Check if an error message indicates a transient error worthy of retry.
    Returns True for rate limits, timeouts, server errors; False for permanent failures.
    """
    msg_lower = error_msg.lower() if error_msg else ""
    transient_indicators = (
        "503" in msg_lower,              # Service unavailable
        "500" in msg_lower,              # Internal server error
        "429" in msg_lower,              # Too many requests / rate limit
        "unavailable" in msg_lower,
        "quota" in msg_lower or "resource" in msg_lower,  # Resource exhausted
        "deadline" in msg_lower or "timeout" in msg_lower,
        "temporarily" in msg_lower,
        "demand" in msg_lower,
    )
    return any(transient_indicators)


def _migrate_one_impl(record: dict, cfg: MigrationConfig, verifiers_dir: Path) -> dict:
    """
    Core migration logic for one record.
    
    Returns a result dict. If result has migration_failed=True, caller will check
    if error is transient and retry accordingly.
    """
    result = generate_verifier(
        record=record,
        verifiers_dir=verifiers_dir,
        verifier_model=cfg.verifier_generator_model,
        verifier_temperature=cfg.verifier_temperature,
        witness_model=cfg.verifier_generator_model,
        witness_temperature=cfg.witness_temperature,
        max_retries=cfg.max_verifier_retries,
        sandbox_timeout=cfg.sandbox_timeout_seconds,
    )

    # Build enriched output record
    out = dict(record)  # preserve all v1 fields
    out["original_theorem_validated"] = None  # populated by P1c, not here

    if result.success and result.module_path is not None:
        out["verifier"] = {
            "module_path": result.module_path,
            "condition_labels": result.condition_labels,
            "n_conditions": result.n_conditions,
            "n_hyp": result.n_hyp,
            "neg_q_index": result.neg_q_index,
        }
        out["canonical_witness"] = result.canonical_witness
        out["witness_passes_verifier"] = result.witness_passes_verifier
        out["verifier_generation_attempts"] = result.generation_attempts
        out["migration_failed"] = False
    else:
        out["verifier"] = None
        out["canonical_witness"] = None
        out["witness_passes_verifier"] = False
        out["verifier_generation_attempts"] = result.generation_attempts
        out["migration_failed"] = True
        out["migration_error"] = result.error or "Unknown error"

    return out


def _retry_with_backoff_on_result(record: dict, cfg: MigrationConfig, verifiers_dir: Path, max_attempts: int) -> dict:
    """
    Retry record migration with exponential backoff on transient errors.
    
    Inspects the VerifierGenerationResult error message and retries if it indicates
    a transient problem (rate limit, 503, high demand, etc.).
    
    Args:
        record: The record being migrated
        cfg: Migration config
        verifiers_dir: Path to verifiers directory
        max_attempts: Max number of attempts
    
    Returns:
        Enriched record dict (success or failure)
    """
    tid = record.get("theorem_id", "?")
    hyp = record.get("dropped_hypothesis_name", "?")

    for attempt in range(max_attempts):
        try:
            result = _migrate_one_impl(record, cfg, verifiers_dir)
            
            # Check if the result indicates a transient error
            if result.get("migration_failed") and attempt < max_attempts - 1:
                error_msg = result.get("migration_error", "")
                if _is_transient_error_msg(error_msg):
                    # Transient error; retry with backoff
                    delay = cfg.record_retry_base_seconds * (2 ** attempt)
                    jitter = delay * cfg.record_retry_jitter * (2 * random.random() - 1)
                    wait = max(0.5, delay + jitter)
                    logger.warning(
                        "Transient error on %s:%s (attempt %d/%d): %s — retrying in %.1fs",
                        tid, hyp, attempt + 1, max_attempts, 
                        error_msg[:100], wait,
                    )
                    time.sleep(wait)
                    continue  # Retry
            
            # Either success, or a permanent error (don't retry)
            return result
        
        except Exception as exc:
            if attempt >= max_attempts - 1:
                logger.error(
                    "Unexpected exception on %s:%s after %d attempts: %s",
                    tid, hyp, attempt + 1, exc,
                )
                # Return failure record
                enriched = dict(record)
                enriched["verifier"] = None
                enriched["canonical_witness"] = None
                enriched["witness_passes_verifier"] = False
                enriched["verifier_generation_attempts"] = 0
                enriched["migration_failed"] = True
                enriched["migration_error"] = f"Exception: {exc}"
                enriched["original_theorem_validated"] = None
                return enriched
            
            # Transient exception; retry with backoff
            delay = cfg.record_retry_base_seconds * (2 ** attempt)
            jitter = delay * cfg.record_retry_jitter * (2 * random.random() - 1)
            wait = max(0.5, delay + jitter)
            logger.warning(
                "Exception on %s:%s (attempt %d/%d): %s — retrying in %.1fs",
                tid, hyp, attempt + 1, max_attempts, type(exc).__name__, wait,
            )
            time.sleep(wait)
    
    # Shouldn't reach here, but provide a fallback
    enriched = dict(record)
    enriched["verifier"] = None
    enriched["canonical_witness"] = None
    enriched["witness_passes_verifier"] = False
    enriched["verifier_generation_attempts"] = 0
    enriched["migration_failed"] = True
    enriched["migration_error"] = f"Max retries ({max_attempts}) exhausted"
    enriched["original_theorem_validated"] = None
    return enriched


def _migrate_one(record: dict, cfg: MigrationConfig, verifiers_dir: Path) -> dict:
    """
    Migrate one record with exponential backoff retry on transient errors.
    
    Returns an enriched record dict (always, never raises).
    Sets migration_failed=True on permanent failures.
    """
    max_attempts = cfg.max_record_retries + 1
    return _retry_with_backoff_on_result(record, cfg, verifiers_dir, max_attempts)


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

_write_lock = threading.Lock()


def _append_jsonl(path: Path, record: dict) -> None:
    with _write_lock:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Per-record migration
# ---------------------------------------------------------------------------

def _migrate_one_impl(record: dict, cfg: MigrationConfig, verifiers_dir: Path) -> dict:
    """
    Core migration logic for one record (may raise on transient errors).
    
    Called by _migrate_one() through the retry wrapper.
    Raises exceptions that _retry_with_backoff will retry on transient errors.
    """
    result = generate_verifier(
        record=record,
        verifiers_dir=verifiers_dir,
        verifier_model=cfg.verifier_generator_model,
        verifier_temperature=cfg.verifier_temperature,
        witness_model=cfg.verifier_generator_model,
        witness_temperature=cfg.witness_temperature,
        max_retries=cfg.max_verifier_retries,
        sandbox_timeout=cfg.sandbox_timeout_seconds,
    )

    # Build enriched output record
    out = dict(record)  # preserve all v1 fields
    out["original_theorem_validated"] = None  # populated by P1c, not here

    if result.success and result.module_path is not None:
        out["verifier"] = {
            "module_path": result.module_path,
            "condition_labels": result.condition_labels,
            "n_conditions": result.n_conditions,
            "n_hyp": result.n_hyp,
            "neg_q_index": result.neg_q_index,
        }
        out["canonical_witness"] = result.canonical_witness
        out["witness_passes_verifier"] = result.witness_passes_verifier
        out["verifier_generation_attempts"] = result.generation_attempts
        out["migration_failed"] = False
    else:
        out["verifier"] = None
        out["canonical_witness"] = None
        out["witness_passes_verifier"] = False
        out["verifier_generation_attempts"] = result.generation_attempts
        out["migration_failed"] = True
        out["migration_error"] = result.error or "Unknown error"

    return out


def _migrate_one(record: dict, cfg: MigrationConfig, verifiers_dir: Path) -> dict:
    """
    Migrate one record with exponential backoff retry on transient errors.
    
    Returns an enriched record dict (always, never raises).
    Sets migration_failed=True on permanent failures.
    """
    max_attempts = cfg.max_record_retries + 1
    return _retry_with_backoff_on_result(record, cfg, verifiers_dir, max_attempts)


# ---------------------------------------------------------------------------
# Main migration loop
# ---------------------------------------------------------------------------

def run_migration(cfg: MigrationConfig, root: Path) -> None:
    input_path = root / cfg.input_path
    output_path = root / cfg.output_path
    
    # Auto-derive failure output path if not set
    if not cfg.output_path_failures:
        # Replace <stem>.jsonl with <stem>_failures.jsonl
        base_name = output_path.name
        if base_name.endswith(".jsonl"):
            failure_name = base_name.replace(".jsonl", "_failures.jsonl")
        else:
            failure_name = base_name + "_failures.jsonl"
        output_path_failures = output_path.parent / failure_name
    else:
        output_path_failures = root / cfg.output_path_failures
    
    verifiers_dir = root / cfg.verifiers_dir

    if not input_path.exists():
        logger.error("Input file not found: %s", input_path)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    verifiers_dir.mkdir(parents=True, exist_ok=True)

    # Load all records
    records: list[dict] = []
    with open(input_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    logger.warning("Skipping malformed line: %s", exc)

    logger.info("Loaded %d records from %s", len(records), input_path)

    # Resumability: check both success and failures output files
    seen = _load_seen_pairs(output_path)
    seen.update(_load_seen_pairs(output_path_failures))
    logger.info("Already processed (success or failure): %d pairs", len(seen))

    # Filter to unprocessed records
    to_process: list[dict] = []
    for rec in records:
        tid = rec.get("theorem_id", "")
        hyp = rec.get("dropped_hypothesis_name", "__unknown__")
        if f"{tid}:{hyp}" not in seen:
            to_process.append(rec)

    if cfg.max_records > 0:
        to_process = to_process[: cfg.max_records]

    logger.info("Records to migrate: %d", len(to_process))

    if not to_process:
        logger.info("Nothing to do.")
        return

    # Counters
    n_success = 0
    n_failed = 0
    completed = 0

    def _process(record: dict) -> dict:
        return _migrate_one(record, cfg, verifiers_dir)

    workers = min(cfg.workers, len(to_process))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(_process, rec): rec for rec in to_process}
        for fut in as_completed(futures):
            completed += 1
            try:
                enriched = fut.result()
            except Exception as exc:
                original = futures[fut]
                logger.error(
                    "Unexpected error migrating %s:%s — %s",
                    original.get("theorem_id"), original.get("dropped_hypothesis_name"), exc,
                )
                # Write a failure record
                enriched = dict(original)
                enriched["verifier"] = None
                enriched["canonical_witness"] = None
                enriched["witness_passes_verifier"] = False
                enriched["verifier_generation_attempts"] = 0
                enriched["migration_failed"] = True
                enriched["migration_error"] = f"UnexpectedError: {exc}"
                enriched["original_theorem_validated"] = None

            _append_jsonl(output_path, enriched)
            if enriched.get("migration_failed"):
                n_failed += 1
            else:
                n_success += 1

            if completed % 100 == 0 or completed == len(to_process):
                logger.info(
                    "Progress: %d/%d — success=%d, failed=%d",
                    completed, len(to_process), n_success, n_failed,
                )

    logger.info(
        "Migration complete. Total=%d  Success=%d (%.1f%%)  Failed=%d",
        len(to_process), n_success,
        100 * n_success / len(to_process) if to_process else 0,
        n_failed,
    )
    logger.info("Successful migrations written to: %s", output_path)
    logger.info("Failed migrations written to: %s", output_path_failures)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Migrate v1 JSONL records to v2.0 schema with per-theorem verifiers."
    )
    p.add_argument("--config", default=None, metavar="PATH",
                   help="YAML config file (reads 'migration:' section)")
    p.add_argument("--input", default=None, metavar="PATH",
                   help="Source JSONL (default: data/algebra_counterexamples.jsonl)")
    p.add_argument("--output", default=None, metavar="PATH",
                   help="Output JSONL (default: data/algebra_counterexamples_v2.jsonl)")
    p.add_argument("--output-failures", default=None, metavar="PATH",
                   help="Separate JSONL for failed migrations (default: auto-derived from --output)")
    p.add_argument("--verifiers-dir", default=None, metavar="PATH",
                   help="Root directory for verifier modules (default: data/verifiers/)")
    p.add_argument("--max-records", type=int, default=None, metavar="N",
                   help="Process at most N records (0=unlimited). Run 50 first for dev sample.")
    p.add_argument("--workers", type=int, default=None, metavar="N",
                   help="Number of parallel workers (default: 16)")
    p.add_argument("--model", default=None, metavar="NAME",
                   help="Gemini model name for verifier generation")
    p.add_argument("--verifier-temp", type=float, default=None, metavar="T",
                   help="Temperature for verifier code generation (default: 0.2)")
    p.add_argument("--witness-temp", type=float, default=None, metavar="T",
                   help="Temperature for witness extraction (default: 0.5)")
    p.add_argument("--max-verifier-retries", type=int, default=None, metavar="N",
                   help="Max verifier generation retries (overrides config.max_verifier_retries)")
    p.add_argument("--max-record-retries", type=int, default=None, metavar="N",
                   help="Max record-level retries on transient errors like rate limits (default: 7)")
    p.add_argument("--record-retry-base-seconds", type=float, default=None, metavar="T",
                   help="Base delay for exponential backoff at record level (default: 1.0)")
    p.add_argument("--record-retry-jitter", type=float, default=None, metavar="T",
                   help="Jitter fraction for record-level retries (default: 0.2)")
    p.add_argument("--log-level", default="INFO",
                   choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    return p


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    cfg = MigrationConfig()

    # Overlay YAML config if provided
    if args.config:
        import yaml
        with open(args.config, encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        section = (raw or {}).get("migration", {}) or {}
        for f in fields(cfg):
            if f.name in section and section[f.name] is not None:
                setattr(cfg, f.name, section[f.name])

    # Overlay CLI flags
    if args.input is not None:
        cfg.input_path = args.input
    if args.output is not None:
        cfg.output_path = args.output
    if args.output_failures is not None:
        cfg.output_path_failures = args.output_failures
    if args.verifiers_dir is not None:
        cfg.verifiers_dir = args.verifiers_dir
    if args.max_records is not None:
        cfg.max_records = args.max_records
    if args.workers is not None:
        cfg.workers = args.workers
    if args.model is not None:
        cfg.verifier_generator_model = args.model
    if args.verifier_temp is not None:
        cfg.verifier_temperature = args.verifier_temp
    if args.witness_temp is not None:
        cfg.witness_temperature = args.witness_temp
    if args.max_verifier_retries is not None:
        cfg.max_verifier_retries = args.max_verifier_retries
    if args.max_record_retries is not None:
        cfg.max_record_retries = args.max_record_retries
    if args.record_retry_base_seconds is not None:
        cfg.record_retry_base_seconds = args.record_retry_base_seconds
    if args.record_retry_jitter is not None:
        cfg.record_retry_jitter = args.record_retry_jitter

    logger.info(
        "Migration config: input=%s output=%s output_failures=%s workers=%d "
        "max_records=%d max_record_retries=%d record_retry_base=%.2fs",
        cfg.input_path, cfg.output_path,
        cfg.output_path_failures if cfg.output_path_failures else "(auto)",
        cfg.workers, cfg.max_records,
        cfg.max_record_retries, cfg.record_retry_base_seconds,
    )

    run_migration(cfg, root=_PROJECT_ROOT)


if __name__ == "__main__":
    main()
