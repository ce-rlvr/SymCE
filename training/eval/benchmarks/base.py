"""Benchmark ABC + shared types."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Problem:
    """Normalized benchmark problem.

    - ``id``: stable identifier (used for caching + result rows).
    - ``question``: the natural-language problem statement.
    - ``gold``: the reference answer (string; benchmarks normalise as needed).
    - ``domain``: optional sub-category (e.g. MATH subject; counterexample domain).
    - ``extra``: per-benchmark fields (e.g. v2 verifier_module_path).
    """
    id: str
    question: str
    gold: str
    domain: Optional[str] = None
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class ScoredSample:
    """One scored completion for one problem."""
    completion: str
    extracted: Optional[str]
    correct: bool
    score: float = 0.0          # finer-grained reward when applicable (oracle)
    extra: dict[str, Any] = field(default_factory=dict)


class Benchmark(ABC):
    """Abstract benchmark. Concrete subclasses live in this package."""

    #: Stable id used in YAML configs and result paths.
    name: str = "unset"
    #: Prompt styles this benchmark knows how to render. ``auto`` is always
    #: supported (resolves to the first listed real style).
    supported_styles: tuple[str, ...] = ("standard_cot",)
    #: Domain key for the per-domain breakdown.
    default_domain: str = "general"

    def __init__(self, cfg: Optional[dict] = None):
        self.cfg = cfg or {}

    @abstractmethod
    def load_problems(
        self, limit: Optional[int] = None, seed: int = 42,
    ) -> list[Problem]:
        ...

    def resolve_style(self, style: str) -> str:
        """Resolve ``auto`` -> first supported style; validate everything else."""
        if style == "auto":
            return self.supported_styles[0]
        if style not in self.supported_styles:
            raise ValueError(
                f"Benchmark {self.name} does not support prompt_style={style!r}. "
                f"Known: {self.supported_styles}"
            )
        return style

    @abstractmethod
    def build_prompt(self, problem: Problem, prompt_style: str) -> list[dict]:
        """Return the messages list ([system, user]) for the chosen style."""

    @abstractmethod
    def extract_answer(self, completion: str, problem: Problem, prompt_style: str) -> Optional[str]:
        """Normalize the model output to a comparable answer string.

        Returns ``None`` if no answer could be extracted (counts as incorrect).
        """

    @abstractmethod
    def score(
        self, extracted: Optional[str], problem: Problem, completion: str,
    ) -> ScoredSample:
        """Compare the extracted answer to the gold answer.

        Some benchmarks (counterexample) score via the oracle and don't rely
        purely on ``extracted``; they may use ``completion`` directly.
        """

    def per_domain_key(self, problem: Problem) -> str:
        return problem.domain or self.default_domain
