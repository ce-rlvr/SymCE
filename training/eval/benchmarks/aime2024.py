"""AIME 2024 benchmark — 30 problems with integer answers (0..999).

Several HF dataset mirrors exist; we try them in order. Each problem has a
unique integer answer in [0, 999], so we accept any of {integer match,
sympy equivalence, normalized string match}.
"""

from __future__ import annotations

import logging
from typing import Optional

from training.eval.benchmarks._answer_extract import (
    answers_equivalent,
    extract_boxed,
    extract_freeform_answer,
    normalize_math_string,
)
from training.eval.benchmarks.base import Benchmark, Problem, ScoredSample

logger = logging.getLogger(__name__)


_STANDARD_COT_SYSTEM = (
    "You are an expert at AIME-style competition problems. The answer to "
    "every AIME problem is an integer between 0 and 999. Reason step by step "
    "and put your final integer answer in \\boxed{}."
)

_V2_COUNTEREXAMPLE_SYSTEM = (
    "You are a mathematician evaluating a proposed conjecture.\n"
    "First, think through the problem step by step inside "
    "<reasoning> ... </reasoning> tags.\n"
    "Then, output a single line of the form:\n"
    "    [COUNTEREXAMPLE: <integer>]\n"
    "where <integer> is the final integer answer (0 to 999)."
)


_DATASET_CANDIDATES = [
    ("Maxwell-Jia/AIME_2024", None, "train", "Problem", "Answer", None),
    ("HuggingFaceH4/aime_2024", None, "train", "problem", "answer", None),
    ("AI-MO/aimo-validation-aime", None, "train", "problem", "answer", None),
]


class AIME2024Benchmark(Benchmark):
    name = "aime2024"
    supported_styles = ("standard_cot", "v2_counterexample")
    default_domain = "AIME"

    def load_problems(
        self, limit: Optional[int] = None, seed: int = 42,
    ) -> list[Problem]:
        try:
            from datasets import load_dataset
        except ImportError as e:
            raise RuntimeError("`datasets` is required. `pip install datasets`.") from e

        override = (self.cfg or {}).get("dataset")
        if override:
            candidates = [(
                override,
                (self.cfg or {}).get("subset"),
                (self.cfg or {}).get("split", "train"),
                (self.cfg or {}).get("question_field", "Problem"),
                (self.cfg or {}).get("answer_field", "Answer"),
                None,
            )]
        else:
            candidates = _DATASET_CANDIDATES

        ds = None
        chosen = None
        last_err = None
        for spec in candidates:
            ds_id, subset, split, q_field, a_field, _ = spec
            try:
                if subset:
                    ds = load_dataset(ds_id, subset, split=split)
                else:
                    ds = load_dataset(ds_id, split=split)
                chosen = spec
                logger.info("AIME2024: loaded %s (%d rows)", ds_id, len(ds))
                break
            except Exception as e:
                last_err = e
                logger.debug("AIME2024: failed to load %s: %s", ds_id, e)
                continue
        if ds is None or chosen is None:
            raise RuntimeError(
                f"AIME2024: could not load any candidate dataset; last error: {last_err}"
            )

        _, _, split, q_field, a_field, _ = chosen
        problems: list[Problem] = []
        for i, row in enumerate(ds):
            question = row.get(q_field) or row.get("question") or ""
            raw_answer = row.get(a_field)
            if raw_answer is None:
                continue
            gold = str(raw_answer).strip()
            problems.append(
                Problem(
                    id=f"aime2024_{i}",
                    question=question,
                    gold=gold,
                    domain=self.default_domain,
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
            user = f"{problem.question}\n\n(Final answer must be an integer 0..999.)"
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
        return extract_boxed(completion) or extract_freeform_answer(completion)

    def score(
        self, extracted: Optional[str], problem: Problem, completion: str,
    ) -> ScoredSample:
        # Try integer match first (most common for AIME); fall back to sympy.
        ok = False
        if extracted is not None:
            try:
                ok = int(normalize_math_string(extracted)) == int(problem.gold)
            except Exception:
                ok = answers_equivalent(extracted, problem.gold)
        return ScoredSample(
            completion=completion,
            extracted=extracted,
            correct=ok,
            score=1.0 if ok else 0.0,
            extra={"gold": problem.gold},
        )
