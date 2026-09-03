"""
Wall-clock probe for the v2.0 oracle reward path.

Loads a sample of records from data/algebra_counterexamples_v2.jsonl, feeds
each one's canonical_witness through compute_reward_oracle, and reports:

- per-call elapsed_ms (median, p95, max)
- parse_ok rate
- positive-reward rate
- reasons distribution
- breakdown of failures by oracle_error category

This is the oracle latency gate:
    median verifier execution <= 200 ms
    max <= 8 s (sandbox timeout)

Run from repo root:

    python -m tools.oracle_perf_probe --limit 50
    python -m tools.oracle_perf_probe --limit 50 --only-witness-passes
    python -m tools.oracle_perf_probe --limit 50 --seed 7 --out probe.json
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from training.rlvr.reward_oracle import compute_reward_oracle


def _load_records(
    path: Path,
    only_witness_passes: bool,
    limit: int,
    seed: int,
) -> list[dict]:
    records: list[dict] = []
    with path.open() as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            r = json.loads(raw)
            if r.get("migration_failed"):
                continue
            if only_witness_passes and not r.get("witness_passes_verifier", False):
                continue
            mp = r.get("verifier", {}).get("module_path")
            if not mp or not Path(mp).exists():
                continue
            records.append(r)
    rng = random.Random(seed)
    rng.shuffle(records)
    return records[:limit]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--input",
        type=Path,
        default=_REPO_ROOT / "data" / "algebra_counterexamples_v2.jsonl",
        help="v2 JSONL path",
    )
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument(
        "--only-witness-passes",
        action="store_true",
        help="filter to records with witness_passes_verifier=True only",
    )
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--timeout", type=float, default=8.0)
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="optional JSON dump of per-record results",
    )
    args = ap.parse_args()

    if not args.input.exists():
        sys.exit(f"input not found: {args.input}")

    records = _load_records(
        args.input,
        only_witness_passes=args.only_witness_passes,
        limit=args.limit,
        seed=args.seed,
    )
    if not records:
        sys.exit("no eligible records")

    print(f"Probing {len(records)} records (timeout={args.timeout}s)...\n")

    results: list[dict] = []
    elapsed_list: list[int] = []
    reasons: Counter = Counter()
    error_categories: Counter = Counter()
    pos_reward = 0
    parse_ok = 0
    t_wall_start = time.monotonic()

    for i, rec in enumerate(records, 1):
        cw = rec["canonical_witness"]
        completion = f"<reasoning>...</reasoning>\n[COUNTEREXAMPLE: {cw}]"
        bd = compute_reward_oracle(rec, completion, timeout_seconds=args.timeout)
        rid = f"{rec['theorem_id']}__{rec['dropped_hypothesis_name']}"

        elapsed_list.append(bd.oracle_elapsed_ms)
        reasons[bd.reason] += 1
        if bd.parse_ok:
            parse_ok += 1
        if bd.total > 0:
            pos_reward += 1

        if bd.oracle_error:
            cat = bd.oracle_error.split(":", 1)[0]
            error_categories[cat] += 1

        results.append({
            "rid": rid,
            "domain": rec["domain"],
            "n_hyp": bd.n_hyp,
            "n_conditions": bd.n_conditions,
            "witness": cw,
            "reward": bd.total,
            "reason": bd.reason,
            "parse_ok": bd.parse_ok,
            "elapsed_ms": bd.oracle_elapsed_ms,
            "oracle_error": bd.oracle_error,
        })

        status = "OK " if bd.total > 0 else "..."
        print(
            f"  [{i:3d}/{len(records)}] {status} "
            f"r={bd.total:+.2f} "
            f"ms={bd.oracle_elapsed_ms:5d} "
            f"reason={bd.reason:24s} {rid}"
        )

    wall = time.monotonic() - t_wall_start

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"  n records:           {len(records)}")
    print(f"  wall-clock total:    {wall:.2f}s")
    print(f"  parse_ok rate:       {parse_ok}/{len(records)} ({parse_ok/len(records):.0%})")
    print(f"  positive-reward:     {pos_reward}/{len(records)} ({pos_reward/len(records):.0%})")
    print()
    print("  elapsed_ms (per-record oracle execution):")
    print(f"    median:            {statistics.median(elapsed_list):.0f}")
    print(f"    p95:               {sorted(elapsed_list)[int(0.95*len(elapsed_list))-1]}")
    print(f"    max:               {max(elapsed_list)}")
    print(f"    mean:              {statistics.mean(elapsed_list):.0f}")
    print()
    print("  reason distribution:")
    for k, v in reasons.most_common():
        print(f"    {k:30s} {v:4d}")
    if error_categories:
        print()
        print("  oracle_error categories:")
        for k, v in error_categories.most_common():
            print(f"    {k:30s} {v:4d}")
    print()

    median_ms = statistics.median(elapsed_list)
    max_ms = max(elapsed_list)
    print("Gate checks:")
    print(
        f"  [{'PASS' if median_ms <= 200 else 'WARN'}] median <= 200 ms "
        f"(got {median_ms:.0f})"
    )
    print(
        f"  [{'PASS' if max_ms <= 8000 else 'FAIL'}] max <= 8000 ms "
        f"(got {max_ms})"
    )

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "n_records": len(records),
            "wall_clock_sec": wall,
            "parse_ok_rate": parse_ok / len(records),
            "positive_reward_rate": pos_reward / len(records),
            "elapsed_ms": {
                "median": statistics.median(elapsed_list),
                "p95": sorted(elapsed_list)[int(0.95 * len(elapsed_list)) - 1],
                "max": max(elapsed_list),
                "mean": statistics.mean(elapsed_list),
            },
            "reasons": dict(reasons),
            "oracle_error_categories": dict(error_categories),
            "results": results,
        }
        args.out.write_text(json.dumps(payload, indent=2, default=str))
        print(f"\nWrote JSON report -> {args.out}")


if __name__ == "__main__":
    main()
