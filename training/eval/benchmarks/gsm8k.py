"""GSM8K benchmark (Cobbe et al. 2021).

Loaded via ``datasets.load_dataset("gsm8k", "main", split="test")``. 1319
grade-school math word problems with numeric answers in the ``#### <n>``
final-line format.
"""

from __future__ import annotations

import logging
import re
from typing import Optional

from training.eval.benchmarks._answer_extract import (
    answers_equivalent,
    extract_boxed,
    extract_freeform_answer,
    extract_gsm_final,
    normalize_math_string,
)
from training.eval.benchmarks.base import Benchmark, Problem, ScoredSample

logger = logging.getLogger(__name__)


_STANDARD_COT_SYSTEM = (
    "You are an expert at solving grade-school math word problems. Reason "
    "step by step, then end with a single line of the form: "
    "Final Answer: <number>"
)

_V2_COUNTEREXAMPLE_SYSTEM = (
    # Identical to the V2 training prompt. Lets us test whether the RLVR
    # model has regressed on general math when forced to use its trained
    # output contract.
    "You are a mathematician evaluating a proposed conjecture.\n"
    "First, think through the conjecture step by step inside "
    "<reasoning> ... </reasoning> tags.\n"
    "Then, output a single line of the form:\n"
    "    [COUNTEREXAMPLE: <expression>]\n"
    "where <expression> is the final numeric answer."
)


class GSM8KBenchmark(Benchmark):
    name = "gsm8k"
    supported_styles = ("standard_cot", "v2_counterexample")
    default_domain = "arithmetic"

    def load_problems(
        self, limit: Optional[int] = None, seed: int = 42,
    ) -> list[Problem]:
        try:
            from datasets import load_dataset
        except ImportError as e:
            raise RuntimeError(
                "`datasets` is required for the gsm8k benchmark. "
                "`pip install datasets`."
            ) from e
        split = (self.cfg or {}).get("split", "test")
        subset = (self.cfg or {}).get("subset", "main")
        ds = load_dataset("gsm8k", subset, split=split)
        problems: list[Problem] = []
        for i, row in enumerate(ds):
            gold = extract_gsm_final(row["answer"]) or row["answer"].split("####")[-1].strip()
            problems.append(
                Problem(
                    id=f"gsm8k_{split}_{i}",
                    question=row["question"],
                    gold=gold,
                    domain=self.default_domain,
                    extra={"raw_answer": row["answer"]},
                )
            )
        if limit is not None:
            problems = problems[:limit]
        return problems

    def build_prompt(self, problem: Problem, prompt_style: str) -> list[dict]:
        style = self.resolve_style(prompt_style)
        if style == "v2_counterexample":
            system = _V2_COUNTEREXAMPLE_SYSTEM
            user = (
                f"{problem.question}\n\n"
                "(Solve this problem and put the final numeric answer inside "
                "the [COUNTEREXAMPLE: ...] tag.)"
            )
        else:
            system = _STANDARD_COT_SYSTEM
            user = problem.question
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]

    def extract_answer(
        self, completion: str, problem: Problem, prompt_style: str
    ) -> Optional[str]:
        # Try the most specific extractor first, given the prompt style.
        style = self.resolve_style(prompt_style)
        if style == "v2_counterexample":
            from training.rlvr.reward_oracle import parse_counterexample_tag
            parsed = parse_counterexample_tag(completion)
            if parsed.payload and not parsed.is_none:
                return parsed.payload
        return (
            extract_boxed(completion)
            or extract_gsm_final(completion)
            or extract_freeform_answer(completion)
        )

    def score(
        self, extracted: Optional[str], problem: Problem, completion: str,
    ) -> ScoredSample:
        ok = answers_equivalent(extracted, problem.gold)
        return ScoredSample(
            completion=completion,
            extracted=extracted,
            correct=ok,
            score=1.0 if ok else 0.0,
            extra={
                "gold": problem.gold,
                "extracted_normalized": normalize_math_string(extracted) if extracted else None,
            },
        )
