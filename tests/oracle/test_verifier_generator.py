"""
Unit tests for src/oracle/verifier_generator.py parser utilities.

Tests only the parsing / formatting logic — no Gemini API calls.
"""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))

from src.oracle.verifier_generator import (
    _parse_module_constants,
    _extract_python_from_response,
    _module_filename,
)


# ---------------------------------------------------------------------------
# _parse_module_constants
# ---------------------------------------------------------------------------

_GOOD_MODULE = """
from sympy.combinatorics.named_groups import SymmetricGroup

S3 = SymmetricGroup(3)

def conditions(witness) -> list[bool]:
    h1 = witness.is_finite if hasattr(witness, 'is_finite') else True
    neg_q = not witness.is_cyclic
    return [h1, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: G is finite",
    "neg_Q: G is not cyclic",
]
N_HYP: int = 1
NEG_Q_INDEX: int = 1
"""


class TestParseModuleConstants:
    def test_parses_good_module(self):
        labels, n_hyp, neg_q_index = _parse_module_constants(_GOOD_MODULE)
        assert labels == ["H_1: G is finite", "neg_Q: G is not cyclic"]
        assert n_hyp == 1
        assert neg_q_index == 1

    def test_missing_condition_labels(self):
        source = textwrap.dedent("""
            def conditions(witness): return [True]
            N_HYP: int = 0
            NEG_Q_INDEX: int = 0
        """)
        with pytest.raises(ValueError, match="CONDITION_LABELS"):
            _parse_module_constants(source)

    def test_missing_nhyp(self):
        source = textwrap.dedent("""
            def conditions(witness): return [True]
            CONDITION_LABELS: list[str] = ["neg_Q: x"]
            NEG_Q_INDEX: int = 0
        """)
        with pytest.raises(ValueError, match="N_HYP"):
            _parse_module_constants(source)

    def test_neg_q_not_last(self):
        """NEG_Q_INDEX != N_HYP should raise ValueError."""
        source = textwrap.dedent("""
            def conditions(witness): return [True, True]
            CONDITION_LABELS: list[str] = ["H_1: x", "neg_Q: y"]
            N_HYP: int = 1
            NEG_Q_INDEX: int = 0
        """)
        with pytest.raises(ValueError, match="NEG_Q_INDEX"):
            _parse_module_constants(source)

    def test_label_count_mismatch(self):
        """CONDITION_LABELS length != N_HYP + 1 should raise."""
        source = textwrap.dedent("""
            def conditions(witness): return [True, True, True]
            CONDITION_LABELS: list[str] = ["H_1: x", "neg_Q: y"]
            N_HYP: int = 2
            NEG_Q_INDEX: int = 2
        """)
        with pytest.raises(ValueError, match="CONDITION_LABELS length"):
            _parse_module_constants(source)

    def test_three_conditions(self):
        source = textwrap.dedent("""
            def conditions(witness): return [True, True, True]
            CONDITION_LABELS: list[str] = ["H_1: a", "H_2: b", "neg_Q: c"]
            N_HYP: int = 2
            NEG_Q_INDEX: int = 2
        """)
        labels, n_hyp, neg_q_index = _parse_module_constants(source)
        assert len(labels) == 3
        assert n_hyp == 2
        assert neg_q_index == 2

    def test_no_type_annotation_on_constants(self):
        """Constants without type annotations should still be parseable."""
        source = textwrap.dedent("""
            def conditions(witness): return [True, True]
            CONDITION_LABELS = ["H_1: finite", "neg_Q: not cyclic"]
            N_HYP = 1
            NEG_Q_INDEX = 1
        """)
        labels, n_hyp, neg_q_index = _parse_module_constants(source)
        assert n_hyp == 1


# ---------------------------------------------------------------------------
# _extract_python_from_response
# ---------------------------------------------------------------------------

class TestExtractPython:
    def test_plain_code(self):
        src = "from sympy import *\nprint('hello')"
        assert _extract_python_from_response(src) == src

    def test_strips_python_fence(self):
        src = "```python\nfrom sympy import *\n```"
        assert _extract_python_from_response(src) == "from sympy import *"

    def test_strips_bare_fence(self):
        src = "```\nfrom sympy import *\n```"
        assert _extract_python_from_response(src) == "from sympy import *"

    def test_strips_surrounding_prose(self):
        src = "Here is the module:\n```python\nfrom sympy import *\n```\nDone."
        result = _extract_python_from_response(src)
        assert result == "from sympy import *"

    def test_whitespace_stripping(self):
        src = "   \n  from sympy import *  \n  "
        assert _extract_python_from_response(src) == "from sympy import *"


# ---------------------------------------------------------------------------
# _module_filename
# ---------------------------------------------------------------------------

class TestModuleFilename:
    def test_basic(self):
        record = {"theorem_id": "sylow_first", "dropped_hypothesis_name": "h1"}
        assert _module_filename(record) == "sylow_first__h1.py"

    def test_sanitises_special_chars(self):
        record = {"theorem_id": "thm.with.dots", "dropped_hypothesis_name": "h-1 (special)"}
        name = _module_filename(record)
        assert name.endswith(".py")
        assert "/" not in name
        assert " " not in name

    def test_defaults_on_missing_keys(self):
        record = {}
        name = _module_filename(record)
        assert name.endswith(".py")
        assert "__" in name
