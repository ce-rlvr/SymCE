"""
Unit tests for ``training.rlvr.trainer._build_reward_funcs`` (P4).

These exercise the branch on ``RLVRConfig.reward_mode`` without instantiating
a ``GRPOTrainer`` (which needs a real LLM + tokenizer + dataset). We assert:

- ``reward_mode='oracle'`` returns the ``oracle_reward`` callable (single fn),
  bound to an ``OracleRolloutLogger`` writing under ``cfg.output_dir``.
- ``reward_mode='legacy'`` with ``enable_format_reward=True`` returns the
  two-fn list ``[verifier_reward, format_reward]``.
- ``reward_mode='legacy'`` with ``enable_format_reward=False`` returns the
  single-fn ``[verifier_reward]`` list.
- An invalid reward_mode raises ``ValueError`` with a clear message.

The oracle path is then driven end-to-end against a hand-crafted verifier
module - the same fixture style as ``tests/oracle/`` - to verify that the
TRL-shaped kwargs path reaches ``compute_reward_oracle`` correctly.
"""

from __future__ import annotations

import os
import sys
import textwrap
from pathlib import Path

import pytest

# Match training.rlvr.train: unsloth's side-effect monkey-patches must run
# before TRL is imported, otherwise trl/trainer/callbacks.py pulls in
# mergekit_utils -> mergekit (not installed in this env). Skip the whole
# module if unsloth isn't importable (e.g. CPU-only CI).
os.environ.setdefault("ACCELERATE_MIXED_PRECISION", "bf16")
unsloth = pytest.importorskip("unsloth")

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from training.rlvr.config import RLVRConfig
from training.rlvr.trainer import _build_reward_funcs


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Minimal verifier module: one trivial remaining-hypothesis (always True) and
# one ¬Q check that fires only when witness == 0. Lets us hit "success" and
# "neg_q_only" reasons via two different witness expressions.
_VERIFIER_SRC = textwrap.dedent(
    """
    CONDITION_LABELS = ["H_1: trivially true", "neg_Q: witness == 0"]
    N_HYP = 1
    NEG_Q_INDEX = 1

    def conditions(witness):
        return [True, witness == 0]
    """
).strip()


def _write_verifier(tmp_path: Path) -> Path:
    p = tmp_path / "tiny_verifier.py"
    p.write_text(_VERIFIER_SRC, encoding="utf-8")
    return p


def _make_cfg(tmp_path: Path, *, reward_mode: str, enable_format: bool = True) -> RLVRConfig:
    cfg = RLVRConfig()
    cfg.output_dir = str(tmp_path / "out")
    cfg.rollouts_log = "rollouts.jsonl"
    cfg.reward_mode = reward_mode
    cfg.enable_format_reward = enable_format
    return cfg


# ---------------------------------------------------------------------------
# Branch tests
# ---------------------------------------------------------------------------

def test_oracle_branch_returns_single_oracle_reward(tmp_path):
    cfg = _make_cfg(tmp_path, reward_mode="oracle")
    funcs, weights = _build_reward_funcs(cfg, Path(cfg.output_dir))
    assert len(funcs) == 1
    assert funcs[0].__name__ == "oracle_reward"
    assert weights == [cfg.verifier_reward_weight]


def test_legacy_with_format_returns_two_funcs(tmp_path):
    cfg = _make_cfg(tmp_path, reward_mode="legacy", enable_format=True)
    funcs, weights = _build_reward_funcs(cfg, Path(cfg.output_dir))
    assert len(funcs) == 2
    names = [fn.__name__ for fn in funcs]
    assert names[0] == "verifier_reward"
    assert names[1] == "format_reward"
    assert weights == [cfg.verifier_reward_weight, cfg.format_reward_weight]


def test_legacy_without_format_returns_one_func(tmp_path):
    cfg = _make_cfg(tmp_path, reward_mode="legacy", enable_format=False)
    funcs, weights = _build_reward_funcs(cfg, Path(cfg.output_dir))
    assert len(funcs) == 1
    assert funcs[0].__name__ == "verifier_reward"
    assert weights == [cfg.verifier_reward_weight]


def test_invalid_reward_mode_raises(tmp_path):
    cfg = _make_cfg(tmp_path, reward_mode="bogus")
    with pytest.raises(ValueError, match="reward_mode"):
        _build_reward_funcs(cfg, Path(cfg.output_dir))


# ---------------------------------------------------------------------------
# End-to-end: oracle reward fn callable via TRL-shaped kwargs
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_oracle_reward_fn_kwargs_path(tmp_path):
    """Drive the oracle reward fn the way TRL would: parallel-list kwargs."""
    cfg = _make_cfg(tmp_path, reward_mode="oracle")
    verifier_path = _write_verifier(tmp_path)
    funcs, _ = _build_reward_funcs(cfg, Path(cfg.output_dir))
    fn = funcs[0]

    # Two rollouts against the *same* prompt: one full success (witness=0,
    # both conditions True -> reason='success'), one parse-error (no tag).
    completions = [
        [{"role": "assistant", "content": "<reasoning>x=0</reasoning>\n[COUNTEREXAMPLE: 0]"}],
        [{"role": "assistant", "content": "I refuse"}],
    ]
    kwargs = {
        "verifier_module_path": [str(verifier_path), str(verifier_path)],
        "n_hyp": [1, 1],
        "neg_q_index": [1, 1],
        "n_conditions": [2, 2],
    }

    rewards = fn(prompts=[None, None], completions=completions, **kwargs)
    assert len(rewards) == 2
    # Full success => α*1 + β*1 + γ*1 = 0.25 + 0.60 + 0.10 = 0.95.
    assert rewards[0] == pytest.approx(0.95, abs=1e-9)
    # No tag => -ε = -1.0.
    assert rewards[1] == pytest.approx(-1.0, abs=1e-9)

    # Rollouts log was written.
    log_path = Path(cfg.output_dir) / cfg.rollouts_log
    assert log_path.exists()
    contents = log_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(contents) == 2


def test_oracle_kwargs_missing_metadata_raises(tmp_path):
    cfg = _make_cfg(tmp_path, reward_mode="oracle")
    funcs, _ = _build_reward_funcs(cfg, Path(cfg.output_dir))
    fn = funcs[0]
    completions = [[{"role": "assistant", "content": "[COUNTEREXAMPLE: 0]"}]]
    # Deliberately omit the four required kwargs to check the error path.
    with pytest.raises(KeyError, match="oracle reward requires per-prompt kwargs"):
        fn(prompts=[None], completions=completions)
