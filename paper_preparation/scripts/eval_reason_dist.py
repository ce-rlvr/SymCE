"""Eval-time reason distributions on the counterexample benchmark.

The counterexample per_cell JSONs carry per-sample `reason` labels emitted by
the oracle reward function (success / neg_q_only / hyp_only / partial /
no_tag / oracle_parse_error / none_on_false / etc.). This aggregates them
across all models so we can show:

    "RLVR-dense fails mostly with hyp_only (model satisfies hypotheses but
    fails to negate Q), while RLVR-sparse fails mostly with no_tag or
    none_on_false."

Inputs
------
- runs/eval/*__suite/per_cell/*__counterexample__*.json
  Each per_record has up to N samples with `reason`.

Outputs
-------
- paper_preparation/results/eval_reason_distribution.csv
- paper_preparation/results/eval_reason_distribution.md

Usage
-----
    python -m paper_preparation.scripts.eval_reason_dist
"""

from __future__ import annotations

import argparse
import csv
import glob
import gzip
import json
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = REPO_ROOT / "paper_preparation" / "results"

REASONS = (
    "success",
    "neg_q_only",
    "hyp_only",
    "partial",
    "no_tag",
    "oracle_parse_error",
    "none_on_false",
    "condition_length_mismatch",
    "invalid_neg_q_index",
    "reward_exception",
)


def load_counterexample_cells(suite_dirs: list[Path]) -> list[dict]:
    """Return the latest per_cell JSON per (model, prompt_style, sampling_label)."""
    cells: dict[tuple, dict] = {}
    for suite_dir in sorted(suite_dirs):
        pc = suite_dir / "per_cell"
        for path in sorted(list(pc.glob("*__counterexample__*.json"))
                            + list(pc.glob("*__counterexample__*.json.gz"))):
            opener = gzip.open if path.suffix == ".gz" else open
            with opener(path, "rt") as fh:
                data = json.load(fh)
            summary = data.get("summary", {})
            if summary.get("benchmark") != "counterexample":
                continue
            key = (
                summary.get("model"),
                summary.get("prompt_style"),
                summary.get("sampling_label"),
            )
            cells[key] = data
    return list(cells.values())


def aggregate_reasons(per_record: list[dict]) -> tuple[int, Counter]:
    counter: Counter = Counter()
    total = 0
    for rec in per_record:
        for sample in rec.get("samples", []):
            r = sample.get("reason") or "unknown"
            counter[r] += 1
            total += 1
    return total, counter


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--suite-dirs", nargs="+", type=Path, default=None)
    ap.add_argument("--out-csv", type=Path, default=DEFAULT_OUT_DIR / "eval_reason_distribution.csv")
    ap.add_argument("--out-md", type=Path, default=DEFAULT_OUT_DIR / "eval_reason_distribution.md")
    args = ap.parse_args()

    if args.suite_dirs is None:
        args.suite_dirs = [Path(p) for p in sorted(
            glob.glob(str(REPO_ROOT / "runs" / "eval" / "*__suite"))
        )]

    cells = load_counterexample_cells(args.suite_dirs)
    if not cells:
        print("No counterexample cells found.")
        return 1

    rows = []
    for cell in cells:
        summary = cell["summary"]
        total, counter = aggregate_reasons(cell["per_record"])
        row = {
            "model": summary.get("model"),
            "model_type": summary.get("model_type"),
            "prompt_style": summary.get("prompt_style"),
            "sampling_label": summary.get("sampling_label"),
            "n_problems": summary.get("n_problems"),
            "n_samples": summary.get("n_samples"),
            "n_total_rollouts": total,
        }
        for reason in REASONS:
            row[f"n_{reason}"] = counter.get(reason, 0)
            row[f"rate_{reason}"] = round(counter.get(reason, 0) / total, 6) if total else 0.0
        # Anything else (defensive - should be empty)
        unknown = sum(v for k, v in counter.items() if k not in REASONS)
        row["n_other"] = unknown
        rows.append(row)

    rows.sort(key=lambda r: (r["model"], r["sampling_label"]))

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_csv, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {args.out_csv} ({len(rows)} cells)")

    # Markdown: one table for greedy, one for sampled, only the interesting columns
    def write_md_section(label: str, sampling: str) -> list[str]:
        lines = [f"## counterexample / {sampling}\n"]
        lines.append("| Model | N | Success | neg_q_only | hyp_only | partial | no_tag | parse_err | none_on_false |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        for r in rows:
            if r["sampling_label"] != sampling:
                continue
            lines.append(
                f"| {r['model']} | {r['n_total_rollouts']} "
                f"| {r['rate_success']:.3f} "
                f"| {r['rate_neg_q_only']:.3f} "
                f"| {r['rate_hyp_only']:.3f} "
                f"| {r['rate_partial']:.3f} "
                f"| {r['rate_no_tag']:.3f} "
                f"| {r['rate_oracle_parse_error']:.3f} "
                f"| {r['rate_none_on_false']:.3f} |"
            )
        lines.append("")
        return lines

    md = ["# Eval reason distribution - counterexample benchmark", "",
          "Rates are fractions of total samples (n_problems x n_samples).",
          "`hyp_only` is the load-bearing dense-reward pathology - model satisfies remaining hypotheses without negating Q.",
          ""]
    md.extend(write_md_section("greedy", "greedy"))
    md.extend(write_md_section("sampled", "sampled"))
    args.out_md.write_text("\n".join(md))
    print(f"Wrote {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
