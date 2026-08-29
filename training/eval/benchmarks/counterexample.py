"""In-domain v2 counterexample benchmark.

Loads ``data/test_set_v2.jsonl`` (or whatever ``test_file`` is configured),
builds the leakage-free user prompt via ``training.common.prompts``, and
scores each completion through the independent per-theorem verifier via
``compute_reward_oracle``. "Correct" = strict success (q_neg=1 AND all
remaining hypotheses satisfied).
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Optional

from training.common.paths import REPO_ROOT
from training.common.prompts import V2_SYSTEM_PROMPT, build_v2_user_message
from training.eval.benchmarks.base import Benchmark, Problem, ScoredSample
from training.rlvr.reward_oracle import (
    ORACLE_REWARD_WEIGHTS_DEFAULT,
    compute_reward_oracle,
    parse_counterexample_tag,
)

logger = logging.getLogger(__name__)

# Generic CoT prompt for "external" comparability — used when this benchmark
# is invoked with prompt_style=standard_cot (rare; mostly here for symmetry).
_STANDARD_COT_SYSTEM = (
    "You are an expert mathematician. Reason carefully about the proposed "
    "conjecture. If you believe it is false, present a counterexample with "
    "justification. Put your final answer in the form "
    "[COUNTEREXAMPLE: <expression>] at the end (or [COUNTEREXAMPLE: NONE] if "
    "you believe no counterexample exists)."
)


class CounterexampleBenchmark(Benchmark):
    name = "counterexample"
    # v2_counterexample is the canonical training-aligned prompt; standard_cot
    # is the variant we'd use to compare against general-purpose models.
    supported_styles = ("v2_counterexample", "standard_cot")
    default_domain = "Unknown"

    def __init__(self, cfg: Optional[dict] = None):
        super().__init__(cfg)
        self.test_file = (self.cfg or {}).get("test_file", "data/test_set_v2.jsonl")
        self.drop_unusable = bool((self.cfg or {}).get("drop_unusable", True))
        self.oracle_timeout = float((self.cfg or {}).get("oracle_timeout", 8.0))
        self.oracle_weights = (self.cfg or {}).get("oracle_weights") or dict(
            ORACLE_REWARD_WEIGHTS_DEFAULT
        )
        # Cached records keyed by Problem.id so score() can fetch them.
        self._records: dict[str, dict] = {}

    def load_problems(
        self, limit: Optional[int] = None, seed: int = 42,
    ) -> list[Problem]:
        test_path = REPO_ROOT / self.test_file
        if not test_path.exists():
            raise FileNotFoundError(f"Test file not found: {test_path}")
        problems: list[Problem] = []
        with open(test_path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if self.drop_unusable:
                    if rec.get("migration_failed") is True:
                        continue
                    if rec.get("witness_passes_verifier") is False:
                        continue
                tid = rec.get("theorem_id") or f"rec_{len(problems)}"
                prob_id = f"{tid}__{rec.get('dropped_hypothesis_name', 'x')}"
                self._records[prob_id] = rec
                problems.append(
                    Problem(
                        id=prob_id,
                        question=build_v2_user_message(rec),
                        gold=str(rec.get("canonical_witness", "")),
                        domain=rec.get("domain") or self.default_domain,
                        extra={
                            "verifier_module_path": (rec.get("verifier") or {}).get("module_path"),
                            "n_hyp": (rec.get("verifier") or {}).get("n_hyp"),
                            "neg_q_index": (rec.get("verifier") or {}).get("neg_q_index"),
                        },
                    )
                )
        if limit is not None:
            problems = problems[:limit]
        return problems

    def build_prompt(self, problem: Problem, prompt_style: str) -> list[dict]:
        style = self.resolve_style(prompt_style)
        system = V2_SYSTEM_PROMPT if style == "v2_counterexample" else _STANDARD_COT_SYSTEM
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": problem.question},
        ]

    def extract_answer(self, completion: str, problem: Problem, prompt_style: str) -> Optional[str]:
        parsed = parse_counterexample_tag(completion)
        if parsed.payload is None:
            return None
        return parsed.payload

    def score(
        self, extracted: Optional[str], problem: Problem, completion: str,
    ) -> ScoredSample:
        record = self._records.get(problem.id)
        if record is None:
            return ScoredSample(
                completion=completion, extracted=extracted, correct=False, score=0.0,
                extra={"reason": "missing_record"},
            )
        bd = compute_reward_oracle(
            record=record,
            completion_text=completion,
            weights=self.oracle_weights,
            task_mode="counterexample_only",
            timeout_seconds=self.oracle_timeout,
        )
        return ScoredSample(
            completion=completion,
            extracted=bd.witness_expr,
            correct=(bd.reason == "success"),
            score=float(bd.total),
            extra={
                "reason": bd.reason,
                "format_ok": bd.format_ok,
                "parse_ok": bd.parse_ok,
                "is_none": bd.is_none,
                "q_neg": bd.q_neg,
                "s_hyp": bd.s_hyp,
                "n_hyp": bd.n_hyp,
                "n_conditions": bd.n_conditions,
                "oracle_error": bd.oracle_error,
                "oracle_timed_out": bd.oracle_timed_out,
                "oracle_elapsed_ms": bd.oracle_elapsed_ms,
                "conclusion_pass": bool(bd.q_neg == 1),
            },
        )
