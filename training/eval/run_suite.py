"""Multi-model / multi-benchmark eval orchestrator.

Driven by a YAML config under ``configs/eval/<name>.yaml``. Iterates over the
cartesian product (model × benchmark × prompt_style × sampling_pass) and
produces:

    runs/eval/<ts>__<suite_name>/
      ├── suite_config.yaml          # the resolved config used for this run
      ├── suite_summary.json         # the cross-cell summary
      ├── suite_summary.md           # human-friendly skim
      ├── per_cell/
      │   └── <model>__<benchmark>__<style>__<sampling>.json
      └── status.json + run_summary.md (per the runs/ convention)

A "cell" = one (model, benchmark, style, sampling-pass) tuple. Each cell
runs both:
- ``greedy``:  n_samples=1, temperature=0.0 → reports ``pass_at_1_greedy``
- ``sampled``: n_samples=N, temperature=T   → reports ``pass_at_{k}_sampled`` for each k

vLLM engines are reused across all cells that share the same model_id (we
load each model exactly once per suite run).

Usage:

    python -m training.eval.run_suite --config configs/eval/full_eval.yaml
    python -m training.eval.run_suite --config configs/eval/full_eval.yaml --only-models qwen-rlvr
    python -m training.eval.run_suite --config configs/eval/full_eval.yaml --only-benchmarks gsm8k,math
    python -m training.eval.run_suite --config configs/eval/full_eval.yaml --dry-run
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import yaml
from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from training.common.paths import REPO_ROOT  # noqa: E402
from training.common.run_dir import (  # noqa: E402
    RUNS_ROOT,
    finalise_run,
    write_run_metadata,
)
from training.eval.backends import build_backend, Backend, BackendSpec, GenerationRequest  # noqa: E402
from training.eval.benchmarks import get_benchmark  # noqa: E402
from training.eval.benchmarks.base import Benchmark, Problem  # noqa: E402
from training.eval.cache import get_cache  # noqa: E402
from training.eval.pass_at_k import (  # noqa: E402
    aggregate_pass_at_k,
    compute_pass_at_k_for_problem,
    filter_k_values,
    pass_at_k,
)

load_dotenv(REPO_ROOT / ".env")

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


# ─────────────────────────────────────────────────────────────────────────────
# Resolved-config dataclasses
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ModelConfig:
    name: str                          # short id used in result paths
    backend: str                       # vllm | unsloth | openai | deepseek | anthropic | gemini
    model_id: str                      # HF id / path / API model name
    model_type: str = "unknown"        # base | sft | rlvr | open_baseline | commercial
    enabled: bool = True
    lora_adapter: Optional[str] = None
    chat_template: str = "auto"
    # External-benchmark prompt-style override; "auto" = use benchmark default.
    external_prompt_style: str = "auto"
    # When True, run external benchmarks ALSO under v2_counterexample (in
    # addition to the auto/standard style). Used for SFT / RLVR to measure
    # the catastrophic-forgetting signal under the trained format.
    external_prompt_both: bool = False
    extra: dict = field(default_factory=dict)


@dataclass
class BenchmarkConfig:
    name: str
    enabled: bool = True
    prompt_style: str = "auto"
    prompt_styles: Optional[list[str]] = None
    limit: Optional[int] = None
    cfg: dict = field(default_factory=dict)


@dataclass
class SamplingConfig:
    n_samples: int
    temperature: float
    max_new_tokens: int = 1024
    top_p: float = 1.0


@dataclass
class SuiteConfig:
    suite_name: str
    models: list[ModelConfig]
    benchmarks: list[BenchmarkConfig]
    greedy: SamplingConfig
    sampled: SamplingConfig
    pass_at_k_values: list[int]
    backends: dict[str, dict]
    cache: dict
    seed: int = 42
    reward_workers: int = 8


def _load_suite_config(path: Path) -> SuiteConfig:
    with open(path) as fh:
        raw = yaml.safe_load(fh)
    models = [ModelConfig(**m) for m in raw["models"]]
    benchmarks = [BenchmarkConfig(**b) for b in raw["benchmarks"]]
    greedy = SamplingConfig(**raw["sampling"]["greedy"])
    sampled = SamplingConfig(**raw["sampling"]["sampled"])
    return SuiteConfig(
        suite_name=raw.get("suite_name", path.stem),
        models=models,
        benchmarks=benchmarks,
        greedy=greedy,
        sampled=sampled,
        pass_at_k_values=list(raw.get("pass_at_k_values", [1, 3, 5, 8])),
        backends=dict(raw.get("backends", {})),
        cache=dict(raw.get("cache", {"enabled": True, "path": "runs/eval_cache/cache.sqlite"})),
        seed=int(raw.get("seed", 42)),
        reward_workers=int(raw.get("reward_workers", 8)),
    )


def _build_backend_for_model(m: ModelConfig, backends_cfg: dict) -> Backend:
    """Build a Backend from a ModelConfig, merging backend defaults."""
    common = dict(backends_cfg.get(m.backend, {}))
    spec = BackendSpec(
        kind=m.backend,
        model_id=m.model_id,
        display_name=m.name,
        lora_adapter=m.lora_adapter,
        dtype=str(common.get("dtype", "bfloat16")),
        max_model_len=int(common.get("max_model_len", 4096)),
        gpu_memory_utilization=float(common.get("gpu_memory_utilization", 0.85)),
        tensor_parallel_size=int(common.get("tensor_parallel_size", 1)),
        trust_remote_code=bool(common.get("trust_remote_code", True)),
        chat_template=m.chat_template,
        api_key_env=common.get("env_var"),
        base_url=common.get("base_url"),
        max_concurrent_requests=int(common.get("max_concurrent_requests", 8)),
        request_timeout_seconds=float(common.get("request_timeout_seconds", 120.0)),
        max_retries=int(common.get("max_retries", 5)),
        extra=dict(m.extra),
    )
    return build_backend(spec)


# ─────────────────────────────────────────────────────────────────────────────
# One cell = (model, benchmark, style, sampling)
# ─────────────────────────────────────────────────────────────────────────────

def _run_cell(
    *,
    model_cfg: ModelConfig,
    backend: Backend,
    benchmark: Benchmark,
    benchmark_cfg: BenchmarkConfig,
    problems: list[Problem],
    style: str,
    sampling: SamplingConfig,
    sampling_label: str,        # "greedy" | "sampled"
    pass_at_k_values: list[int],
    seed: int,
    reward_workers: int,
) -> dict:
    """Run one cell and return its summary."""
    cell_id = f"{model_cfg.name}__{benchmark_cfg.name}__{style}__{sampling_label}"
    logger.info("── Cell: %s ──", cell_id)
    logger.info("  problems = %d, n_samples = %d, temperature = %.2f",
                len(problems), sampling.n_samples, sampling.temperature)

    # Build requests
    requests = [
        GenerationRequest(
            messages=benchmark.build_prompt(p, style),
            n_samples=sampling.n_samples,
            temperature=sampling.temperature,
            max_new_tokens=sampling.max_new_tokens,
            top_p=sampling.top_p,
            seed=seed + i,
            cache_key_extra=f"|style={style}",
        )
        for i, p in enumerate(problems)
    ]

    t0 = time.time()
    batch_results = backend.generate_batch(requests)
    elapsed_gen = time.time() - t0

    # Score (parallel across problems for the oracle path; CPU-bound)
    def _score_one(args):
        i, p, results = args
        gens = results
        # For greedy we may have collapsed N samples to 1 inside the backend.
        per_sample = []
        for g in gens:
            extracted = benchmark.extract_answer(g.text, p, style)
            scored = benchmark.score(extracted, p, g.text)
            per_sample.append({
                "completion": scored.completion,
                "extracted": scored.extracted,
                "correct": scored.correct,
                "score": scored.score,
                "cached": g.cached,
                "stop_reason": g.stop_reason,
                **scored.extra,
            })
        n_correct = sum(1 for s in per_sample if s["correct"])
        n_samples_effective = len(per_sample)
        return i, p, per_sample, n_correct, n_samples_effective

    per_record: list[dict] = []
    domain_totals: dict[str, dict] = defaultdict(lambda: {"n": 0, "n_correct_any": 0})
    n_problems = len(problems)

    t_score = time.time()
    # Use a single-threaded path for the counterexample benchmark because the
    # oracle already forks subprocesses; for the rest we can parallelize.
    use_workers = max(1, reward_workers) if benchmark.name != "counterexample" else 1
    if use_workers > 1:
        with ThreadPoolExecutor(max_workers=use_workers) as pool:
            results_iter = pool.map(
                _score_one,
                [(i, problems[i], batch_results[i]) for i in range(n_problems)],
            )
            scored = sorted(results_iter, key=lambda r: r[0])
    else:
        scored = [
            _score_one((i, problems[i], batch_results[i])) for i in range(n_problems)
        ]
    elapsed_score = time.time() - t_score

    # Aggregate
    eligible_k = filter_k_values(pass_at_k_values, sampling.n_samples)
    per_problem_passk: list[dict[int, float]] = []
    for i, p, per_sample, n_correct, n_eff in scored:
        passk = compute_pass_at_k_for_problem(n_eff, n_correct, eligible_k)
        per_problem_passk.append(passk)
        # Conclusion-pass: counterexample-specific bonus metric
        conclusion_pass = any(s.get("conclusion_pass") for s in per_sample) if benchmark.name == "counterexample" else False
        per_record.append({
            "problem_id": p.id,
            "domain": p.domain,
            "subset": (p.extra or {}).get("subset", "unknown"),
            "n_samples": n_eff,
            "n_correct": n_correct,
            "pass_at_k": passk,
            "any_correct": n_correct > 0,
            "conclusion_pass": conclusion_pass,
            "samples": per_sample,
        })
        domain = benchmark.per_domain_key(p)
        domain_totals[domain]["n"] += 1
        domain_totals[domain]["n_correct_any"] += int(n_correct > 0)

    aggregated = aggregate_pass_at_k(per_problem_passk, eligible_k)

    summary: dict[str, Any] = {
        "cell_id": cell_id,
        "model": model_cfg.name,
        "model_id": model_cfg.model_id,
        "model_type": model_cfg.model_type,
        "backend": model_cfg.backend,
        "benchmark": benchmark.name,
        "prompt_style": style,
        "sampling_label": sampling_label,
        "n_samples": sampling.n_samples,
        "temperature": sampling.temperature,
        "max_new_tokens": sampling.max_new_tokens,
        "n_problems": n_problems,
        "elapsed_generation_seconds": round(elapsed_gen, 1),
        "elapsed_scoring_seconds": round(elapsed_score, 1),
        "pass_at_k": {k: round(v, 4) for k, v in aggregated.items()},
        "by_domain": {
            d: {
                "n": v["n"],
                "any_correct_rate": round(v["n_correct_any"] / v["n"], 4) if v["n"] else 0.0,
            }
            for d, v in sorted(domain_totals.items())
        },
    }
    # Convenience aliases: pass_at_1_greedy / pass_at_{k}_sampled
    if sampling_label == "greedy":
        summary["pass_at_1_greedy"] = summary["pass_at_k"].get(1, 0.0)
    else:
        for k in eligible_k:
            summary[f"pass_at_{k}_sampled"] = summary["pass_at_k"][k]

    # counterexample-specific roll-up
    if benchmark.name == "counterexample":
        summary["conclusion_pass_rate"] = round(
            sum(1 for r in per_record if r["conclusion_pass"]) / max(1, n_problems), 4
        )
    if benchmark.name == "theorem_truth":
        def _sample_rate(records: list[dict], key: str) -> float:
            total = sum(len(r["samples"]) for r in records)
            if total == 0:
                return 0.0
            hits = sum(1 for r in records for s in r["samples"] if s.get(key))
            return round(hits / total, 4)

        summary["parse_ok_rate"] = _sample_rate(per_record, "parse_ok")
        summary["correct_rate"] = _sample_rate(per_record, "correct")

        subset_metrics: dict[str, dict[str, Any]] = {}
        subsets = sorted({r.get("subset", "unknown") for r in per_record})
        for subset in subsets:
            recs = [r for r in per_record if r.get("subset") == subset]
            subset_passk = aggregate_pass_at_k(
                [r["pass_at_k"] for r in recs], eligible_k
            )
            subset_metrics[subset] = {
                "n_problems": len(recs),
                "any_correct_rate": round(
                    sum(1 for r in recs if r["any_correct"]) / max(1, len(recs)), 4
                ),
                "parse_ok_rate": _sample_rate(recs, "parse_ok"),
                "correct_rate": _sample_rate(recs, "correct"),
                "pass_at_k": {k: round(v, 4) for k, v in subset_passk.items()},
            }
        summary["subset_metrics"] = subset_metrics

    return {"summary": summary, "per_record": per_record}


# ─────────────────────────────────────────────────────────────────────────────
# Top-level orchestration
# ─────────────────────────────────────────────────────────────────────────────

def _resolve_external_styles(model_cfg: ModelConfig, benchmark_cfg: BenchmarkConfig) -> list[str]:
    """Which prompt styles to run for (model, benchmark)?

    - For the counterexample benchmark, always use the benchmark's configured
      style (typically v2_counterexample).
    - For external benchmarks:
        * model.external_prompt_style overrides the benchmark default.
        * If model.external_prompt_both is True, also run v2_counterexample
          in addition to the standard style.
    """
    if benchmark_cfg.name in ("counterexample", "theorem_truth"):
        if benchmark_cfg.prompt_styles:
            return list(benchmark_cfg.prompt_styles)
        return [benchmark_cfg.prompt_style]

    if benchmark_cfg.prompt_styles:
        styles = list(benchmark_cfg.prompt_styles)
    else:
        styles = [model_cfg.external_prompt_style or benchmark_cfg.prompt_style]

    # Resolve "auto" to the benchmark's first supported style so cell labels
    # in dry-runs and per-cell JSONs reflect what was actually used.
    if "auto" in styles:
        try:
            BenchCls = get_benchmark(benchmark_cfg.name)
            default_style = BenchCls().supported_styles[0]
            styles = [default_style if s == "auto" else s for s in styles]
        except Exception:
            pass

    if model_cfg.external_prompt_both and "v2_counterexample" not in styles:
        styles.append("v2_counterexample")
    return styles


def run_suite(
    suite: SuiteConfig,
    *,
    only_models: Optional[set[str]] = None,
    only_benchmarks: Optional[set[str]] = None,
    dry_run: bool = False,
    out_dir: Optional[Path] = None,
) -> dict:
    # Initialize cache singleton
    cache_path = REPO_ROOT / suite.cache.get("path", "runs/eval_cache/cache.sqlite")
    get_cache(db_path=cache_path, enabled=bool(suite.cache.get("enabled", True)))

    enabled_models = [
        m for m in suite.models
        if m.enabled and (only_models is None or m.name in only_models)
    ]
    enabled_benchmarks = [
        b for b in suite.benchmarks
        if b.enabled and (only_benchmarks is None or b.name in only_benchmarks)
    ]
    if not enabled_models:
        raise ValueError("No models enabled in the suite (after filtering).")
    if not enabled_benchmarks:
        raise ValueError("No benchmarks enabled in the suite (after filtering).")

    logger.info("Suite: %s", suite.suite_name)
    logger.info("  models     = %s", [m.name for m in enabled_models])
    logger.info("  benchmarks = %s", [b.name for b in enabled_benchmarks])
    logger.info("  pass@k     = %s", suite.pass_at_k_values)
    if dry_run:
        return _dry_run_summary(suite, enabled_models, enabled_benchmarks)

    # Output directory
    if out_dir is None:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        out_dir = RUNS_ROOT / "eval" / f"{ts}__{suite.suite_name}__suite"
        out_dir.mkdir(parents=True, exist_ok=False)
    (out_dir / "per_cell").mkdir(exist_ok=True)

    # Stamp run metadata
    write_run_metadata(
        run_dir=out_dir,
        cfg=asdict_suite(suite),
        phase="eval",
        argv=sys.argv,
        extra={"suite_name": suite.suite_name, "kind": "eval_suite"},
    )
    # Save the resolved YAML for reproducibility
    (out_dir / "suite_config.yaml").write_text(yaml.safe_dump(asdict_suite(suite), sort_keys=False))

    # Pre-load problems once per benchmark (shared across all models)
    bench_objs: dict[str, Benchmark] = {}
    bench_problems: dict[str, list[Problem]] = {}
    for bc in enabled_benchmarks:
        BenchCls = get_benchmark(bc.name)
        b = BenchCls(cfg=bc.cfg)
        bench_objs[bc.name] = b
        problems = b.load_problems(limit=bc.limit, seed=suite.seed)
        bench_problems[bc.name] = problems
        # Per-domain counts for the user's "report domain sizes" request
        per_domain: dict[str, int] = defaultdict(int)
        for p in problems:
            per_domain[p.domain or "unknown"] += 1
        logger.info(
            "Loaded %s: %d problems  (per-domain: %s)",
            bc.name, len(problems), dict(per_domain),
        )

    # Iterate models × benchmarks × styles × sampling-passes
    all_cells: list[dict] = []
    suite_t0 = time.time()
    for m in enabled_models:
        logger.info("\n=== Model: %s (%s, %s) ===", m.name, m.model_id, m.backend)
        backend = _build_backend_for_model(m, suite.backends)
        try:
            for bc in enabled_benchmarks:
                bench = bench_objs[bc.name]
                problems = bench_problems[bc.name]
                styles = _resolve_external_styles(m, bc)
                for style in styles:
                    for sampling_label, sampling in [
                        ("greedy", suite.greedy), ("sampled", suite.sampled),
                    ]:
                        cell = _run_cell(
                            model_cfg=m,
                            backend=backend,
                            benchmark=bench,
                            benchmark_cfg=bc,
                            problems=problems,
                            style=style,
                            sampling=sampling,
                            sampling_label=sampling_label,
                            pass_at_k_values=suite.pass_at_k_values,
                            seed=suite.seed,
                            reward_workers=suite.reward_workers,
                        )
                        # Persist per-cell JSON
                        cell_path = out_dir / "per_cell" / f"{cell['summary']['cell_id']}.json"
                        with open(cell_path, "w") as fh:
                            json.dump(cell, fh, indent=2, default=str)
                        all_cells.append(cell["summary"])
        finally:
            backend.close()

    elapsed = time.time() - suite_t0

    # Suite-level aggregation
    per_domain_sizes = {
        bc.name: {
            d: sum(1 for p in bench_problems[bc.name] if (p.domain or "unknown") == d)
            for d in sorted({p.domain or "unknown" for p in bench_problems[bc.name]})
        }
        for bc in enabled_benchmarks
    }
    suite_summary = {
        "suite_name": suite.suite_name,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(elapsed, 1),
        "n_cells": len(all_cells),
        "models_run": [m.name for m in enabled_models],
        "benchmarks_run": [b.name for b in enabled_benchmarks],
        "pass_at_k_values": suite.pass_at_k_values,
        "per_benchmark_domain_sizes": per_domain_sizes,
        "cells": all_cells,
        "cache_stats": get_cache().stats(),
    }
    with open(out_dir / "suite_summary.json", "w") as fh:
        json.dump(suite_summary, fh, indent=2, default=str)
    _write_suite_markdown(out_dir, suite_summary, per_domain_sizes)

    finalise_run(out_dir, status="completed", extra={
        "suite_name": suite.suite_name,
        "n_cells": len(all_cells),
        "elapsed_seconds": round(elapsed, 1),
    })
    logger.info("\nSuite finished in %.1fs → %s", elapsed, out_dir)
    return suite_summary


def asdict_suite(suite: SuiteConfig) -> dict:
    """Convert SuiteConfig (with dataclass children) to plain dict."""
    return {
        "suite_name": suite.suite_name,
        "seed": suite.seed,
        "reward_workers": suite.reward_workers,
        "pass_at_k_values": suite.pass_at_k_values,
        "backends": suite.backends,
        "cache": suite.cache,
        "sampling": {
            "greedy": asdict(suite.greedy),
            "sampled": asdict(suite.sampled),
        },
        "models": [asdict(m) for m in suite.models],
        "benchmarks": [asdict(b) for b in suite.benchmarks],
    }


def _dry_run_summary(suite: SuiteConfig, models, benchmarks) -> dict:
    rows = []
    for m in models:
        for b in benchmarks:
            for style in _resolve_external_styles(m, b):
                for label in ("greedy", "sampled"):
                    rows.append({"model": m.name, "benchmark": b.name, "style": style, "pass": label})
    logger.info("Dry-run cells (%d):", len(rows))
    for r in rows:
        logger.info("  %s × %s × %s × %s", r["model"], r["benchmark"], r["style"], r["pass"])
    return {"dry_run_cells": rows}


def _write_suite_markdown(out_dir: Path, summary: dict, per_domain_sizes: dict) -> None:
    lines = [
        f"# Eval suite — {summary['suite_name']}",
        "",
        f"- **Elapsed**: {summary['elapsed_seconds']} s  •  **Cells**: {summary['n_cells']}",
        f"- **Models**: {', '.join(summary['models_run'])}",
        f"- **Benchmarks**: {', '.join(summary['benchmarks_run'])}",
        f"- **Pass@k**: {summary['pass_at_k_values']}",
        "",
        "## Per-benchmark domain sizes",
        "",
    ]
    for bench, doms in per_domain_sizes.items():
        lines.append(f"### {bench}")
        lines.append("")
        lines.append("| Domain | N |")
        lines.append("| --- | ---: |")
        for d, n in sorted(doms.items(), key=lambda kv: -kv[1]):
            lines.append(f"| `{d}` | {n} |")
        lines.append("")
    lines += [
        "## Results table (mean over problems)",
        "",
        "| Model | Benchmark | Style | Pass@1 (greedy) | Pass@1 (sampled) | Pass@3 | Pass@5 | Pass@8 |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    # Pair greedy + sampled cells for the same (model, bench, style)
    by_key: dict[tuple, dict] = {}
    for c in summary["cells"]:
        k = (c["model"], c["benchmark"], c["prompt_style"])
        by_key.setdefault(k, {})[c["sampling_label"]] = c
    for (model, bench, style), cells in sorted(by_key.items()):
        g = cells.get("greedy", {}).get("pass_at_k", {})
        s = cells.get("sampled", {}).get("pass_at_k", {})
        lines.append(
            f"| `{model}` | `{bench}` | `{style}` "
            f"| {g.get(1, 0.0):.3f} | {s.get(1, 0.0):.3f} "
            f"| {s.get(3, 0.0):.3f} | {s.get(5, 0.0):.3f} | {s.get(8, 0.0):.3f} |"
        )
    (out_dir / "suite_summary.md").write_text("\n".join(lines) + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Run a multi-model/multi-benchmark eval suite.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--config", required=True, help="Path to a configs/eval/<name>.yaml file.")
    p.add_argument("--only-models", default=None,
                   help="Comma-separated list of model.name to filter (default: all enabled).")
    p.add_argument("--only-benchmarks", default=None,
                   help="Comma-separated list of benchmark.name to filter.")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the cartesian of cells and exit.")
    p.add_argument("--out-dir", default=None,
                   help="Override run-dir location (default: runs/eval/<ts>__<suite>__suite/).")
    return p


def main():
    args = _build_parser().parse_args()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = REPO_ROOT / config_path
    suite = _load_suite_config(config_path)

    only_models = set(s.strip() for s in args.only_models.split(",")) if args.only_models else None
    only_benchmarks = set(s.strip() for s in args.only_benchmarks.split(",")) if args.only_benchmarks else None
    out_dir = Path(args.out_dir).resolve() if args.out_dir else None

    run_suite(
        suite,
        only_models=only_models,
        only_benchmarks=only_benchmarks,
        dry_run=args.dry_run,
        out_dir=out_dir,
    )


if __name__ == "__main__":
    main()
