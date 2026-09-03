"""Bootstrap 95% confidence intervals over eval per_cell JSONs.

Inputs
------
- One or more eval suite directories under runs/eval/, named
  <timestamp>__<suite_name>__suite. With no --suite-dirs argument every such
  directory is read.
- Each suite has a per_cell/ folder holding one JSON or JSON.gz per cell; this
  script ingests all of them.

What it computes
----------------
For every cell (model x benchmark x prompt_style x sampling_label):

    Pass@1     : point + (lo, hi)
    Pass@k     : for sampled cells, k in summary.pass_at_k.keys() (3/5/8 etc.)
    By-domain Pass@1
    theorem_truth subset_metrics (extra_stratified vs from_test_set)
    Optional pairwise deltas (default: vs qwen3-base; configurable)

Bootstrap is over *problem IDs* (the unit of independence). For Pass@k with
multiple samples per problem, the per-problem `n_correct / n_samples` and the
unbiased pass@k estimator (Chen et al. 2021) are reused so the CI reflects
*test-set* variance, not sampling variance.

Outputs
-------
- paper_preparation/results/bootstrap_cis.csv   (long-format table)
- paper_preparation/results/bootstrap_cis.md    (human-readable summary)
- paper_preparation/results/bootstrap_deltas.csv   (pairwise Pass@1 deltas)

Usage
-----
    # default: scan every runs/eval/*__suite/per_cell/*.json
    python -m paper_preparation.scripts.bootstrap_cis

    # restrict to two suite dirs
    python -m paper_preparation.scripts.bootstrap_cis \\
        --suite-dirs runs/eval/20260522-044136__symce_full__suite \\
                     runs/eval/20260524-003142__symce_full__suite

    # custom comparator and bootstrap depth
    python -m paper_preparation.scripts.bootstrap_cis \\
        --n-bootstrap 20000 --baseline qwen3-base

Note: outputs *one row per cell* - if two suite runs scored the same cell
(e.g. qwen-rlvr CE greedy was run twice), the *later* suite directory wins,
matching the convention in all_results_summary.md.
"""

from __future__ import annotations

import argparse
import csv
import glob
import gzip
import json
import math
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = REPO_ROOT / "paper_preparation" / "results"


# ---------------------------------------------------------------------------
# Pass@k (Chen et al. 2021, OpenAI HumanEval) -- unbiased estimator
# ---------------------------------------------------------------------------

def pass_at_k_unbiased(n: int, c: int, k: int) -> float:
    """Probability that at least one of k randomly chosen samples is correct."""
    if n - c < k:
        return 1.0
    # 1 - C(n-c, k) / C(n, k)
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)


def cell_pass_at_k(records: list[dict], k: int) -> float:
    """Cell-level Pass@k = mean over problems of unbiased Pass@k."""
    if not records:
        return float("nan")
    values = []
    for r in records:
        n = int(r["n_samples"])
        c = int(r["n_correct"])
        if k > n:
            # cell didn't generate enough samples for this k
            return float("nan")
        values.append(pass_at_k_unbiased(n, c, k))
    return float(np.mean(values))


# ---------------------------------------------------------------------------
# Bootstrap helpers
# ---------------------------------------------------------------------------

def bootstrap_ci(
    values: np.ndarray,
    n_bootstrap: int,
    alpha: float,
    rng: np.random.Generator,
) -> tuple[float, float, float]:
    """Return (mean, lo, hi) where (lo, hi) is the percentile CI."""
    if values.size == 0:
        return float("nan"), float("nan"), float("nan")
    n = values.size
    idx = rng.integers(0, n, size=(n_bootstrap, n))
    means = values[idx].mean(axis=1)
    lo = float(np.percentile(means, 100 * alpha / 2))
    hi = float(np.percentile(means, 100 * (1 - alpha / 2)))
    return float(values.mean()), lo, hi


def bootstrap_pass_at_k(
    records: list[dict],
    k: int,
    n_bootstrap: int,
    alpha: float,
    rng: np.random.Generator,
) -> tuple[float, float, float]:
    """Bootstrap CI for Pass@k by resampling problems with replacement."""
    if not records:
        return float("nan"), float("nan"), float("nan")
    n = len(records)
    ns = np.array([int(r["n_samples"]) for r in records])
    cs = np.array([int(r["n_correct"]) for r in records])
    if (ns < k).any():
        return float("nan"), float("nan"), float("nan")
    # Pre-compute per-problem pass@k
    per_prob = np.array([pass_at_k_unbiased(int(nn), int(cc), k) for nn, cc in zip(ns, cs)])
    idx = rng.integers(0, n, size=(n_bootstrap, n))
    means = per_prob[idx].mean(axis=1)
    point = float(per_prob.mean())
    lo = float(np.percentile(means, 100 * alpha / 2))
    hi = float(np.percentile(means, 100 * (1 - alpha / 2)))
    return point, lo, hi


# ---------------------------------------------------------------------------
# Cell loading
# ---------------------------------------------------------------------------

@dataclass
class Cell:
    suite_dir: str
    cell_id: str
    model: str
    model_id: str
    model_type: str
    benchmark: str
    prompt_style: str
    sampling_label: str
    n_samples: int
    n_problems: int
    records: list[dict]
    summary: dict


def load_cells(suite_dirs: list[Path]) -> list[Cell]:
    cells: dict[tuple, Cell] = {}
    for suite_dir in suite_dirs:
        per_cell_dir = suite_dir / "per_cell"
        if not per_cell_dir.is_dir():
            continue
        for path in sorted(list(per_cell_dir.glob("*.json"))
                            + list(per_cell_dir.glob("*.json.gz"))):
            opener = gzip.open if path.suffix == ".gz" else open
            with opener(path, "rt") as fh:
                data = json.load(fh)
            summary = data.get("summary", {})
            records = data.get("per_record", [])
            cell = Cell(
                suite_dir=str(suite_dir.name),
                cell_id=summary.get("cell_id", path.stem),
                model=summary.get("model", ""),
                model_id=summary.get("model_id", ""),
                model_type=summary.get("model_type", "unknown"),
                benchmark=summary.get("benchmark", ""),
                prompt_style=summary.get("prompt_style", ""),
                sampling_label=summary.get("sampling_label", ""),
                n_samples=int(summary.get("n_samples", 1)),
                n_problems=int(summary.get("n_problems", len(records))),
                records=records,
                summary=summary,
            )
            # Keyed by training seed as well, so a model evaluated at several
            # seeds contributes one row per seed instead of silently collapsing
            # to whichever suite happened to be read last.
            seed = re.search(r"seed(\d+)", cell.model_id or "")
            key = (cell.model, seed.group(1) if seed else "",
                   cell.benchmark, cell.prompt_style, cell.sampling_label)
            # Last writer wins within a (model, seed) cell.
            cells[key] = cell
    return list(cells.values())


# ---------------------------------------------------------------------------
# Metric extraction per benchmark
# ---------------------------------------------------------------------------

def record_correct_array(records: list[dict]) -> np.ndarray:
    """For Pass@1 / correct rate. Treats each record as 0/1 (greedy or any_correct)."""
    return np.array([1.0 if r.get("any_correct") else 0.0 for r in records])


def record_conclusion_pass_array(records: list[dict]) -> np.ndarray:
    return np.array([1.0 if r.get("conclusion_pass") else 0.0 for r in records])


def subset_records(records: list[dict], subset_name: str) -> list[dict]:
    return [r for r in records if r.get("subset") == subset_name]


def domain_records(records: list[dict], domain: str) -> list[dict]:
    return [r for r in records if r.get("domain") == domain]


# ---------------------------------------------------------------------------
# CI computation per cell
# ---------------------------------------------------------------------------

def compute_cell_rows(
    cell: Cell,
    n_bootstrap: int,
    alpha: float,
    rng: np.random.Generator,
) -> list[dict]:
    """Emit one row per (cell, metric, slice)."""
    rows: list[dict] = []

    def emit(metric: str, slice_: str, n: int, point: float, lo: float, hi: float):
        rows.append({
            "suite_dir": cell.suite_dir,
            "model": cell.model,
            "model_id": cell.model_id,
            # Training seed, parsed from the adapter path. Empty for the base
            # model and every external comparator, which have no training seed.
            "seed": (re.search(r"seed(\d+)", cell.model_id or "").group(1)
                     if re.search(r"seed(\d+)", cell.model_id or "") else ""),
            "model_type": cell.model_type,
            "benchmark": cell.benchmark,
            "prompt_style": cell.prompt_style,
            "sampling_label": cell.sampling_label,
            "n_samples": cell.n_samples,
            "metric": metric,
            "slice": slice_,
            "n": n,
            "point": round(point, 6) if not math.isnan(point) else "",
            "ci_lo": round(lo, 6) if not math.isnan(lo) else "",
            "ci_hi": round(hi, 6) if not math.isnan(hi) else "",
        })

    records = cell.records

    # ---- Pass@1 (overall) ----
    point, lo, hi = bootstrap_pass_at_k(records, 1, n_bootstrap, alpha, rng)
    emit("pass_at_1", "overall", len(records), point, lo, hi)

    # ---- Pass@k for sampled cells ----
    if cell.sampling_label == "sampled":
        for k in (3, 5, 8):
            if cell.n_samples >= k:
                point, lo, hi = bootstrap_pass_at_k(records, k, n_bootstrap, alpha, rng)
                emit(f"pass_at_{k}", "overall", len(records), point, lo, hi)

    # ---- Conclusion-pass rate (counterexample benchmark only) ----
    if any("conclusion_pass" in r for r in records):
        vals = record_conclusion_pass_array(records)
        point, lo, hi = bootstrap_ci(vals, n_bootstrap, alpha, rng)
        emit("conclusion_pass_rate", "overall", len(records), point, lo, hi)

    # ---- Per-domain Pass@1 ----
    domains = sorted({r.get("domain") for r in records if r.get("domain")})
    for dom in domains:
        sub = domain_records(records, dom)
        if not sub:
            continue
        p, l, h = bootstrap_pass_at_k(sub, 1, n_bootstrap, alpha, rng)
        emit("pass_at_1", f"domain:{dom}", len(sub), p, l, h)

    # ---- theorem_truth subset_metrics (memorization probe) ----
    if any("subset" in r for r in records):
        for subset in ("extra_stratified", "from_test_set"):
            sub = subset_records(records, subset)
            if not sub:
                continue
            p, l, h = bootstrap_pass_at_k(sub, 1, n_bootstrap, alpha, rng)
            emit("pass_at_1", f"subset:{subset}", len(sub), p, l, h)
            # Pass@k for theorem_truth sampled
            if cell.sampling_label == "sampled":
                for k in (3, 5, 8):
                    if cell.n_samples >= k:
                        p, l, h = bootstrap_pass_at_k(sub, k, n_bootstrap, alpha, rng)
                        emit(f"pass_at_{k}", f"subset:{subset}", len(sub), p, l, h)

    return rows


# ---------------------------------------------------------------------------
# Pairwise deltas (model - baseline) - paired by problem_id
# ---------------------------------------------------------------------------

def paired_delta_pass_at_1(
    cell_a: Cell, cell_b: Cell, n_bootstrap: int, alpha: float, rng: np.random.Generator,
) -> Optional[dict]:
    """Bootstrap CI on (cell_a Pass@1 - cell_b Pass@1), paired by problem_id."""
    a = {r["problem_id"]: r for r in cell_a.records}
    b = {r["problem_id"]: r for r in cell_b.records}
    common = sorted(set(a) & set(b))
    if not common:
        return None
    da = np.array([pass_at_k_unbiased(int(a[p]["n_samples"]), int(a[p]["n_correct"]), 1) for p in common])
    db = np.array([pass_at_k_unbiased(int(b[p]["n_samples"]), int(b[p]["n_correct"]), 1) for p in common])
    diffs = da - db
    n = len(common)
    idx = rng.integers(0, n, size=(n_bootstrap, n))
    means = diffs[idx].mean(axis=1)
    return {
        "model_a": cell_a.model,
        "model_b": cell_b.model,
        "benchmark": cell_a.benchmark,
        "prompt_style": cell_a.prompt_style,
        "sampling_label": cell_a.sampling_label,
        "n_common_problems": n,
        "delta_point": round(float(diffs.mean()), 6),
        "delta_ci_lo": round(float(np.percentile(means, 100 * alpha / 2)), 6),
        "delta_ci_hi": round(float(np.percentile(means, 100 * (1 - alpha / 2))), 6),
    }


# ---------------------------------------------------------------------------
# Markdown writer
# ---------------------------------------------------------------------------

def write_markdown(rows: list[dict], out_path: Path) -> None:
    by_cell: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        key = (r["benchmark"], r["prompt_style"], r["sampling_label"], r["model"])
        by_cell[key].append(r)

    lines: list[str] = ["# Bootstrap 95% CIs", ""]
    last_bench = None
    for (bench, style, samp, model), bucket in sorted(by_cell.items()):
        if bench != last_bench:
            lines.append(f"\n## {bench}\n")
            last_bench = bench
        lines.append(f"### {model} - {style} / {samp}\n")
        lines.append("| Metric | Slice | N | Point | CI lo | CI hi |")
        lines.append("|---|---|---:|---:|---:|---:|")
        for r in bucket:
            lines.append(f"| {r['metric']} | {r['slice']} | {r['n']} | {r['point']} | {r['ci_lo']} | {r['ci_hi']} |")
        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--suite-dirs",
        nargs="+",
        type=Path,
        default=None,
        help="Suite directories under runs/eval/. Default: all *__suite",
    )
    ap.add_argument("--n-bootstrap", type=int, default=10000)
    ap.add_argument("--alpha", type=float, default=0.05, help="CI = 1 - alpha. Default: 0.05 (95%)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out-csv", type=Path, default=DEFAULT_OUT_DIR / "bootstrap_cis.csv")
    ap.add_argument("--out-md", type=Path, default=DEFAULT_OUT_DIR / "bootstrap_cis.md")
    ap.add_argument(
        "--out-deltas-csv",
        type=Path,
        default=DEFAULT_OUT_DIR / "bootstrap_deltas.csv",
    )
    ap.add_argument(
        "--baseline",
        default="qwen3-base",
        help="Model name used as the paired-delta baseline. Set empty to skip deltas.",
    )
    args = ap.parse_args()

    if args.suite_dirs is None:
        args.suite_dirs = [Path(p) for p in sorted(
            glob.glob(str(REPO_ROOT / "runs" / "eval" / "*__suite"))
        )]
    if not args.suite_dirs:
        print("No suite directories found.", file=sys.stderr)
        return 1

    print(f"Loading {len(args.suite_dirs)} suite dir(s)...", file=sys.stderr)
    cells = load_cells([Path(p) for p in args.suite_dirs])
    print(f"Loaded {len(cells)} unique cells.", file=sys.stderr)

    rng = np.random.default_rng(args.seed)
    rows: list[dict] = []
    for cell in cells:
        rows.extend(compute_cell_rows(cell, args.n_bootstrap, args.alpha, rng))

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_csv, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {args.out_csv} ({len(rows)} rows)")

    write_markdown(rows, args.out_md)
    print(f"Wrote {args.out_md}")

    # Paired deltas against baseline (counterexample + theorem_truth)
    if args.baseline:
        baseline_cells = {
            (c.benchmark, c.prompt_style, c.sampling_label): c
            for c in cells if c.model == args.baseline
        }
        delta_rows: list[dict] = []
        for cell in cells:
            if cell.model == args.baseline:
                continue
            base = baseline_cells.get((cell.benchmark, cell.prompt_style, cell.sampling_label))
            if base is None:
                continue
            d = paired_delta_pass_at_1(cell, base, args.n_bootstrap, args.alpha, rng)
            if d is not None:
                delta_rows.append(d)
        if delta_rows:
            with open(args.out_deltas_csv, "w", newline="") as fh:
                writer = csv.DictWriter(fh, fieldnames=list(delta_rows[0].keys()))
                writer.writeheader()
                writer.writerows(delta_rows)
            print(f"Wrote {args.out_deltas_csv} ({len(delta_rows)} pairwise deltas vs {args.baseline})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
