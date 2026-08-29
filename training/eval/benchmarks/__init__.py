"""Benchmark loaders + scorers.

Each benchmark module subclasses :class:`Benchmark` from ``base.py`` and
declares:

- ``name``: stable string id (matches the YAML key).
- ``load_problems(limit, seed)``: returns a list of normalised problem dicts.
- ``build_prompt(problem, prompt_style)``: returns the [system, user] messages
  for that prompt style.
- ``extract_answer(completion)``: returns the canonical answer string (post-
  normalization), or ``None`` if no answer found.
- ``score(extracted, gold, problem)``: returns a bool (or float in [0,1]).
- ``per_domain_key(problem)``: returns the domain slug for breakdown stats.

Available prompt styles (subset depends on the benchmark):

- ``"standard_cot"`` — generic "solve and box the final answer" style.
- ``"v2_counterexample"`` — the in-domain [COUNTEREXAMPLE: ...] format
  (used by the in-domain counterexample benchmark, and on external benches
  for the SFT/RLVR models to measure regression under their trained format).
- ``"auto"`` — resolves to the benchmark's preferred default.

Available benchmarks:

- ``counterexample`` (in-domain): v2 oracle scoring against ``data/test_set_v2.jsonl``.
- ``theorem_truth`` (in-domain): true-theorem classification using ``data/theorem_truth_eval.jsonl``.
- ``gsm8k`` (external)
- ``math`` (external)
- ``aime2024`` (external)
"""

from training.eval.benchmarks.base import Benchmark, Problem
from training.eval.benchmarks.counterexample import CounterexampleBenchmark
from training.eval.benchmarks.gsm8k import GSM8KBenchmark
from training.eval.benchmarks.math_bench import MATHBenchmark
from training.eval.benchmarks.aime2024 import AIME2024Benchmark
from training.eval.benchmarks.theorem_truth import TheoremTruthBenchmark

BENCHMARK_REGISTRY: dict[str, type[Benchmark]] = {
    "counterexample": CounterexampleBenchmark,
  "theorem_truth": TheoremTruthBenchmark,
    "gsm8k": GSM8KBenchmark,
    "math": MATHBenchmark,
    "aime2024": AIME2024Benchmark,
}

# Optional opt-in benchmarks; lazy-imported in run_suite if enabled.
OPT_IN_BENCHMARKS = {
    "olympiad_math": "training.eval.benchmarks.olympiad_math:OlympiadMathBenchmark",
    "mmlu_college_math": "training.eval.benchmarks.mmlu_college_math:MMLUCollegeMathBenchmark",
}


def get_benchmark(name: str) -> type[Benchmark]:
    if name in BENCHMARK_REGISTRY:
        return BENCHMARK_REGISTRY[name]
    if name in OPT_IN_BENCHMARKS:
        mod_path, cls = OPT_IN_BENCHMARKS[name].split(":")
        import importlib
        return getattr(importlib.import_module(mod_path), cls)
    raise KeyError(f"Unknown benchmark: {name!r}. Known: {list(BENCHMARK_REGISTRY)}")


__all__ = ["Benchmark", "Problem", "get_benchmark", "BENCHMARK_REGISTRY"]
