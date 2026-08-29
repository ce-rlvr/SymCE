"""MMLU College Mathematics (Hendrycks et al. 2020).

Multiple-choice; gold answer is a letter A/B/C/D. Cheap (~100 problems) and
trivially scorable. Useful as a 'general college-math knowledge' check.

Opt-in: enable via ``benchmarks.mmlu_college_math.enabled: true`` in the YAML.
"""

from __future__ import annotations

import logging
import re
from typing import Optional

from training.eval.benchmarks.base import Benchmark, Problem, ScoredSample

logger = logging.getLogger(__name__)


_STANDARD_COT_SYSTEM = (
    "You are answering a multiple-choice math question. Reason step by step, "
    "then end with a single line: ``Final Answer: <letter>`` where <letter> "
    "is one of A, B, C, D."
)

_V2_COUNTEREXAMPLE_SYSTEM = (
    "You are a mathematician evaluating a multiple-choice question.\n"
    "First, reason inside <reasoning> ... </reasoning>.\n"
    "Then output a single line of the form:\n"
    "    [COUNTEREXAMPLE: <letter>]\n"
    "where <letter> is one of A, B, C, D."
)

_LETTER_PATTERN = re.compile(r"\b([ABCD])\b")
_FINAL_LETTER = re.compile(r"(?i)final\s*answer\s*[:=]\s*([ABCD])")
_LETTER_PARENS = re.compile(r"\(([ABCD])\)")


class MMLUCollegeMathBenchmark(Benchmark):
    name = "mmlu_college_math"
    supported_styles = ("standard_cot", "v2_counterexample")
    default_domain = "college_math"

    def load_problems(
        self, limit: Optional[int] = None, seed: int = 42,
    ) -> list[Problem]:
        try:
            from datasets import load_dataset
        except ImportError as e:
            raise RuntimeError("`datasets` is required. `pip install datasets`.") from e
        # The cais/mmlu mirror has per-subject splits.
        ds = load_dataset("cais/mmlu", "college_mathematics", split="test")
        problems: list[Problem] = []
        letter_map = ["A", "B", "C", "D"]
        for i, row in enumerate(ds):
            choices = row["choices"]
            choice_block = "\n".join(f"{letter_map[j]}. {c}" for j, c in enumerate(choices))
            question = f"{row['question']}\n\n{choice_block}"
            gold = letter_map[int(row["answer"])]
            problems.append(
                Problem(
                    id=f"mmlu_cm_{i}",
                    question=question,
                    gold=gold,
                    domain=self.default_domain,
                    extra={"choices": choices},
                )
            )
        if limit is not None:
            problems = problems[:limit]
        return problems

    def build_prompt(self, problem: Problem, prompt_style: str) -> list[dict]:
        style = self.resolve_style(prompt_style)
        system = _V2_COUNTEREXAMPLE_SYSTEM if style == "v2_counterexample" else _STANDARD_COT_SYSTEM
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": problem.question},
        ]

    def extract_answer(self, completion: str, problem: Problem, prompt_style: str) -> Optional[str]:
        style = self.resolve_style(prompt_style)
        if style == "v2_counterexample":
            from training.rlvr.reward_oracle import parse_counterexample_tag
            parsed = parse_counterexample_tag(completion)
            if parsed.payload:
                m = _LETTER_PATTERN.search(parsed.payload.upper())
                if m:
                    return m.group(1)
        # Prefer the explicit "Final Answer: X" pattern; otherwise look for
        # the last standalone letter in the response.
        m = _FINAL_LETTER.search(completion)
        if m:
            return m.group(1).upper()
        m_par = list(_LETTER_PARENS.finditer(completion))
        if m_par:
            return m_par[-1].group(1).upper()
        matches = list(_LETTER_PATTERN.finditer(completion.upper()))
        if matches:
            return matches[-1].group(1)
        return None

    def score(
        self, extracted: Optional[str], problem: Problem, completion: str,
    ) -> ScoredSample:
        ok = bool(extracted) and extracted.upper().strip() == problem.gold.upper().strip()
        return ScoredSample(
            completion=completion,
            extracted=extracted,
            correct=ok,
            score=1.0 if ok else 0.0,
            extra={"gold": problem.gold},
        )
