"""Paper figures — single matplotlib script.

Produces PDFs in paper_preparation/plots/ from the CSVs we already have. Each
plot is gated by a flag; default `--all` regenerates everything.

Plot inventory
--------------
    --reason-stack       Figure: reason-taxonomy stacked bar (SFT / dense / sparse / base).
    --truth-bar          Figure: theorem-truth Pass@1, two prompt styles, base/SFT/dense/sparse.
    --training-curves    Figure: RLVR reward / KL / parse_ok over steps, dense + sparse.
    --domain-bar         Figure: per-domain Pass@1 on counterexample with 95% CIs.
    --baselines-bar      Figure: counterexample Pass@1, our 4B vs 7B baselines vs frontier band.
    --ood-bar            Figure: OOD transfer (GSM8K / MATH / MMLU-CM) under standard_cot.
    --all                All of the above.

Style: matplotlib only, no seaborn dependence. Each plot writes a PDF and a PNG.

Usage
-----
    python -m paper_preparation.scripts.make_plots --all
    python -m paper_preparation.scripts.make_plots --reason-stack --truth-bar
    python -m paper_preparation.scripts.make_plots --all --out-dir paper_preparation/plots --dpi 200
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_DIR = REPO_ROOT / "paper_preparation" / "results"
SUMMARY_DIR = REPO_ROOT / "results_summary"
DEFAULT_PLOTS_DIR = REPO_ROOT / "paper_preparation" / "plots"

# Colour palette (kept conservative for greyscale-printable)
COLOR_BASE   = "#999999"
COLOR_SFT    = "#d95f02"
COLOR_DENSE  = "#1b9e77"
COLOR_SPARSE = "#7570b3"

MODEL_LABELS = {
    "qwen3-base":       ("Qwen3-4B base",     COLOR_BASE),
    "qwen-sft":         ("+ SFT",             COLOR_SFT),
    "qwen-rlvr":        ("+ RLVR (dense)",    COLOR_DENSE),
    "qwen-rlvr-sparse": ("+ RLVR (sparse)",   COLOR_SPARSE),
}
MODEL_ORDER = ["qwen3-base", "qwen-sft", "qwen-rlvr", "qwen-rlvr-sparse"]


# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------

REFERENCE_SEED = "42"


def at_reference_seed(rows: list[dict]) -> list[dict]:
    """Keep rows from the reference seed, plus rows with no training seed.

    The corpus holds one cell per (model, seed); without this filter a model
    trained at several seeds would be represented by whichever row happened to
    be read last, which need not be the seed the paper's tables report.
    """
    return [r for r in rows if r.get("seed", "") in ("", REFERENCE_SEED)]


def read_csv(path: Path) -> list[dict]:
    with open(path) as fh:
        return list(csv.DictReader(fh))


def _save(fig, name: str, out_dir: Path, dpi: int) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf = out_dir / f"{name}.pdf"
    png = out_dir / f"{name}.png"
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(png, bbox_inches="tight", dpi=dpi)
    print(f"  wrote {pdf}")
    print(f"  wrote {png}")
    plt.close(fig)


# ---------------------------------------------------------------------------
# Plot 1: reason-taxonomy stacked bar (counterexample / greedy)
# ---------------------------------------------------------------------------

REASONS_ORDERED = [
    ("success",            "Success",          "#1b9e77"),
    ("neg_q_only",         "¬Q only",          "#66c2a5"),
    ("none_on_false",      "Abstain (NONE)",   "#3288bd"),  # the abstention we want
    ("hyp_only",           "Hyp-only (asserts Q true)", "#fc8d59"),
    ("partial",            "Partial",          "#fdae61"),
    ("oracle_parse_error", "Parse error",      "#d53e4f"),
    ("no_tag",             "No tag",           "#999999"),
]


def plot_reason_stack(out_dir: Path, dpi: int) -> None:
    print("[plot] reason stack")
    rows = read_csv(RESULTS_DIR / "eval_reason_distribution.csv")
    by_model = {r["model"]: r for r in rows if r["sampling_label"] == "greedy"}
    models = [m for m in MODEL_ORDER if m in by_model]
    labels = [MODEL_LABELS[m][0] for m in models]
    x = np.arange(len(models))

    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    bottoms = np.zeros(len(models))
    for key, label, color in REASONS_ORDERED:
        rates = np.array([float(by_model[m][f"rate_{key}"]) for m in models])
        ax.bar(x, rates, bottom=bottoms, width=0.62, label=label, color=color, edgecolor="white", linewidth=0.5)
        bottoms += rates

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=0)
    ax.set_ylabel("Fraction of greedy rollouts")
    ax.set_title("Counterexample benchmark — per-sample reason distribution (greedy, n=201)")
    ax.set_ylim(0, 1.0)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=8)
    _save(fig, "fig_reason_stack", out_dir, dpi)


# ---------------------------------------------------------------------------
# Plot 2: theorem-truth bar (two prompt styles, four models)
# ---------------------------------------------------------------------------

def plot_truth_bar(out_dir: Path, dpi: int) -> None:
    print("[plot] theorem-truth bar")
    rows = at_reference_seed(read_csv(RESULTS_DIR / "bootstrap_cis.csv"))
    # Use the from_test_set subset, greedy only, pass_at_1
    keep = [r for r in rows
            if r["benchmark"] == "theorem_truth"
            and r["sampling_label"] == "greedy"
            and r["metric"] == "pass_at_1"
            and r["slice"] == "subset:from_test_set"]
    table = {(r["model"], r["prompt_style"]): r for r in keep}

    styles = [("v2_counterexample", "v2_counterexample style\n(emit [COUNTEREXAMPLE: NONE])"),
              ("truth_classify",    "truth_classify style\n(emit explicit TRUE)")]
    models = MODEL_ORDER
    width = 0.18

    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    x = np.arange(len(styles))

    for i, m in enumerate(models):
        points = []
        err_lo = []
        err_hi = []
        for style_key, _ in styles:
            r = table.get((m, style_key))
            if r is None:
                points.append(0.0); err_lo.append(0.0); err_hi.append(0.0)
                continue
            p = float(r["point"]); lo = float(r["ci_lo"]); hi = float(r["ci_hi"])
            points.append(p)
            err_lo.append(p - lo)
            err_hi.append(hi - p)
        offset = (i - (len(models) - 1) / 2) * width
        label, color = MODEL_LABELS[m]
        ax.bar(x + offset, points, width=width,
               yerr=[err_lo, err_hi], capsize=2.0,
               label=label, color=color, edgecolor="white", linewidth=0.4)
        for xi, p in zip(x + offset, points):
            ax.text(xi, p + 0.015, f"{p:.2f}", ha="center", va="bottom", fontsize=7)

    ax.set_xticks(x)
    ax.set_xticklabels([s[1] for s in styles])
    ax.set_ylabel("Pass@1 (TRUE recognised, n=197)")
    ax.set_ylim(0, 1.0)
    ax.set_title("Theorem-truth probe — the SFT imitation trap and the sparse-RL recovery")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.10), ncol=4, frameon=False, fontsize=8)
    _save(fig, "fig_theorem_truth", out_dir, dpi)


# ---------------------------------------------------------------------------
# Plot 3: RLVR training curves
# ---------------------------------------------------------------------------

def _load_train_log(name: str) -> dict:
    """Return columns as numpy arrays, ignoring trailing summary row."""
    path = SUMMARY_DIR / name / "train_log.csv"
    with open(path) as fh:
        reader = csv.DictReader(fh)
        cols = {k: [] for k in reader.fieldnames}
        for row in reader:
            for k, v in row.items():
                cols[k].append(v)
    out = {}
    for k, vs in cols.items():
        arr = []
        for v in vs:
            try:
                arr.append(float(v))
            except (TypeError, ValueError):
                arr.append(np.nan)
        out[k] = np.array(arr)
    return out


def plot_training_curves(out_dir: Path, dpi: int) -> None:
    print("[plot] training curves")
    dense = _load_train_log("rlvr_dense")
    sparse = _load_train_log("rlvr_sparse")

    fig, axes = plt.subplots(1, 3, figsize=(9.5, 2.9), sharex=True)

    for ax, key, title, ylabel in [
        (axes[0], "reward",    "Mean reward",    "reward"),
        (axes[1], "kl",        "KL to SFT ref",  "KL"),
        (axes[2], "loss",      "Policy loss",    "loss"),
    ]:
        for name, log, color in [
            ("RLVR-dense",  dense,  COLOR_DENSE),
            ("RLVR-sparse", sparse, COLOR_SPARSE),
        ]:
            step = log["step"]
            y = log[key]
            mask = ~np.isnan(step) & ~np.isnan(y)
            ax.plot(step[mask], y[mask], "-", color=color, lw=1.5, label=name)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("Step")
        ax.set_ylabel(ylabel)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(alpha=0.2)

    axes[0].axhline(0, color="grey", lw=0.6, ls=":")
    axes[0].legend(loc="lower right", frameon=False, fontsize=8)
    fig.suptitle("RLVR training stability — 4 epochs over 3506 prompts (G=4, T=1.0)",
                 fontsize=11, y=1.04)
    _save(fig, "fig_training_curves", out_dir, dpi)


# ---------------------------------------------------------------------------
# Plot 4: per-domain Pass@1 with CIs (counterexample / greedy)
# ---------------------------------------------------------------------------

DOMAINS = ["GroupTheory", "RingTheory", "NumberTheory", "LinearAlgebra", "RealAnalysis", "FieldTheory"]


def plot_domain_bar(out_dir: Path, dpi: int) -> None:
    print("[plot] per-domain bar")
    rows = at_reference_seed(read_csv(RESULTS_DIR / "bootstrap_cis.csv"))
    keep = [r for r in rows
            if r["benchmark"] == "counterexample"
            and r["sampling_label"] == "greedy"
            and r["metric"] == "pass_at_1"
            and r["slice"].startswith("domain:")]
    by = {(r["model"], r["slice"].split(":", 1)[1]): r for r in keep}

    width = 0.20
    x = np.arange(len(DOMAINS))
    fig, ax = plt.subplots(figsize=(8.5, 3.3))

    for i, m in enumerate(MODEL_ORDER):
        points = []; err_lo = []; err_hi = []
        for d in DOMAINS:
            r = by.get((m, d))
            if r is None:
                points.append(0.0); err_lo.append(0.0); err_hi.append(0.0)
                continue
            p = float(r["point"]); lo = float(r["ci_lo"]); hi = float(r["ci_hi"])
            points.append(p); err_lo.append(p - lo); err_hi.append(hi - p)
        offset = (i - (len(MODEL_ORDER) - 1) / 2) * width
        label, color = MODEL_LABELS[m]
        ax.bar(x + offset, points, width=width,
               yerr=[err_lo, err_hi], capsize=2.0,
               label=label, color=color, edgecolor="white", linewidth=0.4)

    # n annotation on top
    for j, d in enumerate(DOMAINS):
        n = next((r["n"] for r in keep if r["slice"] == f"domain:{d}"), "?")
        ax.text(x[j], 0.95, f"n={n}", ha="center", fontsize=7, color="grey")

    ax.set_xticks(x)
    ax.set_xticklabels(DOMAINS)
    ax.set_ylabel("Pass@1 (greedy)")
    ax.set_ylim(0, 1.0)
    ax.set_title("Counterexample benchmark — per-domain Pass@1 with 95% bootstrap CIs")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=4, frameon=False, fontsize=8)
    _save(fig, "fig_per_domain", out_dir, dpi)


# ---------------------------------------------------------------------------
# Plot 5: counterexample baselines bar (ours vs 7B OSS vs frontier band)
# ---------------------------------------------------------------------------

OSS_7B = [
    ("mammoth2-7b-plus",          "MAmmoTH2-7B+"),
    ("abel-7b-002",               "Abel-7B-002"),
    ("deepseek-math-7b-rl",       "DeepSeek-Math-7B-RL"),
    ("qwen25-math-7b-instruct",   "Qwen2.5-Math-7B-Instr"),
    ("eurus-2-7b-prime",          "Eurus-2-7B-PRIME"),
]
FRONTIER_APIS = ["deepseek-flash", "deepseek-pro", "gemini-pro", "gemini-flash-preview", "gemini-flash", "gemini-flash-lite"]


def plot_baselines_bar(out_dir: Path, dpi: int) -> None:
    print("[plot] baselines bar")
    rows = at_reference_seed(read_csv(RESULTS_DIR / "bootstrap_cis.csv"))
    table = {r["model"]: r for r in rows
             if r["benchmark"] == "counterexample"
             and r["sampling_label"] == "greedy"
             and r["metric"] == "pass_at_1"
             and r["slice"] == "overall"}

    labels = []
    points = []
    los = []
    his = []
    colors = []

    # Group 1: our four models (Qwen3-4B family)
    for m in MODEL_ORDER:
        if m not in table:
            continue
        r = table[m]
        labels.append(MODEL_LABELS[m][0])
        points.append(float(r["point"]))
        los.append(float(r["ci_lo"]))
        his.append(float(r["ci_hi"]))
        colors.append(MODEL_LABELS[m][1])

    # Group 2: 7B OSS specialists
    for key, lab in OSS_7B:
        if key not in table:
            continue
        r = table[key]
        labels.append(lab)
        points.append(float(r["point"]))
        los.append(float(r["ci_lo"]))
        his.append(float(r["ci_hi"]))
        colors.append("#7f7f7f")

    points = np.array(points); los = np.array(los); his = np.array(his)

    fig, ax = plt.subplots(figsize=(9.5, 4.0))
    y = np.arange(len(labels))
    ax.barh(y, points, xerr=[points - los, his - points],
            color=colors, edgecolor="white", linewidth=0.4, capsize=2.5)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Counterexample Pass@1 (greedy, n=201)")
    ax.set_xlim(0, 0.75)
    ax.set_title("Counterexample benchmark — our 4B method vs open-weights 7B math specialists")

    # Frontier API band
    api_points = [float(table[k]["point"]) for k in FRONTIER_APIS if k in table]
    if api_points:
        api_min, api_max = min(api_points), max(api_points)
        ax.axvspan(api_min, api_max, color="#fff2cc", alpha=0.6, zorder=0)
        ax.text(api_max + 0.005, len(labels) - 0.5,
                f"frontier commercial APIs\n(range {api_min:.2f}–{api_max:.2f}, n={len(api_points)})",
                va="bottom", ha="left", fontsize=8, color="#a07a00")

    # Value labels
    for yi, p in zip(y, points):
        ax.text(p + 0.005, yi, f"{p:.2f}", va="center", fontsize=8)

    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", alpha=0.2)
    _save(fig, "fig_baselines", out_dir, dpi)


# ---------------------------------------------------------------------------
# Plot 6: OOD transfer (GSM8K / MATH-500 / MMLU-CM / AIME)
# ---------------------------------------------------------------------------

OOD_BENCHES = [
    ("gsm8k",             "GSM8K (n=1319)"),
    ("math",              "MATH-500 (n=500)"),
    ("mmlu_college_math", "MMLU-College-Math (n=100)"),
    ("aime2024",          "AIME-2024 (n=30)"),
]


def plot_ood_bar(out_dir: Path, dpi: int) -> None:
    print("[plot] ood bar")
    rows = at_reference_seed(read_csv(RESULTS_DIR / "bootstrap_cis.csv"))
    by = {(r["model"], r["benchmark"]): r for r in rows
          if r["prompt_style"] == "standard_cot"
          and r["sampling_label"] == "greedy"
          and r["metric"] == "pass_at_1"
          and r["slice"] == "overall"}

    width = 0.20
    x = np.arange(len(OOD_BENCHES))
    fig, ax = plt.subplots(figsize=(8.0, 3.4))

    for i, m in enumerate(MODEL_ORDER):
        points = []; err_lo = []; err_hi = []
        for bench, _ in OOD_BENCHES:
            r = by.get((m, bench))
            if r is None:
                points.append(0.0); err_lo.append(0.0); err_hi.append(0.0)
                continue
            p = float(r["point"]); lo = float(r["ci_lo"]); hi = float(r["ci_hi"])
            points.append(p); err_lo.append(p - lo); err_hi.append(hi - p)
        offset = (i - (len(MODEL_ORDER) - 1) / 2) * width
        label, color = MODEL_LABELS[m]
        ax.bar(x + offset, points, width=width,
               yerr=[err_lo, err_hi], capsize=2.0,
               label=label, color=color, edgecolor="white", linewidth=0.4)
        for xi, p in zip(x + offset, points):
            ax.text(xi, p + 0.01, f"{p:.2f}", ha="center", va="bottom", fontsize=7)

    ax.set_xticks(x)
    ax.set_xticklabels([b[1] for b in OOD_BENCHES])
    ax.set_ylabel("Pass@1 (greedy, standard CoT)")
    ax.set_ylim(0, 1.0)
    ax.set_title("Out-of-domain transfer — RLVR does not regress general math reasoning")
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=4, frameon=False, fontsize=8)
    _save(fig, "fig_ood_transfer", out_dir, dpi)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_PLOTS_DIR)
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--reason-stack", action="store_true")
    ap.add_argument("--truth-bar", action="store_true")
    ap.add_argument("--training-curves", action="store_true")
    ap.add_argument("--domain-bar", action="store_true")
    ap.add_argument("--baselines-bar", action="store_true")
    ap.add_argument("--ood-bar", action="store_true")
    args = ap.parse_args()

    if not any([args.reason_stack, args.truth_bar, args.training_curves,
                args.domain_bar, args.baselines_bar, args.ood_bar]):
        args.all = True

    plt.rcParams.update({
        "font.size": 9,
        "axes.labelsize": 10,
        "axes.titlesize": 10,
        "figure.dpi": args.dpi,
        "savefig.dpi": args.dpi,
        "pdf.fonttype": 42,  # editable text in vector PDFs
        "ps.fonttype": 42,
    })

    if args.all or args.reason_stack:
        plot_reason_stack(args.out_dir, args.dpi)
    if args.all or args.truth_bar:
        plot_truth_bar(args.out_dir, args.dpi)
    if args.all or args.training_curves:
        plot_training_curves(args.out_dir, args.dpi)
    if args.all or args.domain_bar:
        plot_domain_bar(args.out_dir, args.dpi)
    if args.all or args.baselines_bar:
        plot_baselines_bar(args.out_dir, args.dpi)
    if args.all or args.ood_bar:
        plot_ood_bar(args.out_dir, args.dpi)

    print(f"\nDone. Plots in {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
