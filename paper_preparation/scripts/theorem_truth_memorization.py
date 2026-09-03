"""Memorization-vs-generalization probe on the theorem_truth benchmark.

The 347-item theorem_truth set is partitioned into two subsets recorded in
the per_record JSONs via the `subset` field:

    extra_stratified : True theorems whose *mutated (false) versions* were
                       SEEN in the RLVR training corpus. If a model only
                       memorised the mutations as "things that need a
                       counterexample", it will under-perform here in
                       v2_counterexample style. Conversely, if it really
                       learned to recognise structure, performance here is
                       a lower bound on real generalisation.

    from_test_set    : True theorems the model never saw the mutations of.
                       This is the clean held-out subset.

For each (model, prompt_style, sampling_label) cell we report:
- N, Pass@1 with 95% bootstrap CI on each subset.
- The paired delta (extra_stratified - from_test_set) - *positive* delta means
  the model does better on seen-mutation theorems, which is the memorisation
  signal we want to bound.

Inputs
------
runs/eval/*__suite/per_cell/*__theorem_truth__*.json

Outputs
-------
paper_preparation/results/theorem_truth_subset.csv
paper_preparation/results/theorem_truth_subset.md

Usage
-----
    python -m paper_preparation.scripts.theorem_truth_memorization
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import math
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = REPO_ROOT / "paper_preparation" / "results"


def pass_at_k_unbiased(n: int, c: int, k: int) -> float:
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)


def bootstrap_pass_at_1(records: list[dict], n_bootstrap: int, alpha: float, rng) -> tuple[float, float, float]:
    if not records:
        return float("nan"), float("nan"), float("nan")
    vals = np.array([
        pass_at_k_unbiased(int(r["n_samples"]), int(r["n_correct"]), 1) for r in records
    ])
    n = len(vals)
    idx = rng.integers(0, n, size=(n_bootstrap, n))
    means = vals[idx].mean(axis=1)
    return float(vals.mean()), float(np.percentile(means, 100 * alpha / 2)), float(np.percentile(means, 100 * (1 - alpha / 2)))


def bootstrap_subset_delta(
    records: list[dict], n_bootstrap: int, alpha: float, rng,
) -> tuple[float, float, float, int, int]:
    """Bootstrap CI on (Pass@1 on extra_stratified) - (Pass@1 on from_test_set).

    Resamples *within each subset independently* (since the subsets are
    different theorems - not paired).
    """
    extra = [r for r in records if r.get("subset") == "extra_stratified"]
    base = [r for r in records if r.get("subset") == "from_test_set"]
    if not extra or not base:
        return float("nan"), float("nan"), float("nan"), len(extra), len(base)
    va = np.array([pass_at_k_unbiased(int(r["n_samples"]), int(r["n_correct"]), 1) for r in extra])
    vb = np.array([pass_at_k_unbiased(int(r["n_samples"]), int(r["n_correct"]), 1) for r in base])
    na, nb = len(va), len(vb)
    ia = rng.integers(0, na, size=(n_bootstrap, na))
    ib = rng.integers(0, nb, size=(n_bootstrap, nb))
    diffs = va[ia].mean(axis=1) - vb[ib].mean(axis=1)
    return (
        float(va.mean() - vb.mean()),
        float(np.percentile(diffs, 100 * alpha / 2)),
        float(np.percentile(diffs, 100 * (1 - alpha / 2))),
        na, nb,
    )


def load_theorem_truth_cells(suite_dirs: list[Path]) -> list[dict]:
    cells: dict[tuple, dict] = {}
    for suite_dir in sorted(suite_dirs):
        for path in sorted((suite_dir / "per_cell").glob("*__theorem_truth__*.json")):
            with open(path) as fh:
                data = json.load(fh)
            s = data["summary"]
            key = (s.get("model"), s.get("prompt_style"), s.get("sampling_label"))
            cells[key] = data
    return list(cells.values())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--suite-dirs", nargs="+", type=Path, default=None)
    ap.add_argument("--n-bootstrap", type=int, default=10000)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out-csv", type=Path, default=DEFAULT_OUT_DIR / "theorem_truth_subset.csv")
    ap.add_argument("--out-md", type=Path, default=DEFAULT_OUT_DIR / "theorem_truth_subset.md")
    args = ap.parse_args()

    if args.suite_dirs is None:
        args.suite_dirs = [Path(p) for p in sorted(
            glob.glob(str(REPO_ROOT / "runs" / "eval" / "*__suite"))
        )]

    cells = load_theorem_truth_cells(args.suite_dirs)
    if not cells:
        print("No theorem_truth cells found.")
        return 1

    rng = np.random.default_rng(args.seed)
    rows = []
    for cell in cells:
        s = cell["summary"]
        recs = cell["per_record"]
        extra = [r for r in recs if r.get("subset") == "extra_stratified"]
        base = [r for r in recs if r.get("subset") == "from_test_set"]
        p_extra, lo_extra, hi_extra = bootstrap_pass_at_1(extra, args.n_bootstrap, args.alpha, rng)
        p_base, lo_base, hi_base = bootstrap_pass_at_1(base, args.n_bootstrap, args.alpha, rng)
        d_point, d_lo, d_hi, na, nb = bootstrap_subset_delta(recs, args.n_bootstrap, args.alpha, rng)
        rows.append({
            "model": s.get("model"),
            "model_type": s.get("model_type"),
            "prompt_style": s.get("prompt_style"),
            "sampling_label": s.get("sampling_label"),
            "n_extra_stratified": na,
            "p1_extra_stratified": round(p_extra, 4),
            "ci_lo_extra": round(lo_extra, 4),
            "ci_hi_extra": round(hi_extra, 4),
            "n_from_test_set": nb,
            "p1_from_test_set": round(p_base, 4),
            "ci_lo_test": round(lo_base, 4),
            "ci_hi_test": round(hi_base, 4),
            "delta_extra_minus_test": round(d_point, 4),
            "delta_ci_lo": round(d_lo, 4),
            "delta_ci_hi": round(d_hi, 4),
        })

    rows.sort(key=lambda r: (r["prompt_style"], r["sampling_label"], r["model"]))

    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_csv, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {args.out_csv} ({len(rows)} cells)")

    md = [
        "# Theorem-truth memorisation probe",
        "",
        "**Subset definitions:**",
        "- `extra_stratified`: TRUE theorems whose *mutated* versions WERE seen during RLVR training.",
        "- `from_test_set`: TRUE theorems whose mutations were NEVER seen.",
        "",
        "A positive delta = the model does better on theorems with seen mutations than on unseen ones.",
        "An overlap of the delta CI with 0 means no detectable memorisation in this metric.",
        "",
    ]
    for style in ("truth_classify", "v2_counterexample"):
        for samp in ("greedy", "sampled"):
            bucket = [r for r in rows if r["prompt_style"] == style and r["sampling_label"] == samp]
            if not bucket:
                continue
            md.append(f"## {style} / {samp}\n")
            md.append("| Model | Pass@1 extra_strat (CI) | Pass@1 from_test (CI) | Δ (extra - test) | 95% CI on Δ |")
            md.append("|---|---:|---:|---:|---:|")
            for r in bucket:
                md.append(
                    f"| {r['model']} "
                    f"| {r['p1_extra_stratified']:.3f} [{r['ci_lo_extra']:.3f}, {r['ci_hi_extra']:.3f}] "
                    f"| {r['p1_from_test_set']:.3f} [{r['ci_lo_test']:.3f}, {r['ci_hi_test']:.3f}] "
                    f"| {r['delta_extra_minus_test']:+.3f} "
                    f"| [{r['delta_ci_lo']:+.3f}, {r['delta_ci_hi']:+.3f}] |"
                )
            md.append("")

    args.out_md.write_text("\n".join(md))
    print(f"Wrote {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
