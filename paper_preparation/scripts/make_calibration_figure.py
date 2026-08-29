#!/usr/bin/env python3
"""Render the calibration-probe figure from the regenerated tables.

The figure that shipped with earlier drafts was drawn before the answer-extraction
correction documented in ``build_camera_ready_tables.py`` and showed an inflated
base model.  This redraws it from ``camera_ready_tables.json`` so the figure can
never drift from the numbers in the paper.
"""
from __future__ import annotations

import argparse
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ARMS = ["base", "SFT", "dense", "sparse"]
LABELS = ["Qwen3-4B\nbase", "+ SFT", "+ RLVR\ndense", "+ RLVR\nsparse"]
INK = "#1b1b1b"
GREY = "#9aa0a6"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tables", default="paper_preparation/results/camera_ready_tables.json")
    ap.add_argument("--out", default="paper_preparation/plots/fig_calibration.png")
    ap.add_argument("--dpi", type=int, default=200)
    args = ap.parse_args()

    tables = json.load(open(args.tables))
    trap = tables["trap"]
    v2 = [trap[a]["v2_strict"] for a in ARMS]
    tc = [trap[a]["truth_classify"] for a in ARMS]

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.4), sharey=True)
    for ax, values, title in (
        (axes[0], v2, "Counterexample-emit prompt\n(same style as training)"),
        (axes[1], tc, "Explicit true/false prompt"),
    ):
        colours = [GREY, "#b03a3a", "#6d8fbf", "#2f6b52"]
        bars = ax.bar(LABELS, values, color=colours, width=0.62, zorder=3)
        ax.axhline(values[0], color=GREY, linestyle=(0, (4, 3)), linewidth=1, zorder=2)
        for bar, value in zip(bars, values):
            ax.annotate(f"{value:.2f}", (bar.get_x() + bar.get_width() / 2, value),
                        textcoords="offset points", xytext=(0, 4),
                        ha="center", fontsize=9.5, color=INK)
        ax.set_title(title, fontsize=10, color=INK, pad=10)
        ax.set_ylim(0, 1.0)
        ax.grid(axis="y", color="#e6e6e6", linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color("#cfcfcf")
        ax.tick_params(colors=INK, labelsize=9.5, length=0)

    axes[0].set_ylabel("true theorems recognised", fontsize=10, color=INK)
    fig.suptitle("Counterexample-only SFT destroys calibrated abstention; sparse-reward RLVR restores it",
                 fontsize=11, color=INK, y=1.04)
    fig.tight_layout()
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    fig.savefig(args.out, dpi=args.dpi, bbox_inches="tight", facecolor="white")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
