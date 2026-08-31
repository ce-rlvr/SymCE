#!/usr/bin/env python3
"""Regenerate every number in the camera-ready paper from raw evaluation records.

Single source of truth.  Reads ``runs/eval/**/per_cell/*.json`` and emits one JSON
plus one Markdown report containing every table in the paper.

Both theorem-truth prompt styles are rescored here, because the evaluation harness
that produced the raw records used a last-resort label parser, ``\\b(true|false)\\b``,
that matched any bare occurrence of the word anywhere in a completion and took the
last one.  In a chain of thought about whether a theorem is true that word occurs
constantly, so completions that exhausted the generation budget mid-reasoning --
stating no answer at all -- were scored as if they had answered TRUE.

  v2_counterexample   strict: correct iff the literal NONE sentinel was emitted.
                      Of the 206 seed-42 base records the shipped scorer counted
                      correct without a sentinel, 170 hit the token cap, 0 contained
                      a [COUNTEREXAMPLE: tag, and 1 closed its reasoning block.
  truth_classify      correct iff ``truth_answer.extract_truth_label`` finds an
                      explicit verdict in an answer frame near the end of the
                      completion.  Validated on this corpus: every record it scores
                      as stating no verdict is an unfinished completion, so it
                      cannot understate a model that did answer.

The ``as shipped`` figures are retained alongside so the correction is auditable.

Usage:
    python -m paper_preparation.scripts.build_camera_ready_tables --runs-root <dir>
"""
from __future__ import annotations

import argparse
import json
import glob
import gzip
import os
import re
import statistics as st
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from truth_answer import extract_truth_label  # noqa: E402

# Suites excluded from every aggregate, with the reason.
EXCLUDED_SUITES = {
    "20260714-043917": "single exploratory LoRA rank-64 SFT probe; not part of the reported configuration",
}

QWEN_SEEDS = ["42", "19", "31", "64"]
ARMS = [("base", "qwen3-base"), ("SFT", "qwen-sft"),
        ("dense", "qwen-rlvr"), ("sparse", "qwen-rlvr-sparse")]
DOMAINS = ["GroupTheory", "RingTheory", "NumberTheory",
           "LinearAlgebra", "FieldTheory", "RealAnalysis"]


def is_none(sample: dict) -> bool:
    """Strict NONE-sentinel test (mirrors the evaluation harness)."""
    if isinstance(sample.get("is_none"), bool):
        return bool(sample["is_none"])
    for key in ("extracted", "payload"):
        value = sample.get(key)
        if isinstance(value, str) and value.strip().lower() == "none":
            return True
    return False


def load_cells(runs_root: str):
    """Yield (suite_id, seed, summary, per_record) for every usable eval cell.

    Accepts both the raw ``.json`` cells produced by the evaluation harness and the
    gzipped ``.json.gz`` cells carried by the public release.
    """
    base = os.path.join(runs_root, "eval", "*__thesis_full__suite", "per_cell")
    paths = sorted(glob.glob(os.path.join(base, "*.json"))
                   + glob.glob(os.path.join(base, "*.json.gz")))
    for path in paths:
        suite = os.path.basename(os.path.dirname(os.path.dirname(path))).split("__")[0]
        if suite in EXCLUDED_SUITES:
            continue
        opener = gzip.open if path.endswith(".gz") else open
        with opener(path, "rt", encoding="utf-8") as fh:
            doc = json.load(fh)
        summary = doc["summary"]
        match = re.search(r"seed(\d+)", summary.get("model_id") or "")
        yield suite, (match.group(1) if match else None), summary, doc.get("per_record", [])


class Cells:
    """Indexed view over the evaluation corpus."""

    def __init__(self, runs_root: str):
        self.by_key = defaultdict(list)
        for suite, seed, summary, records in load_cells(runs_root):
            key = (seed, summary["model"], summary["benchmark"],
                   summary["prompt_style"], summary["sampling_label"])
            self.by_key[key].append((suite, summary, records))

    def get(self, seed, model, benchmark, style, sampling="greedy"):
        hits = self.by_key.get((seed, model, benchmark, style, sampling), [])
        return hits[0] if hits else None

    def all(self, seed, model, benchmark, style, sampling="greedy"):
        return self.by_key.get((seed, model, benchmark, style, sampling), [])


# --------------------------------------------------------------------------- metrics

def greedy_sample(record: dict) -> dict:
    return record["samples"][0]


def truth_pass1(records, convention: str) -> float:
    """Theorem-truth Pass@1 under the given scoring convention.

    ``strict``     the literal NONE sentinel was emitted (what the paper reports).
    ``as_shipped`` whatever the original harness recorded, retained so the
                   correction documented in the module docstring is auditable.
    """
    if convention == "strict":
        hit = is_none
    elif convention == "as_shipped":
        hit = lambda s: bool(s.get("correct"))
    else:
        raise ValueError(convention)
    return sum(1 for r in records if hit(greedy_sample(r))) / len(records)


def truth_subsets(records, convention: str) -> dict:
    buckets = defaultdict(lambda: [0, 0])
    hit = is_none if convention == "strict" else (lambda s: bool(s.get("correct")))
    for r in records:
        name = r.get("subset") or "unknown"
        buckets[name][1] += 1
        if hit(greedy_sample(r)):
            buckets[name][0] += 1
    return {k: {"n": n, "correct": c, "rate": c / n} for k, (c, n) in buckets.items()}


def truth_classify_outcomes(records) -> dict:
    """Outcome breakdown under the ``truth_classify`` prompt style.

    Every probe item is a TRUE theorem, so ``said_true`` is the Pass@1 rate.
    ``no_verdict`` counts completions that state no answer at all -- overwhelmingly
    ones that exhausted the generation budget mid-reasoning.  Reporting it
    separately keeps a model that runs out of tokens distinguishable from one that
    confidently answers FALSE.
    """
    labels = []
    for record in records:
        sample = greedy_sample(record)
        if "completion" not in sample:
            return {"unavailable": True}
        labels.append(extract_truth_label(sample["completion"]))
    total = len(labels)
    return {
        "said_true": sum(1 for l in labels if l == "TRUE") / total,
        "said_false": sum(1 for l in labels if l == "FALSE") / total,
        "no_verdict": sum(1 for l in labels if l is None) / total,
        "n": total,
    }


def rate(records, field: str) -> float:
    return sum(1 for r in records if greedy_sample(r).get(field)) / len(records)


def reason_distribution(records) -> dict:
    counts = defaultdict(int)
    for r in records:
        counts[greedy_sample(r).get("reason") or "unknown"] += 1
    total = len(records)
    return {k: v / total for k, v in sorted(counts.items())}


def per_domain(records) -> dict:
    buckets = defaultdict(lambda: [0, 0])
    for r in records:
        buckets[r.get("domain") or "unknown"][1] += 1
        if r.get("any_correct"):
            buckets[r["domain"]][0] += 1
    return {k: {"n": n, "rate": c / n} for k, (c, n) in buckets.items()}


def summarise(values):
    values = [v for v in values if v is not None]
    if not values:
        return None
    return {
        "mean": st.mean(values),
        "sd": st.stdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
        "n": len(values),
        "values": values,
    }


# --------------------------------------------------------------------------- tables

def table_main(cells: Cells, seed: str = "42") -> dict:
    """Table 2: in-domain counterexample benchmark, reference seed."""
    out = {}
    for label, model in ARMS:
        key_seed = None if label == "base" else seed
        greedy = cells.get(key_seed, model, "counterexample", "v2_counterexample", "greedy")
        sampled = cells.get(key_seed, model, "counterexample", "v2_counterexample", "sampled")
        if greedy is None:
            continue
        _, gsum, grecs = greedy
        row = {
            "pass_at_1_greedy": gsum["pass_at_1_greedy"],
            "conclusion_pass_rate": gsum["conclusion_pass_rate"],
            "format_ok": rate(grecs, "format_ok"),
            "parse_ok": rate(grecs, "parse_ok"),
            "n": gsum["n_problems"],
        }
        if sampled is not None:
            row["pass_at_8_sampled"] = (sampled[1].get("pass_at_k") or {}).get("8")
        out[label] = row
    return out


def table_trap(cells: Cells, seed: str = "42") -> dict:
    """Table 3: theorem-truth probe, both prompt styles, both conventions."""
    out = {}
    for label, model in ARMS:
        key_seed = None if label == "base" else seed
        v2 = cells.get(key_seed, model, "theorem_truth", "v2_counterexample", "greedy")
        tc = cells.get(key_seed, model, "theorem_truth", "truth_classify", "greedy")
        row = {}
        if v2 is not None:
            _, vsum, vrecs = v2
            row["v2_strict"] = truth_pass1(vrecs, "strict")
            row["v2_as_shipped"] = truth_pass1(vrecs, "as_shipped")
            row["v2_subsets_strict"] = truth_subsets(vrecs, "strict")
            row["n"] = vsum["n_problems"]
        if tc is not None:
            outcomes = truth_classify_outcomes(tc[2])
            row["truth_classify_outcomes"] = outcomes
            row["truth_classify"] = outcomes.get("said_true")
            row["truth_classify_as_shipped"] = tc[1]["pass_at_1_greedy"]
        out[label] = row
    return out


def table_multiseed(cells: Cells) -> dict:
    """Four-seed robustness summary (Qwen3-4B)."""
    metrics = {
        "counterexample_pass_at_1_greedy": ("counterexample", "v2_counterexample", "greedy", "p1"),
        "counterexample_pass_at_8_sampled": ("counterexample", "v2_counterexample", "sampled", "p8"),
        "truth_v2_strict": ("theorem_truth", "v2_counterexample", "greedy", "v2"),
        "truth_classify": ("theorem_truth", "truth_classify", "greedy", "tc"),
    }
    out = {}
    for metric, (bench, style, sampling, kind) in metrics.items():
        out[metric] = {}
        for label, model in ARMS:
            if label == "base":
                hits = cells.all(None, model, bench, style, sampling)
                values = []
                for _, summary, records in hits:
                    values.append(_extract(kind, summary, records))
                out[metric][label] = {
                    "value": st.mean(values) if values else None,
                    "note": ("base model is training-seed independent; "
                             f"evaluated {len(values)} times, range "
                             f"{min(values):.4f}-{max(values):.4f}" if values else None),
                }
                continue
            values = []
            for seed in QWEN_SEEDS:
                hit = cells.get(seed, model, bench, style, sampling)
                values.append(_extract(kind, hit[1], hit[2]) if hit else None)
            out[metric][label] = summarise(values)
            out[metric][label]["per_seed"] = dict(zip(QWEN_SEEDS, values))
    # sparse-minus-dense gap on the v2 probe, per seed
    dense = out["truth_v2_strict"]["dense"]["per_seed"]
    sparse = out["truth_v2_strict"]["sparse"]["per_seed"]
    gaps = {s: sparse[s] - dense[s] for s in QWEN_SEEDS if dense[s] is not None}
    out["sparse_minus_dense_v2"] = {"per_seed": gaps, **summarise(list(gaps.values()))}
    return out


def _extract(kind, summary, records):
    if kind == "p1":
        return (summary.get("pass_at_1_greedy") if summary["sampling_label"] == "greedy"
                else (summary.get("pass_at_k") or {}).get("1"))
    if kind == "p8":
        return (summary.get("pass_at_k") or {}).get("8")
    if kind == "v2":
        return truth_pass1(records, "strict")
    if kind == "tc":
        return truth_classify_outcomes(records).get("said_true")
    raise ValueError(kind)


def table_ood(cells: Cells, seeds=tuple(QWEN_SEEDS)) -> dict:
    """Out-of-domain transfer under standard chain-of-thought prompting."""
    benches = [("gsm8k", 1319), ("math", 500), ("mmlu_college_math", 100), ("aime2024", 30)]
    out = {"seeds_used": [], "seeds_missing": []}
    for bench, n in benches:
        out[bench] = {"n": n}
        for label, model in ARMS:
            if label == "base":
                hit = cells.get(None, model, bench, "standard_cot", "greedy")
                out[bench][label] = {"value": hit[1]["pass_at_1_greedy"] if hit else None}
                continue
            values = []
            for seed in seeds:
                hit = cells.get(seed, model, bench, "standard_cot", "greedy")
                values.append(hit[1]["pass_at_1_greedy"] if hit else None)
            summary = summarise(values)
            if summary:
                summary["per_seed"] = dict(zip(seeds, values))
            out[bench][label] = summary
    # Which seeds actually carry a transfer evaluation, measured rather than assumed.
    present, absent = [], []
    for seed in seeds:
        if any(cells.get(seed, model, bench, "standard_cot", "greedy")
               for bench, _ in benches for label, model in ARMS if label != "base"):
            present.append(seed)
        else:
            absent.append(seed)
    out["seeds_used"], out["seeds_missing"] = present, absent
    return out


def table_reason(cells: Cells, seed: str = "42") -> dict:
    out = {}
    for label, model in ARMS:
        hit = cells.get(None if label == "base" else seed, model,
                        "counterexample", "v2_counterexample", "greedy")
        if hit:
            out[label] = reason_distribution(hit[2])
    return out


def table_per_domain(cells: Cells, seed: str = "42") -> dict:
    out = {}
    for label, model in ARMS:
        hit = cells.get(None if label == "base" else seed, model,
                        "counterexample", "v2_counterexample", "greedy")
        if hit:
            out[label] = per_domain(hit[2])
    return out


def table_external(cells: Cells) -> dict:
    """Appendix: open-weights and commercial-API comparators."""
    oss = ["eurus-2-7b-prime", "qwen25-math-7b-instruct", "deepseek-math-7b-rl",
           "abel-7b-002", "mammoth2-7b-plus", "qwen-base"]
    api = ["gemini-flash-lite", "gemini-flash", "gemini-flash-preview",
           "deepseek-pro", "gemini-pro", "deepseek-flash"]
    out = {"open_weights": {}, "commercial_api": {}}
    for group, names in (("open_weights", oss), ("commercial_api", api)):
        for name in names:
            greedy = cells.get(None, name, "counterexample", "v2_counterexample", "greedy")
            sampled = cells.get(None, name, "counterexample", "v2_counterexample", "sampled")
            if greedy is None:
                continue
            row = {"pass_at_1_greedy": greedy[1]["pass_at_1_greedy"],
                   "conclusion_pass_rate": greedy[1]["conclusion_pass_rate"]}
            if sampled is not None:
                pk = sampled[1].get("pass_at_k") or {}
                row.update({f"pass_at_{k}_sampled": pk.get(k) for k in ("1", "3", "5", "8")})
            out[group][name] = row
    values = [r["pass_at_1_greedy"] for r in out["commercial_api"].values()]
    out["commercial_api_range"] = {"min": min(values), "max": max(values), "n": len(values)}
    return out


# --------------------------------------------------------------------------- Gemma

# Gemma eval cells record only the base model path in ``model_id``, so the
# checkpoint identity comes from the suite that produced them.
GEMMA_SUITES = {
    "seed56": {"base": "20260714-141859", "sft": "20260714-160032",
               "sft_truth": "20260712-073823", "dense": "20260714-110447",
               "sparse": "20260714-110447", "dense_truth": "20260714-141859",
               "sparse_truth": "20260714-141859"},
    "seed24": {"base": "20260828-234303", "sft": "20260828-234303",
               "dense": "20260828-234303", "dense_truth": "20260828-234303"},
}
GEMMA_MODELS = {"base": "gemma3-base", "sft": "gemma3-sft",
                "dense": "gemma3-rlvr-dense", "sparse": "gemma3-rlvr-sparse"}

# The Gemma RLVR checkpoints are not part of the public release, and their
# v2-probe results are correspondingly not reported.  The collapse itself
# (base -> SFT) is reported and is reproducible from the numbers below.
GEMMA_V2_ARMS_REPORTED = {"base", "sft", "dense"}


def _pick(cells: Cells, suite: str, model: str, bench: str, style: str, sampling: str,
          allow_any_suite: bool = False):
    hits = cells.all(None, model, bench, style, sampling)
    for hit in hits:
        if hit[0] == suite:
            return hit
    # The untrained base is the same checkpoint in every suite, so any suite serves.
    return hits[0] if (allow_any_suite and hits) else None


def table_gemma(cells: Cells) -> dict:
    out = {}
    for run, suites in GEMMA_SUITES.items():
        row = {}
        for arm, model in GEMMA_MODELS.items():
            if arm not in suites:
                continue
            entry = {}
            any_suite = (arm == "base")
            hit = _pick(cells, suites[arm], model, "counterexample", "v2_counterexample",
                        "greedy", any_suite)
            if hit:
                entry["pass_at_1_greedy"] = hit[1]["pass_at_1_greedy"]
            hit = _pick(cells, suites[arm], model, "counterexample", "v2_counterexample",
                        "sampled", any_suite)
            if hit:
                entry["pass_at_8_sampled"] = (hit[1].get("pass_at_k") or {}).get("8")
            tsuite = suites.get(f"{arm}_truth", suites[arm])
            hit = _pick(cells, tsuite, model, "theorem_truth", "truth_classify",
                        "greedy", any_suite)
            if hit:
                outcomes = truth_classify_outcomes(hit[2])
                entry["truth_classify"] = outcomes.get("said_true")
                entry["truth_classify_outcomes"] = outcomes
                entry["truth_classify_as_shipped"] = hit[1]["pass_at_1_greedy"]
            if arm in GEMMA_V2_ARMS_REPORTED:
                hit = _pick(cells, tsuite, model, "theorem_truth", "v2_counterexample",
                            "greedy", any_suite)
                if hit:
                    entry["v2_strict"] = truth_pass1(hit[2], "strict")
            if entry:
                row[arm] = entry
        out[run] = row
    if not any(out[run] for run in GEMMA_SUITES):
        out["_note"] = ("No Gemma cells found. The public release excludes all Gemma-3-4B "
                        "artifacts -- adapters, configs and evaluation outputs -- so the "
                        "Gemma rows of the paper cannot be regenerated from it. Run "
                        "against the full evaluation corpus to reproduce them.")
    else:
        out["_note"] = ("Gemma RLVR v2-probe results are not reported; those "
                        "checkpoints and their configs are not part of the "
                        "artifact release.")
    return out


# --------------------------------------------------------------------------- human audit

def table_human_audit(audit_dir: str) -> dict:
    import csv
    accepted = os.path.join(audit_dir, "accepted_counterexamples_review.csv")
    rejected = os.path.join(audit_dir, "rejected_counterexamples_review.csv")
    if not (os.path.exists(accepted) and os.path.exists(rejected)):
        return {"error": f"audit CSVs not found under {audit_dir}"}

    def read(path, column):
        with open(path) as fh:
            rows = list(csv.DictReader(fh))
        verdicts = [r[column].strip().lower() for r in rows]
        return rows, verdicts

    arows, averdicts = read(accepted, "Accept?")
    rrows, rverdicts = read(rejected, "Accepted Counterexample?")
    n_acc, n_rej = len(arows), len(rrows)
    acc_valid = sum(1 for v in averdicts if v == "yes")
    rej_correct = sum(1 for v in rverdicts if v == "no")
    by_domain = defaultdict(lambda: {"accepted": 0, "rejected": 0})
    for r in arows:
        by_domain[r["Category"].strip()]["accepted"] += 1
    for r in rrows:
        by_domain[r["Category"].strip()]["rejected"] += 1
    by_model = defaultdict(int)
    for r in arows + rrows:
        by_model[r["Model Type"].strip()] += 1
    return {
        "n_total": n_acc + n_rej,
        "n_accepted_audited": n_acc,
        "n_rejected_audited": n_rej,
        "accepted_confirmed_valid": acc_valid,
        "false_accept_rate": (n_acc - acc_valid) / n_acc,
        "rejected_confirmed_invalid": rej_correct,
        "decision_accuracy": (acc_valid + rej_correct) / (n_acc + n_rej),
        "by_domain": dict(by_domain),
        "by_model_type": dict(by_model),
        "annotated_comments": {
            "accepted": sum(1 for r in arows if r["Comments"].strip()),
            "rejected": sum(1 for r in rrows if r["Comments"].strip()),
        },
    }


# --------------------------------------------------------------------------- rendering

def fmt(value, places=3):
    if value is None:
        return "--"
    return f"{value:.{places}f}"


def render_markdown(tables: dict) -> str:
    lines = ["# Camera-ready tables", "",
             "Regenerated from raw evaluation records by "
             "`paper_preparation/scripts/build_camera_ready_tables.py`.", "",
             "Theorem-truth `v2_counterexample` uses **strict** scoring "
             "(literal NONE sentinel only); the lenient variant is shown for comparison.", ""]

    m = tables["main"]
    lines += ["## In-domain counterexample benchmark (reference seed 42, n=201)", "",
              "| Model | Pass@1 greedy | Pass@8 sampled | Conclusion-pass | Format-OK | Parse-OK |",
              "|---|---:|---:|---:|---:|---:|"]
    for label, _ in ARMS:
        r = m.get(label, {})
        lines.append(f"| {label} | {fmt(r.get('pass_at_1_greedy'))} | {fmt(r.get('pass_at_8_sampled'))} "
                     f"| {fmt(r.get('conclusion_pass_rate'))} | {fmt(r.get('format_ok'),2)} "
                     f"| {fmt(r.get('parse_ok'),2)} |")

    t = tables["trap"]
    lines += ["", "## Theorem-truth probe (reference seed 42, n=347)", "",
              "| Model | v2 strict | v2 as shipped | truth_classify | says FALSE | no verdict |",
              "|---|---:|---:|---:|---:|---:|"]
    for label, _ in ARMS:
        r = t.get(label, {})
        o = r.get("truth_classify_outcomes", {})
        lines.append(f"| {label} | {fmt(r.get('v2_strict'))} | {fmt(r.get('v2_as_shipped'))} "
                     f"| {fmt(r.get('truth_classify'))} | {fmt(o.get('said_false'))} "
                     f"| {fmt(o.get('no_verdict'))} |")

    ms = tables["multiseed"]
    lines += ["", "## Four-seed robustness (seeds 42, 19, 31, 64)", "",
              "| Metric | base | SFT | dense | sparse |", "|---|---:|---:|---:|---:|"]
    for metric in ("counterexample_pass_at_1_greedy", "counterexample_pass_at_8_sampled",
                   "truth_v2_strict", "truth_classify"):
        cells_out = []
        for label, _ in ARMS:
            r = ms[metric][label]
            if label == "base":
                cells_out.append(fmt(r.get("value")))
            else:
                cells_out.append(f"{fmt(r['mean'])} ± {fmt(r['sd'])}")
        lines.append(f"| {metric} | " + " | ".join(cells_out) + " |")
    gap = ms["sparse_minus_dense_v2"]
    lines += ["", f"Sparse minus dense on the v2 probe: **{fmt(gap['mean'])} ± {fmt(gap['sd'])}**, "
                  f"per seed " + ", ".join(f"{k}={fmt(v)}" for k, v in gap["per_seed"].items()) + "."]

    o = tables["ood"]
    lines += ["", f"## Out-of-domain transfer (mean over seeds {', '.join(o['seeds_used'])})", "",
              "| Benchmark | n | base | SFT | dense | sparse |", "|---|---:|---:|---:|---:|---:|"]
    for bench in ("gsm8k", "math", "mmlu_college_math", "aime2024"):
        row = o[bench]
        vals = []
        for label, _ in ARMS:
            r = row[label]
            vals.append(fmt(r.get("value")) if label == "base" else
                        (f"{fmt(r['mean'])} ± {fmt(r['sd'])}" if r else "--"))
        lines.append(f"| {bench} | {row['n']} | " + " | ".join(vals) + " |")
    lines.append("")
    lines.append(f"Seeds without transfer evaluations: {', '.join(o['seeds_missing'])}.")

    r = tables["reason"]
    keys = sorted({k for v in r.values() for k in v})
    lines += ["", "## Reason distribution (reference seed 42, greedy, n=201)", "",
              "| Model | " + " | ".join(keys) + " |", "|---" * (len(keys) + 1) + "|"]
    for label, _ in ARMS:
        lines.append(f"| {label} | " + " | ".join(fmt(r.get(label, {}).get(k, 0.0)) for k in keys) + " |")

    d = tables["per_domain"]
    lines += ["", "## Per-domain Pass@1 (reference seed 42, greedy)", "",
              "| Domain | n | " + " | ".join(l for l, _ in ARMS) + " |", "|---|---:|---:|---:|---:|---:|"]
    for dom in DOMAINS:
        n = d["base"].get(dom, {}).get("n", 0)
        lines.append(f"| {dom} | {n} | " +
                     " | ".join(fmt(d.get(l, {}).get(dom, {}).get("rate")) for l, _ in ARMS) + " |")

    e = tables["external"]
    lines += ["", "## External comparators (n=201)", "",
              "| Model | Pass@1 greedy | Pass@8 sampled |", "|---|---:|---:|"]
    for group in ("open_weights", "commercial_api"):
        for name, row in e[group].items():
            lines.append(f"| {name} | {fmt(row['pass_at_1_greedy'])} "
                         f"| {fmt(row.get('pass_at_8_sampled'))} |")
    rng = e["commercial_api_range"]
    lines.append("")
    lines.append(f"Commercial-API greedy Pass@1 range across {rng['n']} models: "
                 f"**{fmt(rng['min'],3)} to {fmt(rng['max'],3)}**.")

    g = tables["gemma"]
    lines += ["", "## Gemma-3-4B replication", "",
              "| Run | Arm | Pass@1 | Pass@8 | truth_classify | v2 strict |",
              "|---|---|---:|---:|---:|---:|"]
    for run in ("seed56", "seed24"):
        for arm in ("base", "sft", "dense", "sparse"):
            row = g.get(run, {}).get(arm)
            if not row:
                continue
            lines.append(f"| {run} | {arm} | {fmt(row.get('pass_at_1_greedy'))} "
                         f"| {fmt(row.get('pass_at_8_sampled'))} | {fmt(row.get('truth_classify'))} "
                         f"| {fmt(row.get('v2_strict'))} |")
    lines += ["", g["_note"]]

    a = tables["human_audit"]
    if "error" not in a:
        lines += ["", "## Human audit of verifier decisions", "",
                  f"- Audited decisions: **{a['n_total']}** "
                  f"({a['n_accepted_audited']} accepted, {a['n_rejected_audited']} rejected)",
                  f"- Accepted and confirmed valid: **{a['accepted_confirmed_valid']}/"
                  f"{a['n_accepted_audited']}** (false-accept rate {a['false_accept_rate']:.3f})",
                  f"- Rejected and confirmed invalid: **{a['rejected_confirmed_invalid']}/"
                  f"{a['n_rejected_audited']}**",
                  f"- Overall decision accuracy: **{a['decision_accuracy']:.4f}**"]

    lines += ["", "## Excluded runs", ""]
    for suite, why in EXCLUDED_SUITES.items():
        lines.append(f"- `{suite}` — {why}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs-root", default="runs",
                        help="directory containing eval/ (default: runs)")
    parser.add_argument("--audit-dir", default="human_eval",
                        help="directory containing the audit CSVs (default: human_eval)")
    parser.add_argument("--out-dir", default="paper_preparation/results",
                        help="where to write camera_ready_tables.{json,md}")
    parser.add_argument("--seed", default="42", help="reference seed for per-run tables")
    args = parser.parse_args()

    cells = Cells(args.runs_root)
    tables = {
        "main": table_main(cells, args.seed),
        "trap": table_trap(cells, args.seed),
        "multiseed": table_multiseed(cells),
        "ood": table_ood(cells),
        "reason": table_reason(cells, args.seed),
        "per_domain": table_per_domain(cells, args.seed),
        "external": table_external(cells),
        "gemma": table_gemma(cells),
        "human_audit": table_human_audit(args.audit_dir),
    }
    os.makedirs(args.out_dir, exist_ok=True)
    json_path = os.path.join(args.out_dir, "camera_ready_tables.json")
    md_path = os.path.join(args.out_dir, "camera_ready_tables.md")
    with open(json_path, "w") as fh:
        json.dump(tables, fh, indent=2, sort_keys=True)
    with open(md_path, "w") as fh:
        fh.write(render_markdown(tables))
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
