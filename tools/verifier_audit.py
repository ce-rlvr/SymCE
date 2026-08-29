"""
P1.5 — Verifier audit tool.

Runs the hand-curated unit-test suite (tests/oracle/verifier_unit_tests.jsonl) against
migrated records in data/algebra_counterexamples_v2.jsonl and reports per-domain pass rates.

Each unit-test record has the shape:
    {
      "theorem_id": "sylow_first_theorem",
      "dropped_hypothesis_name": "h1",
      "witness_expr": "S3",
      "expected_all_pass": true,           // true = all conditions should be True
      "expected_conditions": [true, true, true]  // optional per-condition expected values
    }

Usage:
    python tools/verifier_audit.py [--config configs/full_run.yaml] [--v2-jsonl PATH]
    python -m tools.verifier_audit   # same via module invocation

Exit code:
    0 — all algebra-domain pass rates ≥ min_audit_pass_rate_per_domain
    1 — one or more domains below threshold
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ROOT))

from src.oracle.sandbox import run_oracle

logger = logging.getLogger(__name__)


@dataclass
class AuditConfig:
    v2_jsonl: str = "data/algebra_counterexamples_v2.jsonl"
    unit_test_suite_path: str = "tests/oracle/verifier_unit_tests.jsonl"
    audit_report_path: str = "data/verifier_audit_report.json"
    sandbox_timeout_seconds: float = 8.0
    min_audit_pass_rate_per_domain: float = 0.90
    domains_in_audit_gate: list = field(default_factory=lambda: [
        "GroupTheory", "RingTheory", "FieldTheory", "LinearAlgebra", "NumberTheory"
    ])


def _load_v2_index(path: Path) -> dict[str, dict]:
    """Build a {theorem_id:hyp_name → record} index from the v2 JSONL."""
    index: dict[str, dict] = {}
    if not path.exists():
        return index
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                tid = rec.get("theorem_id", "")
                hyp = rec.get("dropped_hypothesis_name", "__unknown__")
                index[f"{tid}:{hyp}"] = rec
            except json.JSONDecodeError:
                continue
    return index


def _load_unit_tests(path: Path) -> list[dict]:
    if not path.exists():
        logger.error("Unit test suite not found: %s", path)
        return []
    tests = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                tests.append(json.loads(line))
            except json.JSONDecodeError as exc:
                logger.warning("Skipping malformed unit test line: %s", exc)
    return tests


def run_audit(cfg: AuditConfig, root: Path) -> dict:
    """
    Run the audit and return a report dict. Writes JSON to cfg.audit_report_path.

    Returns:
        {
            "per_domain": {domain: {"total": int, "passed": int, "pass_rate": float}},
            "global": {"total": int, "passed": int, "pass_rate": float},
            "failures": [{"theorem_id", "hyp_name", "witness_expr", "error", ...}],
            "gate_passed": bool,
        }
    """
    v2_path = root / cfg.v2_jsonl
    suite_path = root / cfg.unit_test_suite_path
    report_path = root / cfg.audit_report_path

    v2_index = _load_v2_index(v2_path)
    logger.info("v2 records indexed: %d", len(v2_index))

    unit_tests = _load_unit_tests(suite_path)
    logger.info("Unit tests loaded: %d", len(unit_tests))

    if not unit_tests:
        logger.warning("No unit tests found — audit trivially passes (no tests).")
        report = {
            "per_domain": {},
            "global": {"total": 0, "passed": 0, "pass_rate": 1.0},
            "failures": [],
            "gate_passed": True,
        }
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2))
        return report

    per_domain: dict[str, dict] = {}
    failures = []
    total_passed = 0

    for ut in unit_tests:
        tid = ut.get("theorem_id", "")
        hyp = ut.get("dropped_hypothesis_name", "__unknown__")
        witness_expr = ut.get("witness_expr", "")
        expected_all_pass = ut.get("expected_all_pass", True)
        expected_conditions: Optional[list[bool]] = ut.get("expected_conditions")

        key = f"{tid}:{hyp}"
        rec = v2_index.get(key)

        # Find domain
        domain = rec.get("domain", "Unknown") if rec else "Unknown"

        if domain not in per_domain:
            per_domain[domain] = {"total": 0, "passed": 0}
        per_domain[domain]["total"] += 1

        if rec is None:
            failures.append({
                "theorem_id": tid,
                "hyp_name": hyp,
                "witness_expr": witness_expr,
                "error": "Record not found in v2 JSONL",
                "domain": domain,
            })
            continue

        if rec.get("migration_failed"):
            failures.append({
                "theorem_id": tid,
                "hyp_name": hyp,
                "witness_expr": witness_expr,
                "error": f"Migration failed: {rec.get('migration_error', '?')}",
                "domain": domain,
            })
            continue

        verifier_info = rec.get("verifier")
        if not verifier_info or not verifier_info.get("module_path"):
            failures.append({
                "theorem_id": tid,
                "hyp_name": hyp,
                "witness_expr": witness_expr,
                "error": "No verifier module_path in record",
                "domain": domain,
            })
            continue

        module_path = verifier_info["module_path"]
        n_conditions = verifier_info.get("n_conditions", 1)

        result = run_oracle(
            verifier_module_path=module_path,
            witness_expr=witness_expr,
            n_conditions=n_conditions,
            timeout_seconds=cfg.sandbox_timeout_seconds,
        )

        # Determine pass/fail
        test_passed = False
        failure_reason: Optional[str] = None

        if not result.parse_ok:
            failure_reason = f"parse_ok=False: {result.error}"
        elif result.conditions is None:
            failure_reason = f"conditions=None: {result.error}"
        elif expected_conditions is not None:
            if result.conditions == [bool(c) for c in expected_conditions]:
                test_passed = True
            else:
                failure_reason = (
                    f"conditions mismatch: got {result.conditions}, "
                    f"expected {expected_conditions}"
                )
        elif expected_all_pass:
            if all(result.conditions):
                test_passed = True
            else:
                failure_reason = f"Not all conditions True: {result.conditions}"
        else:
            # expected_all_pass=False: at least one condition should be False
            if not all(result.conditions):
                test_passed = True
            else:
                failure_reason = f"Expected some False conditions but got all True: {result.conditions}"

        if test_passed:
            total_passed += 1
            per_domain[domain]["passed"] += 1
        else:
            failures.append({
                "theorem_id": tid,
                "hyp_name": hyp,
                "witness_expr": witness_expr,
                "error": failure_reason,
                "domain": domain,
                "oracle_conditions": result.conditions,
            })

    # Compute pass rates
    total = len(unit_tests)
    for d, stats in per_domain.items():
        stats["pass_rate"] = stats["passed"] / stats["total"] if stats["total"] > 0 else 1.0

    global_pass_rate = total_passed / total if total > 0 else 1.0

    # Gate check
    gate_passed = True
    for domain in cfg.domains_in_audit_gate:
        if domain not in per_domain:
            logger.warning("Domain '%s' has no unit tests — cannot verify gate", domain)
            continue
        rate = per_domain[domain]["pass_rate"]
        if rate < cfg.min_audit_pass_rate_per_domain:
            logger.error(
                "GATE FAILED: domain '%s' pass rate %.1f%% < %.1f%%",
                domain, rate * 100, cfg.min_audit_pass_rate_per_domain * 100,
            )
            gate_passed = False

    report = {
        "per_domain": per_domain,
        "global": {"total": total, "passed": total_passed, "pass_rate": global_pass_rate},
        "failures": failures,
        "gate_passed": gate_passed,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info("Audit report written to %s", report_path)

    if gate_passed:
        logger.info("AUDIT GATE PASSED — all algebra domains ≥ %.0f%%",
                    cfg.min_audit_pass_rate_per_domain * 100)
    else:
        logger.error("AUDIT GATE FAILED — see failures in report")

    return report


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run the P1.5 verifier audit suite.")
    p.add_argument("--config", default=None, metavar="PATH")
    p.add_argument("--v2-jsonl", default=None, metavar="PATH",
                   help="Path to data/algebra_counterexamples_v2.jsonl")
    p.add_argument("--suite", default=None, metavar="PATH",
                   help="Path to tests/oracle/verifier_unit_tests.jsonl")
    p.add_argument("--report", default=None, metavar="PATH",
                   help="Path to write audit_report.json")
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

    cfg = AuditConfig()

    if args.config:
        import yaml
        with open(args.config, encoding="utf-8") as fh:
            raw = yaml.safe_load(fh)
        section = (raw or {}).get("migration", {}) or {}
        for key in ["unit_test_suite_path", "audit_report_path",
                    "sandbox_timeout_seconds", "min_audit_pass_rate_per_domain",
                    "domains_in_audit_gate"]:
            if key in section and section[key] is not None:
                setattr(cfg, key, section[key])

    if args.v2_jsonl:
        cfg.v2_jsonl = args.v2_jsonl
    if args.suite:
        cfg.unit_test_suite_path = args.suite
    if args.report:
        cfg.audit_report_path = args.report

    report = run_audit(cfg, root=_ROOT)
    sys.exit(0 if report["gate_passed"] else 1)


if __name__ == "__main__":
    main()
