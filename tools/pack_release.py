#!/usr/bin/env python3
"""Assemble the public SymCE release from a camera-ready export bundle.

The export bundle is ~600 MB, most of it raw evaluation records and rollouts.
This produces a repository that is small enough to host on GitHub while still
regenerating every number in the paper:

  * only the evaluation suites the paper actually cites are carried over;
  * per-record completions are dropped except where an analysis script needs
    them (qualitative example selection, and the theorem-truth answer
    extraction of ``paper_preparation/scripts/truth_answer.py``);
  * every evaluation record is gzipped.

Gemma-3-4B artifacts are excluded in full -- adapters, training configs, eval
outputs and the suite configs that name them -- because those checkpoints are not
part of the public release (see the paper's Limitations).
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
import shutil

# Evaluation suites cited by the camera-ready tables.
KEEP_SUITES = {
    "20260522-044136",  # seed 42, dense + in-domain baselines
    "20260522-222105",  # seed 42, sparse
    "20260523-140214",  # open-weights 7B comparators
    "20260523-165202", "20260523-165233", "20260523-181910",
    "20260523-215427", "20260523-223410",  # commercial API comparators
    "20260524-003142",  # seed 42, theorem-truth probes
    "20260625-112130",  # seed 19
    "20260704-093428",  # seed 31
    "20260714-062945",  # seed 64
}

# Cells whose completions must survive: the answer-extraction rules are applied
# to raw text, and the qualitative appendix quotes it.
KEEP_COMPLETIONS_SUBSTR = ("__theorem_truth__", "__counterexample__")

EXCLUDE_NAME_SUBSTR = ("gemma", "llama")

COPY_TREES = ["src", "training", "tools", "prompts", "human_eval", "tests", "docs"]
COPY_FILES = ["requirements.txt", "requirements-train.txt", "pipeline.py", "README.md"]

DATA_FILES = [
    "test_set.jsonl", "theorem_truth_eval.jsonl", "sft_data.jsonl",
    "rlvr_prompts.jsonl", "witness_schemas.jsonl", "dataset_stats.json",
    "oracle_perf_probe.json", "verifier_audit_report.json",
    "symce_corpus.jsonl",
]


def excluded(path: str) -> bool:
    low = path.lower()
    return any(tok in low for tok in EXCLUDE_NAME_SUBSTR)


def pack_cell(src: str, dst: str) -> tuple[int, int]:
    with open(src) as fh:
        doc = json.load(fh)
    keep_text = any(tok in os.path.basename(src) for tok in KEEP_COMPLETIONS_SUBSTR)
    dropped = 0
    for record in doc.get("per_record", []):
        for sample in record.get("samples", []):
            if "completion" in sample and not keep_text:
                sample["completion_chars"] = len(sample["completion"])
                del sample["completion"]
                dropped += 1
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with gzip.open(dst, "wt", encoding="utf-8") as fh:
        json.dump(doc, fh, separators=(",", ":"))
    return dropped, os.path.getsize(dst)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--export", required=True, help="camera_ready_export_* directory")
    ap.add_argument("--out", required=True, help="destination repository root")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    total = 0
    kept_cells = skipped_cells = 0

    def report(label, path):
        nonlocal total
        size = os.path.getsize(path) if os.path.isfile(path) else 0
        total += size
        return size

    # ---- evaluation records -------------------------------------------------
    eval_root = os.path.join(args.export, "runs", "eval")
    for suite_dir in sorted(os.listdir(eval_root)):
        suite = suite_dir.split("__")[0]
        if suite not in KEEP_SUITES:
            continue
        per_cell = os.path.join(eval_root, suite_dir, "per_cell")
        if not os.path.isdir(per_cell):
            continue
        for name in sorted(os.listdir(per_cell)):
            if excluded(name):
                skipped_cells += 1
                continue
            src = os.path.join(per_cell, name)
            dst = os.path.join(args.out, "runs", "eval", suite_dir, "per_cell", name + ".gz")
            if args.dry_run:
                kept_cells += 1
                continue
            _, size = pack_cell(src, dst)
            total += size
            kept_cells += 1
        # suite provenance, minus anything naming an excluded checkpoint
        for meta in ("suite_config.yaml", "dataset_fingerprint.json", "git_info.json",
                     "invocation.json", "status.json"):
            src = os.path.join(eval_root, suite_dir, meta)
            if not os.path.exists(src):
                continue
            body = open(src).read()
            if excluded(body):
                body = "\n".join(l for l in body.splitlines() if not excluded(l))
            dst = os.path.join(args.out, "runs", "eval", suite_dir, meta)
            if not args.dry_run:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                open(dst, "w").write(body)
                total += os.path.getsize(dst)

    # ---- data ---------------------------------------------------------------
    for name in DATA_FILES:
        src = os.path.join(args.export, "data", name)
        if os.path.exists(src) and not args.dry_run:
            dst = os.path.join(args.out, "data", name)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            report(name, dst)
    verifiers_src = os.path.join(args.export, "data", "verifiers")
    verifiers_dst = os.path.join(args.out, "data", "verifiers")
    if os.path.isdir(verifiers_src) and not args.dry_run:
        shutil.copytree(verifiers_src, verifiers_dst, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    # ---- code, configs, docs ------------------------------------------------
    for tree in COPY_TREES:
        src = os.path.join(args.export, tree)
        if os.path.isdir(src) and not args.dry_run:
            shutil.copytree(src, os.path.join(args.out, tree), dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for name in COPY_FILES:
        src = os.path.join(args.export, name)
        if os.path.exists(src) and not args.dry_run:
            shutil.copy2(src, os.path.join(args.out, name))

    cfg_src = os.path.join(args.export, "configs")
    for root, _, files in os.walk(cfg_src):
        for name in files:
            if excluded(name):
                continue
            src = os.path.join(root, name)
            rel = os.path.relpath(src, cfg_src)
            dst = os.path.join(args.out, "configs", rel)
            if not args.dry_run:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)

    # ---- training-run summaries (no weights, no rollouts) -------------------
    for phase in ("sft", "rlvr"):
        root = os.path.join(args.export, "runs", phase)
        if not os.path.isdir(root):
            continue
        for run in sorted(os.listdir(root)):
            if excluded(run):
                continue
            for meta in ("config.json", "status.json", "train_log.csv",
                         "run_summary.md", "rollouts_summary.json",
                         "sft_diagnostics.json"):
                src = os.path.join(root, run, meta)
                if os.path.exists(src) and not args.dry_run:
                    dst = os.path.join(args.out, "runs", phase, run, meta)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy2(src, dst)

    print(f"eval cells kept: {kept_cells}   excluded (withheld family): {skipped_cells}")
    if not args.dry_run:
        out_size = sum(os.path.getsize(os.path.join(d, f))
                       for d, _, fs in os.walk(args.out) for f in fs)
        print(f"release size: {out_size/1048576:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
