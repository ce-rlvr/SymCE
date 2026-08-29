#!/usr/bin/env python3
"""Answer extraction for the theorem-truth probe under the ``truth_classify`` style.

The evaluation harness shipped a last-resort parser, ``\\b(true|false)\\b``, that
matched any bare occurrence of the word anywhere in the completion and took the
last one.  In a chain of thought about whether a theorem is true that word occurs
constantly, so completions that ran out of tokens mid-reasoning -- never stating an
answer at all -- were scored as if they had answered TRUE.

This module replaces it.  An answer counts only when it appears inside an explicit
answer frame *near the end* of the completion, which is where a verdict is actually
stated.  The frames cover every phrasing observed across Qwen3-4B and Gemma-3-4B
checkpoints:

    Answer: TRUE                      Final answer = FALSE
    The final answer is \\boxed{TRUE}   Thus, the claim is **FALSE**.
    Therefore, the conjecture is TRUE  TRUE          (alone on the closing line)
"""
from __future__ import annotations

import re

# Characters from the end of the completion (or from the end of the reasoning
# block, when one is closed) within which a verdict is looked for.
TAIL_WINDOW = 400

_FRAMES = [
    # \boxed{TRUE}, \boxed{\text{TRUE}}, \boxed{**TRUE**}
    re.compile(r"\\boxed\s*\{[^{}]*?\b(TRUE|FALSE)\b[^{}]*?\}", re.IGNORECASE),
    # "answer: TRUE", "final answer = FALSE", "the answer is TRUE"
    re.compile(r"(?:final\s+)?answer\s*(?:is|:|=)\s*[*_`$\s]*\b(TRUE|FALSE)\b", re.IGNORECASE),
    # "the claim is TRUE", "therefore the conjecture is **FALSE**"
    re.compile(r"\b(?:claim|conjecture|statement|theorem|proposition)\s+is\s*"
               r"[*_`$\s]*\b(TRUE|FALSE)\b", re.IGNORECASE),
    # a closing line that is nothing but the verdict
    re.compile(r"(?m)^\s*[*_`#\s]*\b(TRUE|FALSE)\b[*_`.\s]*$", re.IGNORECASE),
]


def _tail(text: str) -> str:
    """The region in which a final verdict may legitimately appear."""
    marker = text.rfind("</think>")
    if marker != -1:
        after = text[marker + len("</think>"):]
        # A closed reasoning block delimits the answer exactly.
        if after.strip():
            return after
    return text[-TAIL_WINDOW:]


def extract_truth_label(text: str) -> str | None:
    """Return "TRUE", "FALSE", or None when the completion states no verdict."""
    if not isinstance(text, str) or not text:
        return None
    window = _tail(text)
    best_pos, best_val = -1, None
    for pattern in _FRAMES:
        for match in pattern.finditer(window):
            if match.start() > best_pos:
                best_pos, best_val = match.start(), match.group(1).upper()
    return best_val.upper() if best_val else None


def predicted_true(text: str) -> bool:
    return extract_truth_label(text) == "TRUE"
