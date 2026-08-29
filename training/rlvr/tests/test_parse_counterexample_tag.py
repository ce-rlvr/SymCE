"""
Focused unit tests for the `[COUNTEREXAMPLE: <expr>]` tag parser.

These tests intentionally exercise edge cases that affect the reward signal:
case sensitivity, multi-line rejection, balanced-bracket payloads, last-match
preference, NONE sentinel, and surrounding markdown.

Run from repo root:
    python -m pytest training/rlvr/tests/test_parse_counterexample_tag.py -v
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import pytest

from training.rlvr.reward_oracle import ParsedTag, parse_counterexample_tag


# ─── Happy path ──────────────────────────────────────────────────────────────


def test_simple_well_formed():
    res = parse_counterexample_tag("[COUNTEREXAMPLE: V4]")
    assert res == ParsedTag(payload="V4", format_ok=True, is_none=False)


def test_none_sentinel():
    res = parse_counterexample_tag("[COUNTEREXAMPLE: NONE]")
    assert res == ParsedTag(payload="NONE", format_ok=True, is_none=True)


def test_with_reasoning_prefix():
    text = "<reasoning>let me think... A5 should work</reasoning>\n[COUNTEREXAMPLE: AlternatingGroup(5)]"
    res = parse_counterexample_tag(text)
    assert res.payload == "AlternatingGroup(5)"
    assert res.format_ok is True
    assert res.is_none is False


def test_payload_is_stripped():
    res = parse_counterexample_tag("[COUNTEREXAMPLE:   V4   ]")
    assert res.payload == "V4"
    assert res.format_ok is True


# ─── Bracket-balanced payloads (Matrix([[…]]), PermutationGroup(...), etc.) ──


def test_nested_brackets_matrix():
    text = "[COUNTEREXAMPLE: Matrix([[1,0],[0,1]])]"
    res = parse_counterexample_tag(text)
    assert res.payload == "Matrix([[1,0],[0,1]])"
    assert res.format_ok is True


def test_nested_brackets_deep():
    text = "[COUNTEREXAMPLE: [[[1]]]]"
    res = parse_counterexample_tag(text)
    assert res.payload == "[[[1]]]"
    assert res.format_ok is True


def test_nested_brackets_with_call():
    text = "[COUNTEREXAMPLE: PermutationGroup(Permutation([[1,0,2]]))]"
    res = parse_counterexample_tag(text)
    assert res.payload == "PermutationGroup(Permutation([[1,0,2]]))"
    assert res.format_ok is True


# ─── Last-match-wins policy ──────────────────────────────────────────────────


def test_multiple_tags_last_wins():
    text = "[COUNTEREXAMPLE: A] some prose [COUNTEREXAMPLE: B]"
    res = parse_counterexample_tag(text)
    assert res.payload == "B"


def test_multiple_tags_last_wins_across_lines():
    text = "[COUNTEREXAMPLE: A]\nsecond thought\n[COUNTEREXAMPLE: B]"
    res = parse_counterexample_tag(text)
    assert res.payload == "B"


def test_last_malformed_falls_back_to_earlier():
    # Last opener has no matching close on its line; fall back to the
    # earlier well-formed one.
    text = "[COUNTEREXAMPLE: V4]\n[COUNTEREXAMPLE: oops no close\nmoretext"
    res = parse_counterexample_tag(text)
    assert res.payload == "V4"


def test_last_empty_payload_falls_back():
    text = "[COUNTEREXAMPLE: V4]\n[COUNTEREXAMPLE: ]"
    res = parse_counterexample_tag(text)
    assert res.payload == "V4"


# ─── Strictness: case, newline, empty ────────────────────────────────────────


def test_case_sensitive_opener():
    res = parse_counterexample_tag("[counterexample: V4]")
    assert res.payload is None
    assert res.format_ok is False


def test_mixed_case_opener_does_not_match():
    res = parse_counterexample_tag("[Counterexample: V4]")
    assert res.payload is None


def test_multiline_payload_rejected():
    text = "[COUNTEREXAMPLE: V4\n]"
    res = parse_counterexample_tag(text)
    assert res.payload is None
    assert res.format_ok is False


def test_empty_payload_after_strip_rejected():
    res = parse_counterexample_tag("[COUNTEREXAMPLE:    ]")
    assert res.payload is None
    assert res.format_ok is False


def test_unbalanced_open_no_close_rejected():
    res = parse_counterexample_tag("[COUNTEREXAMPLE: V4")
    assert res.payload is None


# ─── Embedded contexts ───────────────────────────────────────────────────────


def test_tag_inside_code_fence_still_extracted():
    text = "```\n[COUNTEREXAMPLE: V4]\n```"
    res = parse_counterexample_tag(text)
    assert res.payload == "V4"


def test_tag_after_reasoning_block():
    text = (
        "<reasoning>\n"
        "S3 is non-abelian, candidate would be S3.\n"
        "Wait, S3 IS in the hypothesis space. Try A4 instead.\n"
        "</reasoning>\n"
        "[COUNTEREXAMPLE: A4]\n"
    )
    res = parse_counterexample_tag(text)
    assert res.payload == "A4"
    assert res.is_none is False


# ─── Defensive: non-string / empty inputs ────────────────────────────────────


def test_empty_string():
    assert parse_counterexample_tag("") == ParsedTag(
        payload=None, format_ok=False, is_none=False
    )


def test_no_tag_at_all():
    res = parse_counterexample_tag("Just prose with no tag at all.")
    assert res == ParsedTag(payload=None, format_ok=False, is_none=False)


def test_non_string_returns_no_tag():
    # Function should not raise on bad input.
    assert parse_counterexample_tag(None) == ParsedTag(  # type: ignore[arg-type]
        payload=None, format_ok=False, is_none=False
    )
    assert parse_counterexample_tag(123) == ParsedTag(  # type: ignore[arg-type]
        payload=None, format_ok=False, is_none=False
    )


def test_none_lowercase_is_not_sentinel():
    res = parse_counterexample_tag("[COUNTEREXAMPLE: none]")
    assert res.payload == "none"
    assert res.format_ok is True
    assert res.is_none is False  # only exact "NONE" is the sentinel


def test_extra_whitespace_around_none():
    res = parse_counterexample_tag("[COUNTEREXAMPLE:   NONE  ]")
    assert res.payload == "NONE"
    assert res.is_none is True
