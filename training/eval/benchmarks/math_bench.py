"""MATH benchmark (Hendrycks et al. 2021).

Loaded via ``datasets.load_dataset`` - by default tries the modern
``HuggingFaceH4/MATH-500`` (a curated 500-problem test split) first, since
the original ``hendrycks/competition_math`` was taken down. The user can
override the dataset id in the YAML config.
"""

from __future__ import annotations

import logging
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
    "You are an expert mathematician. Solve the following problem. Reason "
    "step by step and put the final answer in \\boxed{}."
)

_V2_COUNTEREXAMPLE_SYSTEM = (
    "You are a mathematician evaluating a proposed conjecture.\n"
    "First, think through the conjecture step by step inside "
    "<reasoning> ... </reasoning> tags.\n"
    "Then, output a single line of the form:\n"
    "    [COUNTEREXAMPLE: <expression>]\n"
    "where <expression> is the final answer to the problem."
)


# Try these dataset specs in order until one loads. Allows local override.
_DEFAULT_DATASET_CANDIDATES = [
    # (id, config_or_None, split, question_field, answer_field, subject_field)
    ("HuggingFaceH4/MATH-500", None, "test", "problem", "answer", "subject"),
    ("lighteval/MATH", "all", "test", "problem", "solution", "type"),
    ("hendrycks/competition_math", None, "test", "problem", "solution", "type"),
]


class MATHBenchmark(Benchmark):
    name = "math"
    supported_styles = ("standard_cot", "v2_counterexample")
    default_domain = "MATH"

    def load_problems(
        self, limit: Optional[int] = None, seed: int = 42,
    ) -> list[Problem]:
        try:
            from datasets import load_dataset
        except ImportError as e:
            raise RuntimeError(
                "`datasets` is required for the MATH benchmark. "
                "`pip install datasets`."
            ) from e

        # User-specified override
        override = (self.cfg or {}).get("dataset")
        if override:
            candidates = [(
                override,
                (self.cfg or {}).get("subset"),
                (self.cfg or {}).get("split", "test"),
                (self.cfg or {}).get("question_field", "problem"),
                (self.cfg or {}).get("answer_field", "answer"),
                (self.cfg or {}).get("subject_field", "subject"),
            )]
        else:
            candidates = _DEFAULT_DATASET_CANDIDATES

        ds = None
        chosen = None
        last_err = None
        for spec in candidates:
            ds_id, subset, split, q_field, a_field, s_field = spec
            try:
                if subset:
                    ds = load_dataset(ds_id, subset, split=split)
                else:
                    ds = load_dataset(ds_id, split=split)
                chosen = spec
                logger.info("MATH: loaded %s (split=%s, %d rows)", ds_id, split, len(ds))
                break
            except Exception as e:
                last_err = e
                logger.debug("MATH: failed to load %s: %s", ds_id, e)
                continue
        if ds is None or chosen is None:
            raise RuntimeError(
                f"MATH: could not load any candidate dataset; last error: {last_err}"
            )

        _, _, split, q_field, a_field, s_field = chosen
        problems: list[Problem] = []
        for i, row in enumerate(ds):
            question = row.get(q_field, "")
            raw_answer = row.get(a_field, "")
            # Some sources store the full solution; extract the boxed answer.
            gold = extract_boxed(raw_answer) or extract_freeform_answer(raw_answer) or str(raw_answer).strip()
            subject = row.get(s_field, self.default_domain) if s_field else self.default_domain
            problems.append(
                Problem(
                    id=f"math_{split}_{i}",
                    question=question,
                    gold=gold,
                    domain=str(subject),
                    extra={"raw_answer": raw_answer},
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
                "(Put the final answer inside the [COUNTEREXAMPLE: ...] tag.)"
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
        style = self.resolve_style(prompt_style)
        if style == "v2_counterexample":
            from training.rlvr.reward_oracle import parse_counterexample_tag
            parsed = parse_counterexample_tag(completion)
            if parsed.payload and not parsed.is_none:
                return parsed.payload
        return (
            extract_boxed(completion)
            or extract_freeform_answer(completion)
            or extract_gsm_final(completion)
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
                "subject": problem.domain,
            },
        )
