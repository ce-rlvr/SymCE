"""
Unit + integration tests for training.rlvr.reward_oracle.

Covers:
- compute_reward_oracle on hand-crafted verifier modules (every branch).
- make_oracle_reward TRL-shaped factory (kwargs path).
- Integration sample on the v2 dev dataset
  (data/algebra_counterexamples_v2.jsonl).
- Sparse / default weights preset behaviour.
- Determinism: same (record, completion) -> same reward across calls.

Heavy tests (those that spawn the oracle subprocess) are marked `@slow` and
can be opted in/out via `-m "not slow"`. Default run executes them, since P2's
validation gate explicitly requires real verifier calls.
"""

from __future__ import annotations

import json
import math
import random
import sys
import textwrap
from pathlib import Path
from typing import Any

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from training.rlvr.config import (
    ORACLE_REWARD_WEIGHTS_DEFAULT,
    ORACLE_REWARD_WEIGHTS_SPARSE,
)
from training.rlvr.reward_oracle import (
    OracleRolloutLogger,
    RewardBreakdown,
    compute_reward_oracle,
    make_oracle_reward,
    parse_counterexample_tag,
)


# ---------------------------------------------------------------------------
# Test fixtures: minimal verifier modules
# ---------------------------------------------------------------------------

# A simple non-cyclic group verifier - one remaining-hyp + one ¬Q.
_GROUP_VERIFIER = """
from sympy.combinatorics.named_groups import (
    SymmetricGroup, CyclicGroup, AlternatingGroup, AbelianGroup,
)

S3 = SymmetricGroup(3)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
A5 = AlternatingGroup(5)

CONDITION_LABELS = [
    "H_1: G is finite",
    "neg_Q: G is not cyclic",
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        h1 = witness.order() > 0
    except Exception:
        h1 = False
    try:
        neg_q = not bool(witness.is_cyclic)
    except Exception:
        neg_q = False
    return [h1, neg_q]
"""


# A verifier with ZERO remaining hypotheses (n_hyp = 0). 41/326 of the
# current dev sample look like this; the alpha term must default to 0 cleanly.
_NO_HYP_VERIFIER = """
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, CyclicGroup,
)
S3 = SymmetricGroup(3)
A5 = AlternatingGroup(5)
C4 = CyclicGroup(4)

CONDITION_LABELS = ["neg_Q: G is not solvable"]
N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        return [not bool(witness.is_solvable)]
    except Exception:
        return [False]
"""


# A verifier that returns the WRONG number of booleans - the reward fn must
# treat this as a parse-level error and apply -ε.
_BAD_LENGTH_VERIFIER = """
CONDITION_LABELS = ["H_1: x is positive", "neg_Q: x != 0"]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    # Declares n_conditions=2 but only returns 1 boolean.
    return [True]
"""


@pytest.fixture
def group_verifier_path(tmp_path: Path) -> Path:
    p = tmp_path / "group_verifier.py"
    p.write_text(textwrap.dedent(_GROUP_VERIFIER), encoding="utf-8")
    return p


@pytest.fixture
def no_hyp_verifier_path(tmp_path: Path) -> Path:
    p = tmp_path / "no_hyp_verifier.py"
    p.write_text(textwrap.dedent(_NO_HYP_VERIFIER), encoding="utf-8")
    return p


@pytest.fixture
def bad_length_verifier_path(tmp_path: Path) -> Path:
    p = tmp_path / "bad_length_verifier.py"
    p.write_text(textwrap.dedent(_BAD_LENGTH_VERIFIER), encoding="utf-8")
    return p


def _record_for(module_path: Path, *, n_hyp: int, neg_q_index: int, n_conditions: int) -> dict:
    """Build a minimal v2-shaped record around a verifier module."""
    return {
        "verifier": {
            "module_path": str(module_path),
            "n_hyp": n_hyp,
            "neg_q_index": neg_q_index,
            "n_conditions": n_conditions,
        }
    }


# ---------------------------------------------------------------------------
# compute_reward_oracle - every branch
# ---------------------------------------------------------------------------


class TestComputeRewardBranches:
    def test_no_tag(self, group_verifier_path):
        rec = _record_for(group_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
        bd = compute_reward_oracle(rec, "no tag here at all", timeout_seconds=15.0)
        assert isinstance(bd, RewardBreakdown)
        assert bd.format_ok is False
        assert bd.parse_ok is False
        assert bd.witness_expr is None
        assert bd.reason == "no_tag"
        assert math.isclose(bd.total, -ORACLE_REWARD_WEIGHTS_DEFAULT["epsilon"])

    def test_none_sentinel_stage1(self, group_verifier_path):
        rec = _record_for(group_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
        bd = compute_reward_oracle(
            rec,
            "<reasoning>I cannot find one.</reasoning>\n[COUNTEREXAMPLE: NONE]",
            timeout_seconds=15.0,
        )
        assert bd.is_none is True
        assert bd.gave_up is True
        assert bd.reason == "none_on_false"
        assert bd.format_ok is True
        # r = -δ + γ * format_ok
        expected = (
            -ORACLE_REWARD_WEIGHTS_DEFAULT["delta"]
            + ORACLE_REWARD_WEIGHTS_DEFAULT["gamma"]
        )
        assert math.isclose(bd.total, expected)

    def test_successful_witness(self, group_verifier_path):
        rec = _record_for(group_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
        bd = compute_reward_oracle(rec, "[COUNTEREXAMPLE: V4]", timeout_seconds=20.0)
        assert bd.reason == "success"
        assert bd.parse_ok is True
        assert bd.format_ok is True
        assert bd.s_hyp == 1
        assert bd.n_hyp == 1
        assert bd.q_neg == 1
        w = ORACLE_REWARD_WEIGHTS_DEFAULT
        expected = w["alpha"] * 1 + w["beta"] * 1 + w["gamma"] * 1
        assert math.isclose(bd.total, expected)

    def test_witness_satisfies_hyps_but_not_negq(self, group_verifier_path):
        """C4 is finite (hyp) but IS cyclic (¬Q fails) - the canonical
        Learning-to-Disprove failure mode. β should NOT contribute; α + γ
        provides bounded partial credit."""
        rec = _record_for(group_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
        bd = compute_reward_oracle(rec, "[COUNTEREXAMPLE: C4]", timeout_seconds=20.0)
        assert bd.parse_ok is True
        assert bd.s_hyp == 1
        assert bd.q_neg == 0
        assert bd.reason == "hyp_only"
        w = ORACLE_REWARD_WEIGHTS_DEFAULT
        expected = w["alpha"] * 1 + w["beta"] * 0 + w["gamma"] * 1
        assert math.isclose(bd.total, expected)
        # Sanity: this MUST be strictly less than a real success.
        success_bd = compute_reward_oracle(rec, "[COUNTEREXAMPLE: V4]", timeout_seconds=20.0)
        assert bd.total < success_bd.total

    def test_witness_name_undefined(self, group_verifier_path):
        rec = _record_for(group_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
        bd = compute_reward_oracle(rec, "[COUNTEREXAMPLE: UndefinedGroup]", timeout_seconds=15.0)
        assert bd.parse_ok is False
        assert bd.reason == "oracle_parse_error"
        assert bd.oracle_error and "WitnessEvalError" in bd.oracle_error
        # r = -ε but we still pay no other terms (format_ok is True).
        # Formula: 0 + 0 + γ*format_ok - 0 - ε*1 = γ - ε
        # Implementation: we short-circuit to -ε (γ does not apply when
        # parse_ok is False); document that the test pins the short-circuit.
        assert math.isclose(bd.total, -ORACLE_REWARD_WEIGHTS_DEFAULT["epsilon"])

    def test_n_hyp_zero(self, no_hyp_verifier_path):
        """When n_hyp == 0, α-term is 0 and only β + γ contribute."""
        rec = _record_for(no_hyp_verifier_path, n_hyp=0, neg_q_index=0, n_conditions=1)
        bd = compute_reward_oracle(rec, "[COUNTEREXAMPLE: A5]", timeout_seconds=20.0)
        assert bd.parse_ok is True
        assert bd.s_hyp == 0
        assert bd.n_hyp == 0
        assert bd.q_neg == 1
        w = ORACLE_REWARD_WEIGHTS_DEFAULT
        # alpha * 0 + β + γ
        expected = w["beta"] + w["gamma"]
        assert math.isclose(bd.total, expected)
        assert bd.reason == "success"

    def test_n_hyp_zero_q_false(self, no_hyp_verifier_path):
        """n_hyp = 0 and Q not negated (A5 IS not solvable; S3 IS solvable
        so ¬Q fails for S3)."""
        rec = _record_for(no_hyp_verifier_path, n_hyp=0, neg_q_index=0, n_conditions=1)
        bd = compute_reward_oracle(rec, "[COUNTEREXAMPLE: S3]", timeout_seconds=20.0)
        assert bd.q_neg == 0
        # Only γ contributes; α=0, β=0
        w = ORACLE_REWARD_WEIGHTS_DEFAULT
        assert math.isclose(bd.total, w["gamma"])
        assert bd.reason == "partial"

    def test_condition_length_mismatch(self, bad_length_verifier_path):
        rec = _record_for(bad_length_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
        bd = compute_reward_oracle(rec, "[COUNTEREXAMPLE: 1]", timeout_seconds=15.0)
        assert bd.parse_ok is False
        assert bd.reason == "condition_length_mismatch"
        assert math.isclose(bd.total, -ORACLE_REWARD_WEIGHTS_DEFAULT["epsilon"])

    def test_nonexistent_module(self, tmp_path):
        rec = _record_for(tmp_path / "missing.py", n_hyp=1, neg_q_index=1, n_conditions=2)
        bd = compute_reward_oracle(rec, "[COUNTEREXAMPLE: V4]", timeout_seconds=10.0)
        assert bd.parse_ok is False
        assert bd.reason == "oracle_parse_error"
        assert math.isclose(bd.total, -ORACLE_REWARD_WEIGHTS_DEFAULT["epsilon"])

    def test_unparseable_completion(self, group_verifier_path):
        rec = _record_for(group_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
        bd = compute_reward_oracle(rec, "", timeout_seconds=10.0)
        assert bd.reason == "no_tag"
        assert math.isclose(bd.total, -ORACLE_REWARD_WEIGHTS_DEFAULT["epsilon"])


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


def test_determinism_success(group_verifier_path):
    rec = _record_for(group_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
    text = "[COUNTEREXAMPLE: V4]"
    a = compute_reward_oracle(rec, text, timeout_seconds=15.0)
    b = compute_reward_oracle(rec, text, timeout_seconds=15.0)
    c = compute_reward_oracle(rec, text, timeout_seconds=15.0)
    assert a.total == b.total == c.total
    assert a.conditions == b.conditions == c.conditions
    assert a.reason == b.reason == c.reason


# ---------------------------------------------------------------------------
# Sparse preset - recovers binary {-1, 0, +1}
# ---------------------------------------------------------------------------


def test_sparse_preset_success(group_verifier_path):
    rec = _record_for(group_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
    bd = compute_reward_oracle(
        rec,
        "[COUNTEREXAMPLE: V4]",
        weights=ORACLE_REWARD_WEIGHTS_SPARSE,
        timeout_seconds=20.0,
    )
    # α=γ=δ=0, β=ε=1 -> on success r = 0 + 1 + 0 = +1
    assert math.isclose(bd.total, 1.0)


def test_sparse_preset_hyp_only(group_verifier_path):
    """C4 satisfies the hyp but is cyclic. Sparse reward gives 0 - only β
    counts and q_neg=0."""
    rec = _record_for(group_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
    bd = compute_reward_oracle(
        rec,
        "[COUNTEREXAMPLE: C4]",
        weights=ORACLE_REWARD_WEIGHTS_SPARSE,
        timeout_seconds=20.0,
    )
    assert math.isclose(bd.total, 0.0)


def test_sparse_preset_parse_error(group_verifier_path):
    rec = _record_for(group_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
    bd = compute_reward_oracle(
        rec,
        "[COUNTEREXAMPLE: UndefinedSym]",
        weights=ORACLE_REWARD_WEIGHTS_SPARSE,
        timeout_seconds=10.0,
    )
    assert math.isclose(bd.total, -1.0)


# ---------------------------------------------------------------------------
# Validation: bad inputs / task_mode placeholders
# ---------------------------------------------------------------------------


def test_weights_missing_key_raises(group_verifier_path):
    rec = _record_for(group_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
    with pytest.raises(KeyError):
        compute_reward_oracle(rec, "[COUNTEREXAMPLE: V4]", weights={"alpha": 0.1})


def test_unknown_task_mode_raises(group_verifier_path):
    rec = _record_for(group_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
    with pytest.raises(ValueError):
        compute_reward_oracle(rec, "[COUNTEREXAMPLE: V4]", task_mode="wat")


def test_stage2_task_mode_not_implemented(group_verifier_path):
    rec = _record_for(group_verifier_path, n_hyp=1, neg_q_index=1, n_conditions=2)
    with pytest.raises(NotImplementedError):
        compute_reward_oracle(
            rec, "[COUNTEREXAMPLE: V4]", task_mode="counterexample_or_none"
        )


def test_missing_verifier_field_raises(group_verifier_path):
    with pytest.raises(KeyError):
        compute_reward_oracle({}, "[COUNTEREXAMPLE: V4]")


# ---------------------------------------------------------------------------
# make_oracle_reward - TRL-shaped factory
# ---------------------------------------------------------------------------


def _conv(text: str) -> list[dict]:
    return [{"role": "assistant", "content": text}]


def test_factory_missing_kwargs_raises(group_verifier_path):
    fn = make_oracle_reward(pool_workers=1)
    with pytest.raises(KeyError):
        fn(prompts=[None], completions=[_conv("[COUNTEREXAMPLE: V4]")])


def test_factory_happy_path(group_verifier_path):
    fn = make_oracle_reward(pool_workers=1, timeout_seconds=20.0)
    out = fn(
        prompts=[None, None],
        completions=[
            _conv("[COUNTEREXAMPLE: V4]"),
            _conv("[COUNTEREXAMPLE: C4]"),
        ],
        verifier_module_path=[str(group_verifier_path), str(group_verifier_path)],
        n_hyp=[1, 1],
        neg_q_index=[1, 1],
        n_conditions=[2, 2],
    )
    assert len(out) == 2
    assert out[0] > out[1]   # V4 success beats C4 hyp-only
    w = ORACLE_REWARD_WEIGHTS_DEFAULT
    assert math.isclose(out[0], w["alpha"] + w["beta"] + w["gamma"])


def test_factory_logs_breakdown(group_verifier_path, tmp_path):
    log_path = tmp_path / "rollouts.jsonl"
    fn = make_oracle_reward(
        pool_workers=1,
        rollout_logger=OracleRolloutLogger(log_path),
        timeout_seconds=20.0,
    )
    fn(
        prompts=[None],
        completions=[_conv("[COUNTEREXAMPLE: V4]")],
        verifier_module_path=[str(group_verifier_path)],
        n_hyp=[1],
        neg_q_index=[1],
        n_conditions=[2],
    )
    line = log_path.read_text().strip().splitlines()[0]
    rec = json.loads(line)
    assert rec["reason"] == "success"
    assert rec["breakdown"]["q_neg"] == 1
    assert rec["breakdown"]["s_hyp"] == 1


def test_factory_tolerates_extra_trl_kwargs(group_verifier_path):
    """TRL passes a number of kwargs (completion_ids, trainer_state, ...).
    The reward fn must tolerate them without complaint."""
    fn = make_oracle_reward(pool_workers=1, timeout_seconds=20.0)
    out = fn(
        prompts=[None],
        completions=[_conv("[COUNTEREXAMPLE: V4]")],
        completion_ids=[[1, 2, 3]],
        trainer_state=None,
        log_extra=lambda **k: None,
        verifier_module_path=[str(group_verifier_path)],
        n_hyp=[1],
        neg_q_index=[1],
        n_conditions=[2],
    )
    assert len(out) == 1


def test_factory_kwarg_length_mismatch_raises(group_verifier_path):
    fn = make_oracle_reward(pool_workers=1)
    with pytest.raises(ValueError):
        fn(
            prompts=[None, None],
            completions=[
                _conv("[COUNTEREXAMPLE: V4]"),
                _conv("[COUNTEREXAMPLE: C4]"),
            ],
            verifier_module_path=[str(group_verifier_path)],   # length 1 != 2
            n_hyp=[1, 1],
            neg_q_index=[1, 1],
            n_conditions=[2, 2],
        )


# ---------------------------------------------------------------------------
# Integration: real v2 dev records
# ---------------------------------------------------------------------------


_V2_PATH = _REPO_ROOT / "data" / "algebra_counterexamples_v2.jsonl"


def _load_v2_records(only_witness_passes: bool = True, limit: int = 20, seed: int = 42) -> list[dict]:
    if not _V2_PATH.exists():
        pytest.skip(f"{_V2_PATH} not present in this checkout")
    records: list[dict] = []
    with _V2_PATH.open() as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            r = json.loads(raw)
            if r.get("migration_failed"):
                continue
            if only_witness_passes and not r.get("witness_passes_verifier", False):
                continue
            # Verifier module file must exist on disk.
            mp = r.get("verifier", {}).get("module_path")
            if not mp or not Path(mp).exists():
                continue
            records.append(r)
    rng = random.Random(seed)
    rng.shuffle(records)
    return records[:limit]


class TestIntegrationDevSample:
    """Smoke-test against the v2 dev sample (data/algebra_counterexamples_v2.jsonl).

    Per the project owner, this JSONL is a *dev sample*, not the production
    gate-passing corpus. Some records carry `witness_passes_verifier=True` that
    was validated under a permissive migration sandbox, but the strict P2
    sandbox (no `from sympy import *` overlay) reveals namespace-coverage gaps
    in the generated verifier modules. We do NOT gate on per-record success;
    we DO require a reasonable success rate and full reward correctness on
    every passing record.
    """

    # Lower bound on the fraction of randomly-sampled (witness_passes_verifier
    # == True) records whose canonical witness scores `q_neg == 1` under the
    # strict P2 sandbox. 0.50 is intentionally lax - the upstream P1 corpus
    # will be re-migrated before P4, and this gate exists to catch reward-fn
    # regressions, not data-side regressions.
    MIN_PASS_FRACTION: float = 0.50

    def test_canonical_witnesses_score_positive(self):
        records = _load_v2_records(only_witness_passes=True, limit=20)
        if not records:
            pytest.skip("no eligible records in v2 dev sample")

        passes = 0
        verifier_corpus_issues: list[str] = []
        for rec in records:
            rid = f"{rec['theorem_id']}__{rec['dropped_hypothesis_name']}"
            cw = rec["canonical_witness"]
            completion = f"<reasoning>...</reasoning>\n[COUNTEREXAMPLE: {cw}]"
            bd = compute_reward_oracle(rec, completion, timeout_seconds=20.0)

            if not bd.parse_ok:
                verifier_corpus_issues.append(
                    f"{rid}: parse_ok=False; witness={cw!r}; err={bd.oracle_error!r}"
                )
                continue

            # If parse_ok, the reward arithmetic MUST be self-consistent.
            assert bd.q_neg == 1, (
                f"{rid}: parse_ok but ¬Q not satisfied "
                f"(conditions={bd.conditions!r})"
            )
            if bd.n_hyp > 0:
                assert bd.s_hyp == bd.n_hyp, (
                    f"{rid}: parse_ok but only "
                    f"{bd.s_hyp}/{bd.n_hyp} remaining hyps satisfied"
                )
            assert bd.total > 0.0, f"{rid}: parse_ok but reward={bd.total}"
            passes += 1

        frac = passes / len(records)
        # Print summary for debug visibility; pytest -s shows this.
        print(
            f"\n[TestIntegrationDevSample] {passes}/{len(records)} canonical "
            f"witnesses scored positive ({frac:.0%}). Issues: "
            f"{len(verifier_corpus_issues)}"
        )
        for issue in verifier_corpus_issues[:5]:
            print(f" - {issue}")
        assert frac >= self.MIN_PASS_FRACTION, (
            f"Only {frac:.0%} of canonical witnesses scored positive; "
            f"expected >= {self.MIN_PASS_FRACTION:.0%}. Sample of failures: "
            f"{verifier_corpus_issues[:3]}"
        )

    def test_canonical_witnesses_are_deterministic(self):
        records = _load_v2_records(only_witness_passes=True, limit=5)
        if not records:
            pytest.skip("no eligible records in v2 dev sample")
        for rec in records:
            cw = rec["canonical_witness"]
            completion = f"[COUNTEREXAMPLE: {cw}]"
            a = compute_reward_oracle(rec, completion, timeout_seconds=20.0)
            b = compute_reward_oracle(rec, completion, timeout_seconds=20.0)
            assert a.total == b.total, (
                f"non-deterministic reward on {rec['theorem_id']}: "
                f"{a.total!r} != {b.total!r}"
            )
            assert a.conditions == b.conditions
