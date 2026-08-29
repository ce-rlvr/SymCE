"""
Unit tests for training.rlvr.reward.

These mock execute_and_verify so the suite runs without spawning python3
subprocesses or importing sympy/z3 — fast, hermetic, deterministic.

Run from repo root:
    python -m pytest training/rlvr/tests/test_reward.py -v
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import pytest

from training.rlvr import reward as reward_mod
from training.rlvr.config import REWARD_WEIGHTS
from training.rlvr.reward import (
    extract_code,
    format_reward,
    make_verifier_reward,
    score_completion,
)


# ─── extract_code ────────────────────────────────────────────────────────────

def test_extract_python_fence():
    text = "Reasoning…\n```python\nx = 1\nassert not False\n```\nDone"
    assert extract_code(text) == "x = 1\nassert not False"


def test_extract_generic_fence_fallback():
    text = "Try this:\n```\nprint('hi')\n```"
    assert extract_code(text) == "print('hi')"


def test_extract_first_of_multiple_fences():
    text = "```python\nA = 1\n```\nlater\n```python\nB = 2\n```"
    assert extract_code(text) == "A = 1"


def test_extract_returns_none_when_no_fence():
    assert extract_code("Just prose, no code.") is None


def test_extract_returns_none_for_non_string():
    assert extract_code(None) is None  # type: ignore[arg-type]
    assert extract_code("") is None


# ─── score_completion: every classifier branch ───────────────────────────────

def _stub(monkeypatch, result: dict):
    monkeypatch.setattr(reward_mod, "execute_and_verify", lambda code: result)


def test_score_no_code(monkeypatch):
    # Verifier should not be invoked when extraction fails.
    monkeypatch.setattr(reward_mod, "execute_and_verify",
                        lambda code: pytest.fail("verifier should not run"))
    r, reason, vresult = score_completion("no code here")
    assert r == REWARD_WEIGHTS["no_code"]
    assert reason == "no_code"
    assert vresult == {}


def test_score_safety_invalid(monkeypatch):
    _stub(monkeypatch, {
        "success": False, "exit_code": -1, "timed_out": False,
        "syntax_error": False, "runtime_error": False,
        "negation_form_ok": True, "safety_ok": False,
    })
    r, reason, _ = score_completion("```python\nimport os\nassert not False\n```")
    assert r == REWARD_WEIGHTS["safety_invalid"]
    assert reason == "safety_invalid"


def test_score_negation_invalid_overrides_success(monkeypatch):
    """Critical: a script that exits 0 but lacks negation MUST still be penalised."""
    _stub(monkeypatch, {
        "success": True, "exit_code": 0, "timed_out": False,
        "syntax_error": False, "runtime_error": False,
        "negation_form_ok": False, "safety_ok": True,
    })
    r, reason, _ = score_completion("```python\nassert True\n```")
    assert r == REWARD_WEIGHTS["negation_invalid"]
    assert reason == "negation_invalid"


def test_score_success(monkeypatch):
    _stub(monkeypatch, {
        "success": True, "exit_code": 0, "timed_out": False,
        "syntax_error": False, "runtime_error": False,
        "negation_form_ok": True, "safety_ok": True,
    })
    r, reason, _ = score_completion("```python\nassert not False\n```")
    assert r == REWARD_WEIGHTS["success"]
    assert reason == "success"


def test_score_syntax_error(monkeypatch):
    _stub(monkeypatch, {
        "success": False, "exit_code": 1, "timed_out": False,
        "syntax_error": True, "runtime_error": False,
        "negation_form_ok": True, "safety_ok": True,
    })
    r, reason, _ = score_completion("```python\nassert not\n```")
    assert r == REWARD_WEIGHTS["syntax_error"]
    assert reason == "syntax_error"


def test_score_timed_out(monkeypatch):
    _stub(monkeypatch, {
        "success": False, "exit_code": -1, "timed_out": True,
        "syntax_error": False, "runtime_error": False,
        "negation_form_ok": True, "safety_ok": True,
    })
    r, reason, _ = score_completion("```python\nwhile True: pass\nassert not False\n```")
    assert r == REWARD_WEIGHTS["timed_out"]
    assert reason == "timed_out"


def test_score_runtime_error(monkeypatch):
    _stub(monkeypatch, {
        "success": False, "exit_code": 1, "timed_out": False,
        "syntax_error": False, "runtime_error": True,
        "negation_form_ok": True, "safety_ok": True,
    })
    r, reason, _ = score_completion("```python\nassert not (1 == 1)\n```")
    assert r == REWARD_WEIGHTS["runtime_error"]
    assert reason == "runtime_error"


def test_score_default_branch(monkeypatch):
    """ImportError / unknown failure with no flag set → default reward."""
    _stub(monkeypatch, {
        "success": False, "exit_code": 1, "timed_out": False,
        "syntax_error": False, "runtime_error": False,
        "negation_form_ok": True, "safety_ok": True,
    })
    r, reason, _ = score_completion("```python\nimport nonexistent\nassert not False\n```")
    assert r == REWARD_WEIGHTS["default"]
    assert reason == "default"


def test_score_handles_verifier_exception(monkeypatch):
    def boom(code):
        raise OSError("disk full")
    monkeypatch.setattr(reward_mod, "execute_and_verify", boom)
    r, reason, vresult = score_completion("```python\nassert not False\n```")
    assert r == REWARD_WEIGHTS["default"]
    assert reason == "verifier_exception"
    assert "exception" in vresult


# ─── make_verifier_reward (TRL signature) ────────────────────────────────────

def _conv(text: str) -> list[dict]:
    return [{"role": "assistant", "content": text}]


def test_verifier_reward_signature_and_length(monkeypatch):
    _stub(monkeypatch, {
        "success": True, "exit_code": 0, "timed_out": False,
        "syntax_error": False, "runtime_error": False,
        "negation_form_ok": True, "safety_ok": True,
    })
    fn = make_verifier_reward(pool_workers=1)  # serial → easy to reason about
    completions = [
        _conv("```python\nassert not False\n```"),
        _conv("no fence here"),
    ]
    out = fn(prompts=[None, None], completions=completions)
    assert out == [REWARD_WEIGHTS["success"], REWARD_WEIGHTS["no_code"]]


def test_verifier_reward_logs_rollouts(monkeypatch, tmp_path):
    _stub(monkeypatch, {
        "success": True, "exit_code": 0, "timed_out": False,
        "syntax_error": False, "runtime_error": False,
        "negation_form_ok": True, "safety_ok": True,
    })
    log_path = tmp_path / "rollouts.jsonl"
    from training.rlvr.reward import RolloutLogger
    fn = make_verifier_reward(rollout_logger=RolloutLogger(log_path), pool_workers=1)
    fn(prompts=[None], completions=[_conv("```python\nassert not False\n```")])
    assert log_path.exists()
    line = log_path.read_text().strip().splitlines()[0]
    assert '"reason": "success"' in line


def test_verifier_reward_extra_kwargs_ignored(monkeypatch):
    _stub(monkeypatch, {
        "success": True, "exit_code": 0, "timed_out": False,
        "syntax_error": False, "runtime_error": False,
        "negation_form_ok": True, "safety_ok": True,
    })
    fn = make_verifier_reward(pool_workers=1)
    # TRL passes a bunch of kwargs; reward_fn must tolerate them.
    out = fn(
        prompts=[None],
        completions=[_conv("```python\nassert not False\n```")],
        completion_ids=[[1, 2, 3]],
        trainer_state=None,
        log_extra=lambda **k: None,
    )
    assert out == [REWARD_WEIGHTS["success"]]


# ─── format_reward ───────────────────────────────────────────────────────────

def test_format_reward_positive():
    completions = [_conv("```python\nx=1\nassert not False\n```")]
    assert format_reward(completions=completions) == [1.0]


def test_format_reward_missing_assert():
    completions = [_conv("```python\nx=1\n```")]
    assert format_reward(completions=completions) == [0.0]


def test_format_reward_missing_fence():
    completions = [_conv("assert not False")]
    assert format_reward(completions=completions) == [0.0]


def test_format_reward_handles_empty_batch():
    assert format_reward(completions=[]) == []
