"""Build a theorem-truth eval set from input_theorems + test-set IDs.

Creates a JSONL of *true* theorems with two subsets:
1) Theorems whose IDs appear in the v2 test set (typically ~200).
2) An additional stratified sample across domains (default 150), drawn
   from the remaining theorems.

Each JSONL record preserves as much metadata as possible.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _format_record(rec: dict[str, Any], *, subset: str, in_test_set: bool) -> dict[str, Any]:
    return {
        "theorem_id": rec.get("id"),
        "theorem_name": rec.get("name"),
        "domain": rec.get("domain"),
        "topic": rec.get("topic"),
        "original_full_statement": rec.get("original_full_statement"),
        "hypotheses": rec.get("hypotheses") or [],
        "remaining_hypotheses": rec.get("hypotheses") or [],
        "conclusion": rec.get("conclusion"),
        "subset": subset,
        "in_test_set": bool(in_test_set),
        "source": "input_theorems",
    }


def build_dataset(
    *,
    input_theorems_path: Path,
    test_set_path: Path,
    output_path: Path,
    seed: int = 42,
    extra_target: int = 150,
    stats_out: Path | None = None,
) -> dict[str, Any]:
    input_theorems = _load_json(input_theorems_path)
    test_set = _load_jsonl(test_set_path)

    theorem_by_id = {t.get("id"): t for t in input_theorems if t.get("id")}

    # 1) From test set IDs
    test_ids = []
    seen = set()
    for rec in test_set:
        tid = rec.get("theorem_id")
        if tid and tid not in seen:
            test_ids.append(tid)
            seen.add(tid)

    from_test: list[dict[str, Any]] = []
    missing_test_ids: list[str] = []
    for tid in test_ids:
        base = theorem_by_id.get(tid)
        if not base:
            missing_test_ids.append(tid)
            continue
        from_test.append(_format_record(base, subset="from_test_set", in_test_set=True))

    # 2) Stratified extra sample
    remaining = [t for t in input_theorems if t.get("id") not in seen]
    by_domain: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for t in remaining:
        by_domain[t.get("domain") or "Unknown"].append(t)

    rng = random.Random(seed)
    domains = sorted(by_domain)
    per_domain = extra_target // max(1, len(domains))
    extra: list[dict[str, Any]] = []
    per_domain_counts: dict[str, int] = {}

    for domain in domains:
        pool = list(by_domain[domain])
        rng.shuffle(pool)
        take = min(per_domain, len(pool))
        per_domain_counts[domain] = take
        for t in pool[:take]:
            extra.append(_format_record(t, subset="extra_stratified", in_test_set=False))

    all_records = from_test + extra
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        for rec in all_records:
            fh.write(json.dumps(rec, ensure_ascii=True) + "\n")

    stats = {
        "input_theorems": str(input_theorems_path),
        "test_set": str(test_set_path),
        "output": str(output_path),
        "seed": seed,
        "extra_target": extra_target,
        "n_from_test_set": len(from_test),
        "n_extra": len(extra),
        "n_total": len(all_records),
        "per_domain_extra": per_domain_counts,
        "missing_test_ids": missing_test_ids,
    }
    if stats_out:
        stats_out.parent.mkdir(parents=True, exist_ok=True)
        with open(stats_out, "w", encoding="utf-8") as fh:
            json.dump(stats, fh, indent=2)
    return stats


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Build theorem-truth eval set from input_theorems + test-set IDs."
    )
    p.add_argument(
        "--input-theorems",
        default="data/input_theorems.json",
        help="Path to input_theorems.json",
    )
    p.add_argument(
        "--test-set",
        default="data/test_set_v2.jsonl",
        help="Path to test_set_v2.jsonl",
    )
    p.add_argument(
        "--output",
        default="data/theorem_truth_eval.jsonl",
        help="Output JSONL path",
    )
    p.add_argument("--seed", type=int, default=42, help="Random seed")
    p.add_argument(
        "--extra-target",
        type=int,
        default=150,
        help="Target number of extra stratified theorems",
    )
    p.add_argument(
        "--stats-out",
        default=None,
        help="Optional JSON stats output path",
    )
    return p


def main() -> None:
    args = _build_parser().parse_args()
    stats = build_dataset(
        input_theorems_path=Path(args.input_theorems),
        test_set_path=Path(args.test_set),
        output_path=Path(args.output),
        seed=args.seed,
        extra_target=args.extra_target,
        stats_out=Path(args.stats_out) if args.stats_out else None,
    )
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
