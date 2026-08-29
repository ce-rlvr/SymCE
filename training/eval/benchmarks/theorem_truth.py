"""Theorem-truth classification benchmark.

Evaluates whether models can identify *true* theorems as true under two
prompt styles:
- v2_counterexample: use the standard counterexample prompt and expect
  [COUNTEREXAMPLE: NONE] or an empty tag.
- truth_classify: explicitly ask for TRUE/FALSE classification.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Optional

from training.common.paths import REPO_ROOT
from training.common.prompts import V2_SYSTEM_PROMPT
from training.eval.benchmarks.base import Benchmark, Problem, ScoredSample

logger = logging.getLogger(__name__)

_TRUTH_SYSTEM = (
    "You are a mathematician checking whether a conjecture is TRUE or FALSE.\n"
    "Reason if needed. Then output a single line:\n"
    "    Answer: TRUE\n"
    "or\n"
    "    Answer: FALSE\n"
    "Answer TRUE if the theorem is correct; answer FALSE if it is not."
)

_TRUTH_PATTERNS = [
    re.compile(r"(?i)final\s*answer\s*[:=]\s*(true|false)"),
    re.compile(r"(?i)answer\s*[:=]\s*(true|false)"),
]
_TRUTH_ANY = re.compile(r"\b(true|false)\b", re.IGNORECASE)


def _build_claim(record: dict) -> str:
    hyps = record.get("remaining_hypotheses") or record.get("hypotheses") or []
    conclusion = record.get("conclusion") or ""
    if hyps and conclusion:
        bulleted = "\n  - ".join(hyps)
        return (
            "Claim: For all mathematical objects satisfying:\n"
            f"  - {bulleted}\n"
            "the following conclusion holds:\n"
            f"  {conclusion}"
        )
    return (record.get("original_full_statement") or "").strip()


@dataclass(frozen=True)
class ParsedTruthTag:
    payload: Optional[str]
    format_ok: bool
    is_none: bool
    is_empty: bool


def _try_extract_tag(text: str, opener_idx: int) -> Optional[str]:
    n = len(text)
    colon = opener_idx + len("[COUNTEREXAMPLE:") - 1
    depth = 1
    i = colon + 1
    while i < n:
        c = text[i]
        if c == "\n":
            return None
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return text[colon + 1 : i]
        i += 1
    return None


def _parse_counterexample_relaxed(text: str) -> ParsedTruthTag:
    if not isinstance(text, str) or not text:
        return ParsedTruthTag(payload=None, format_ok=False, is_none=False, is_empty=False)
    opener_positions = [m.start() for m in re.finditer(r"\[COUNTEREXAMPLE:", text, re.IGNORECASE)]
    if not opener_positions:
        return ParsedTruthTag(payload=None, format_ok=False, is_none=False, is_empty=False)
    for opener_idx in reversed(opener_positions):
        raw = _try_extract_tag(text, opener_idx)
        if raw is None:
            continue
        payload = raw.strip()
        if payload == "":
            return ParsedTruthTag(payload="", format_ok=True, is_none=False, is_empty=True)
        is_none = payload.lower() == "none"
        return ParsedTruthTag(payload=payload, format_ok=True, is_none=is_none, is_empty=False)
    return ParsedTruthTag(payload=None, format_ok=False, is_none=False, is_empty=False)


def _parse_truth_label(text: str) -> Optional[str]:
    if not text:
        return None
    for pat in _TRUTH_PATTERNS:
        matches = list(pat.finditer(text))
        if matches:
            return matches[-1].group(1).upper()
    matches = list(_TRUTH_ANY.finditer(text))
    if matches:
        return matches[-1].group(1).upper()
    return None


class TheoremTruthBenchmark(Benchmark):
    name = "theorem_truth"
    supported_styles = ("v2_counterexample", "truth_classify")
    default_domain = "Unknown"

    def __init__(self, cfg: Optional[dict] = None):
        super().__init__(cfg)
        self.test_file = (self.cfg or {}).get("test_file", "data/theorem_truth_eval.jsonl")
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
                tid = rec.get("theorem_id") or f"rec_{len(problems)}"
                self._records[tid] = rec
                problems.append(
                    Problem(
                        id=tid,
                        question=_build_claim(rec),
                        gold="TRUE",
                        domain=rec.get("domain") or self.default_domain,
                        extra={
                            "subset": rec.get("subset", "unknown"),
                            "in_test_set": bool(rec.get("in_test_set")),
                        },
                    )
                )
        if limit is not None:
            problems = problems[:limit]
        return problems

    def build_prompt(self, problem: Problem, prompt_style: str) -> list[dict]:
        style = self.resolve_style(prompt_style)
        system = V2_SYSTEM_PROMPT if style == "v2_counterexample" else _TRUTH_SYSTEM
        return [
            {"role": "system", "content": system},
            {"role": "user", "content": problem.question},
        ]

    def extract_answer(self, completion: str, problem: Problem, prompt_style: str) -> Optional[str]:
        style = self.resolve_style(prompt_style)
        if style == "v2_counterexample":
            parsed = _parse_counterexample_relaxed(completion)
            return parsed.payload
        return _parse_truth_label(completion)

    def score(
        self, extracted: Optional[str], problem: Problem, completion: str,
    ) -> ScoredSample:
        parsed = _parse_counterexample_relaxed(completion)
        if parsed.format_ok or re.search(r"\[COUNTEREXAMPLE:", completion, re.IGNORECASE):
            predicted_true = parsed.format_ok and (parsed.is_none or parsed.is_empty)
            correct = predicted_true
            return ScoredSample(
                completion=completion,
                extracted=parsed.payload,
                correct=correct,
                score=1.0 if correct else 0.0,
                extra={
                    "parse_ok": parsed.format_ok,
                    "predicted_true": predicted_true,
                    "is_none": parsed.is_none,
                    "is_empty": parsed.is_empty,
                    "payload": parsed.payload,
                },
            )
        label = _parse_truth_label(completion)
        predicted_true = bool(label) and label.upper() == "TRUE"
        correct = predicted_true
        return ScoredSample(
            completion=completion,
            extracted=label,
            correct=correct,
            score=1.0 if correct else 0.0,
            extra={
                "parse_ok": bool(label),
                "predicted_true": predicted_true,
                "label": label,
            },
        )