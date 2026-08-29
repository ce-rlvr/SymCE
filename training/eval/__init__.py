"""Evaluation harness package.

- ``training.eval.run_suite``: multi-model / multi-benchmark orchestrator,
  driven by a YAML config under ``configs/eval/``.
- ``training.eval.eval_runner``: legacy single-checkpoint CLI (kept for
  backwards compatibility; now delegates to the suite for the in-domain
  counterexample path).
- ``training.eval.backends``: thin Backend ABCs (vLLM, Unsloth, OpenAI,
  DeepSeek, Anthropic, Gemini).
- ``training.eval.benchmarks``: per-benchmark loaders + scorers
  (counterexample, gsm8k, math, aime2024, ...).
- ``training.eval.cache``: per-completion sqlite cache for re-scoring /
  resume / cross-run reuse.
"""
