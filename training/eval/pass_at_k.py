"""Pass@K helpers.

The unbiased Pass@K estimator (Chen et al. 2021, "Evaluating LLMs Trained on
Code") is:

    pass@k = 1 - C(n - c, k) / C(n, k)

where ``n`` is the number of samples, ``c`` is the number of correct samples,
and ``k`` is the cutoff. When ``n - c < k`` the formula degenerates to 1.0.

Two reporting modes are used in this codebase per the user's choice:

- **Greedy** (n=1, T=0.0): one Pass@1 number; reported as ``pass_at_1_greedy``.
- **Sampled** (n=N, T>0): Pass@1/3/5/8 (or any subset) reported as
  ``pass_at_{k}_sampled`` for ``k <= N``. ``pass_at_1_sampled`` is the mean
  per-sample correctness, distinct from the greedy number.
"""

from __future__ import annotations

from math import comb
from typing import Iterable


def pass_at_k(n: int, c: int, k: int) -> float:
    """Unbiased pass@k estimator. n=#samples, c=#correct, k=cutoff."""
    if k <= 0:
        raise ValueError(f"k must be positive, got {k}")
    if n <= 0:
        return 0.0
    if c >= n:
        return 1.0
    if n - c < k:
        return 1.0
    if k > n:
        # Fall back to the empirical "any of n was correct" rate, which is
        # what pass@n would compute.
        k = n
    return 1.0 - comb(n - c, k) / comb(n, k)


def compute_pass_at_k_for_problem(
    n_samples: int, n_correct: int, k_values: Iterable[int]
) -> dict[int, float]:
    """Per-problem Pass@k for multiple k. Skips k > n_samples (records 0.0)."""
    out: dict[int, float] = {}
    for k in k_values:
        if k > n_samples:
            # The user might pass k=8 with n_samples=4 — we mark these as None
            # in the aggregator; record 0.0 here so the dict shape is uniform.
            out[k] = 0.0
        else:
            out[k] = pass_at_k(n_samples, n_correct, k)
    return out


def aggregate_pass_at_k(
    per_problem: list[dict[int, float]], k_values: Iterable[int]
) -> dict[int, float]:
    """Mean Pass@k across problems."""
    n = len(per_problem)
    if n == 0:
        return {k: 0.0 for k in k_values}
    out: dict[int, float] = {}
    for k in k_values:
        out[k] = sum(p.get(k, 0.0) for p in per_problem) / n
    return out


def filter_k_values(k_values: Iterable[int], n_samples: int) -> list[int]:
    """Keep only k <= n_samples (so we don't report meaningless numbers)."""
    return sorted({int(k) for k in k_values if 1 <= int(k) <= n_samples})
