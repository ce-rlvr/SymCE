"""
Unit tests for src/oracle/sandbox.py.

These tests run without Gemini — they use hand-crafted verifier modules written
to temporary files to exercise every code path in run_oracle().
"""

from __future__ import annotations

import sys
import tempfile
import textwrap
from pathlib import Path

import pytest

# Ensure project root is on path
_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))

from src.oracle.sandbox import run_oracle, OracleResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_module(source: str) -> Path:
    """Write a Python module to a named temp file and return its path."""
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", prefix="test_verifier_",
        delete=False, encoding="utf-8"
    )
    tmp.write(textwrap.dedent(source))
    tmp.close()
    return Path(tmp.name)


# ---------------------------------------------------------------------------
# Fixtures: a minimal correct verifier module (group theory style)
# ---------------------------------------------------------------------------

_GOOD_MODULE = """
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, AbelianGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
C2 = CyclicGroup(2)
C3 = CyclicGroup(3)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group — all PermutationGroups are finite; order() > 0 is a reliable check
    try:
        h1 = witness.order() > 0
    except Exception:
        h1 = False
    # neg_Q: G is not cyclic
    try:
        neg_q = not witness.is_cyclic
    except Exception:
        neg_q = False
    return [h1, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: G is finite",
    "neg_Q: G is not cyclic",
]
N_HYP: int = 1
NEG_Q_INDEX: int = 1
"""


@pytest.fixture
def good_module_path(tmp_path):
    p = tmp_path / "good_verifier.py"
    p.write_text(textwrap.dedent(_GOOD_MODULE), encoding="utf-8")
    return str(p)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestRunOracle:
    def test_passing_witness(self, good_module_path):
        """V4 is a finite non-cyclic group — all conditions should be True."""
        result = run_oracle(good_module_path, "V4", n_conditions=2, timeout_seconds=15.0)
        assert result.parse_ok is True
        assert result.conditions is not None
        assert len(result.conditions) == 2
        assert result.conditions[0] is True   # H_1: G is finite
        assert result.conditions[1] is True   # neg_Q: V4 is not cyclic
        assert result.error is None
        assert result.timed_out is False

    def test_failing_witness_cyclic(self, good_module_path):
        """C4 is cyclic — neg_Q should be False."""
        result = run_oracle(good_module_path, "C4", n_conditions=2, timeout_seconds=15.0)
        assert result.parse_ok is True
        assert result.conditions is not None
        assert result.conditions[0] is True   # H_1: C4 is finite
        assert result.conditions[1] is False  # neg_Q: C4 IS cyclic, so negation fails

    def test_bad_witness_expression(self, good_module_path):
        """A witness expression that refers to an undefined name should fail gracefully."""
        result = run_oracle(good_module_path, "UndefinedGroup", n_conditions=2, timeout_seconds=15.0)
        assert result.parse_ok is False
        assert result.conditions is None
        assert result.error is not None
        assert "WitnessEvalError" in result.error

    def test_syntax_error_in_witness(self, good_module_path):
        """A witness expression with syntax errors should fail gracefully."""
        result = run_oracle(good_module_path, "def bad(): pass", n_conditions=2, timeout_seconds=15.0)
        # eval of a statement raises SyntaxError — should produce parse_ok=False
        assert result.parse_ok is False

    def test_nonexistent_module(self, tmp_path):
        """A missing module file should return an error without crashing."""
        result = run_oracle(str(tmp_path / "nonexistent.py"), "S3", n_conditions=2, timeout_seconds=5.0)
        assert result.parse_ok is False
        assert result.error is not None

    def test_timeout(self, tmp_path):
        """A verifier that loops forever should time out cleanly."""
        slow_module = tmp_path / "slow_verifier.py"
        slow_module.write_text(textwrap.dedent("""
            def conditions(witness) -> list[bool]:
                import time
                time.sleep(999)
                return [True]
            CONDITION_LABELS = ["H_1: always"]
            N_HYP = 0
            NEG_Q_INDEX = 0
        """), encoding="utf-8")
        result = run_oracle(str(slow_module), "1", n_conditions=1, timeout_seconds=2.0)
        assert result.timed_out is True
        assert result.conditions is None

    def test_dangerous_module_blocked(self, tmp_path):
        """A verifier importing os should be blocked by the safety check."""
        dangerous = tmp_path / "dangerous.py"
        dangerous.write_text(textwrap.dedent("""
            import os
            def conditions(witness) -> list[bool]:
                return [True]
            CONDITION_LABELS = ["H_1: always"]
            N_HYP = 0
            NEG_Q_INDEX = 0
        """), encoding="utf-8")
        result = run_oracle(str(dangerous), "1", n_conditions=1, timeout_seconds=5.0)
        assert result.parse_ok is False
        assert result.error is not None
        assert "SafetyCheckFailed" in result.error

    def test_determinism(self, good_module_path):
        """Same inputs must produce the same result across multiple calls."""
        r1 = run_oracle(good_module_path, "V4", n_conditions=2, timeout_seconds=15.0)
        r2 = run_oracle(good_module_path, "V4", n_conditions=2, timeout_seconds=15.0)
        assert r1.parse_ok == r2.parse_ok
        assert r1.conditions == r2.conditions
        assert r1.error == r2.error

    def test_conditions_error_caught(self, tmp_path):
        """If conditions() raises, we should get an error but not a crash."""
        broken = tmp_path / "broken_conditions.py"
        broken.write_text(textwrap.dedent("""
            def conditions(witness) -> list[bool]:
                raise ValueError("deliberate failure")
            CONDITION_LABELS = ["H_1: always"]
            N_HYP = 0
            NEG_Q_INDEX = 0
        """), encoding="utf-8")
        result = run_oracle(str(broken), "1", n_conditions=1, timeout_seconds=5.0)
        # parse_ok may be True (witness eval succeeded) but conditions is None
        assert result.conditions is None
        assert result.error is not None
        assert "ConditionsError" in result.error

    def test_linear_algebra_witness(self, tmp_path):
        """A matrix-based verifier should work correctly."""
        matrix_module = tmp_path / "matrix_verifier.py"
        matrix_module.write_text(textwrap.dedent("""
            from sympy import Matrix, zeros, eye

            I2 = eye(2)
            O2 = zeros(2, 2)

            def conditions(witness) -> list[bool]:
                try:
                    h1 = witness.shape[0] == witness.shape[1]
                except Exception:
                    h1 = False
                try:
                    evs = list(witness.eigenvals().keys())
                    h2 = all(ev == 0 for ev in evs)
                except Exception:
                    h2 = False
                try:
                    neg_q = witness != zeros(*witness.shape)
                except Exception:
                    neg_q = False
                return [h1, h2, neg_q]

            CONDITION_LABELS = [
                "H_1: witness is square",
                "H_2: all eigenvalues are zero",
                "neg_Q: witness is not the zero matrix",
            ]
            N_HYP = 2
            NEG_Q_INDEX = 2
        """), encoding="utf-8")
        result = run_oracle(
            str(matrix_module),
            "Matrix([[0, 1], [0, 0]])",
            n_conditions=3,
            timeout_seconds=15.0,
        )
        assert result.parse_ok is True
        assert result.conditions == [True, True, True]
