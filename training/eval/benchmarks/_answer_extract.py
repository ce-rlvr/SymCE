"""Shared answer extraction + normalization for math benchmarks.

Two layers of matching:

1. Surface-level extraction:
   - ``\\boxed{...}`` for MATH / AIME / Olympiad-style prompts;
   - ``#### <answer>`` for GSM8K (the dataset's gold format);
   - "Final Answer: ..." / "The answer is ..." for free-form CoT fallback.

2. Numeric / sympy equivalence:
   - Strip commas, dollar signs, percent signs.
   - Try ``sympy.simplify(a - b) == 0`` for symbolic equivalence (handles
     ``1/2`` vs ``0.5``, ``\\frac{1}{2}`` vs ``1/2``, etc.).
   - Fall back to string compare.

These are deliberately tolerant; the standard MATH / GSM8K evaluation scripts
(e.g. lm-evaluation-harness) use very similar heuristics.
"""

from __future__ import annotations

import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)


_BOXED_PATTERNS = [
    re.compile(r"\\boxed\s*{"),
    re.compile(r"\\boxed\s+"),
]


def extract_boxed(text: str) -> Optional[str]:
    """Find the last ``\\boxed{...}`` content in text (brace-balanced)."""
    if not text:
        return None
    # We want the *last* boxed expression — final answer typically.
    last_match: Optional[str] = None
    for pat in _BOXED_PATTERNS:
        for m in pat.finditer(text):
            start = m.end()
            if text[m.start():m.end()].rstrip().endswith("{"):
                depth = 1
                i = start
                while i < len(text) and depth > 0:
                    c = text[i]
                    if c == "{":
                        depth += 1
                    elif c == "}":
                        depth -= 1
                        if depth == 0:
                            last_match = text[start:i]
                            break
                    i += 1
            else:
                # ``\boxed answer`` (no braces) — take the rest of the line.
                line_end = text.find("\n", start)
                last_match = text[start:(line_end if line_end != -1 else len(text))].strip()
    return last_match.strip() if last_match is not None else None


_GSM_FINAL = re.compile(r"####\s*([^\n]+)")
_ANSWER_PATTERNS = [
    re.compile(r"(?i)final\s*answer\s*[:=]\s*([^\n]+)"),
    re.compile(r"(?i)the\s*answer\s*is\s*[:=]?\s*([^\n.]+)"),
    re.compile(r"(?i)answer\s*[:=]\s*([^\n]+)"),
]


def extract_gsm_final(text: str) -> Optional[str]:
    """GSM8K reference format: ``#### <answer>`` at end of solution."""
    if not text:
        return None
    matches = list(_GSM_FINAL.finditer(text))
    if matches:
        return matches[-1].group(1).strip()
    return None


def extract_freeform_answer(text: str) -> Optional[str]:
    """Catch-all for 'Final Answer:' / 'The answer is' patterns."""
    if not text:
        return None
    best: Optional[str] = None
    best_pos = -1
    for pat in _ANSWER_PATTERNS:
        for m in pat.finditer(text):
            if m.start() > best_pos:
                best = m.group(1).strip()
                best_pos = m.start()
    return best


def extract_math_answer(text: str) -> Optional[str]:
    """Standard MATH / AIME extraction: boxed > Final Answer > GSM-style.

    Returns the raw extracted string (no normalization).
    """
    return (
        extract_boxed(text)
        or extract_gsm_final(text)
        or extract_freeform_answer(text)
    )


# ── Normalization ─────────────────────────────────────────────────────────────

_FRAC_RE = re.compile(r"\\?frac\s*{([^{}]+)}\s*{([^{}]+)}")
_DFRAC_RE = re.compile(r"\\dfrac\s*{([^{}]+)}\s*{([^{}]+)}")
_TFRAC_RE = re.compile(r"\\tfrac\s*{([^{}]+)}\s*{([^{}]+)}")
_LEFT_RIGHT = re.compile(r"\\left|\\right")
_UNIT_TAILS = re.compile(r"\\(?:text|mathrm|mathit|mathbf)\s*{[^{}]*}")
_PCT = re.compile(r"\\%|%")
_DOLLAR = re.compile(r"\$")
_COMMAS_IN_NUMBER = re.compile(r"(?<=\d),(?=\d{3}(\D|$))")


def normalize_math_string(s: str) -> str:
    """Light textual normalization (LaTeX fragments → plain math)."""
    if s is None:
        return ""
    s = s.strip()
    # Remove \left \right
    s = _LEFT_RIGHT.sub("", s)
    # \frac{a}{b} → (a)/(b); same for \dfrac, \tfrac
    for pat in (_DFRAC_RE, _TFRAC_RE, _FRAC_RE):
        prev = None
        while prev != s:
            prev = s
            s = pat.sub(r"(\1)/(\2)", s)
    # Drop unit annotations
    s = _UNIT_TAILS.sub("", s)
    # %, $, commas in numbers
    s = _PCT.sub("", s)
    s = _DOLLAR.sub("", s)
    s = _COMMAS_IN_NUMBER.sub("", s)
    # Strip trailing periods and whitespace
    s = s.strip().rstrip(".").strip()
    # Collapse internal whitespace
    s = re.sub(r"\s+", "", s)
    return s


def _to_sympy(s: str):
    try:
        from sympy import sympify
        # Avoid auto-simplifying so ``1/2 == 0.5`` works via simplify(a-b).
        return sympify(s, evaluate=True)
    except Exception:
        return None


def answers_equivalent(pred: Optional[str], gold: Optional[str]) -> bool:
    """Robust equivalence: normalize text → string compare → sympy compare."""
    if pred is None or gold is None:
        return False
    np_ = normalize_math_string(pred)
    ng_ = normalize_math_string(gold)
    if not np_ or not ng_:
        return False
    if np_ == ng_:
        return True
    # Numeric equivalence first
    try:
        if float(np_) == float(ng_):
            return True
    except Exception:
        pass
    # Sympy fallback
    a = _to_sympy(np_)
    b = _to_sympy(ng_)
    if a is None or b is None:
        return False
    try:
        from sympy import simplify
        return bool(simplify(a - b) == 0)
    except Exception:
        return False
