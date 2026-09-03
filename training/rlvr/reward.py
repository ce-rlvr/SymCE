"""
Reward functions for GRPO training.

verifier_reward(prompts, completions, **kwargs) -> list[float]
    Dense reward derived from src/verifier.py.execute_and_verify.

format_reward(prompts, completions, **kwargs) -> list[float]
    Cheap structural reward (does the completion contain a python code fence
    and at least one assert?). Optional, gated by RLVRConfig.enable_format_reward.

Both follow the TRL reward-fn signature: take a list of completions in
conversational form (`completions[i][0]["content"]`) and return a list of
floats of equal length. They accept and ignore extra **kwargs (prompts,
completion_ids, trainer_state, ...) for forward-compat with TRL.
"""

from __future__ import annotations

import json
import logging
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

# Make `src/` importable so we can call execute_and_verify regardless of
# where the training entrypoint is launched from.
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
if str(_REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT / "src"))

from src.verifier import execute_and_verify  # noqa: E402

from training.rlvr.config import REWARD_WEIGHTS  # noqa: E402

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Code extraction
# ---------------------------------------------------------------------------

# Greedy-but-anchored fence match. Prefers ```python fences but falls back to
# any triple-fenced block. Multiple fences in one completion -> take the first.
_FENCE_PY = re.compile(r"```(?:python|py)\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)
_FENCE_ANY = re.compile(r"```\s*\n?(.*?)```", re.DOTALL)


def extract_code(text: str) -> str | None:
    """
    Pull the first python code block out of an LLM completion.

    Returns the inner code (no fences) or None if nothing fence-shaped is
    present. Whitespace is stripped on both sides.
    """
    if not isinstance(text, str) or not text:
        return None
    m = _FENCE_PY.search(text)
    if not m:
        m = _FENCE_ANY.search(text)
    if not m:
        return None
    code = m.group(1).strip()
    return code or None


# ---------------------------------------------------------------------------
# Verifier -> scalar mapping
# ---------------------------------------------------------------------------

def _classify(verifier_result: dict) -> str:
    """Return the REWARD_WEIGHTS key for a given verifier result dict.

    Priority order (most severe / most informative first):

    1. safety_invalid   -  blocked before execution; return immediately.
    2. syntax_error     -  execution-based check, more informative than a static
                        negation scan; a syntax-broken script cannot satisfy hyps.
    3. timed_out        -  execution-based; the search loop was too slow.
    4. success          -  exit code 0. If negation form is also missing the model
                        likely *proved* the conclusion (wrong direction), which is
                        caught as execution_ok_no_negation (-0.2) rather than
                        success (+1.0). This case gives partial credit: the model
                        did run hypothesis checks but got the logical direction wrong.
    5. runtime_error    -  AssertionError or other non-zero exit after syntax passes.
    6. negation_invalid - no execution error but the static negation scan failed;
                         weaker signal than runtime failures.
    7. default          -  fallback.

    NOTE: We intentionally check execution-based flags (syntax_error, timed_out,
    runtime_error) BEFORE the static negation scan so that a script that is
    both syntactically broken AND lacks a negation assertion is classified as
    syntax_error (worse, -1.0) rather than negation_invalid (-0.5).
    """
    if not verifier_result.get("safety_ok", True):
        return "safety_invalid"
    if verifier_result.get("syntax_error", False):
        return "syntax_error"
    if verifier_result.get("timed_out", False):
        return "timed_out"
    if verifier_result.get("success", False):
        # Script exited 0 but lacks a negation-form assertion.
        # The model probably satisfied the hypotheses but asserted the conclusion
        # is True (wrong direction). Give partial credit (-0.2) vs. hard failure.
        if not verifier_result.get("negation_form_ok", False):
            return "execution_ok_no_negation"
        return "success"
    if verifier_result.get("runtime_error", False):
        return "runtime_error"
    # Script failed for an unclassified reason AND lacks negation form.
    if not verifier_result.get("negation_form_ok", False):
        return "negation_invalid"
    return "default"


def score_completion(text: str, weights: dict[str, float] | None = None) -> tuple[float, str, dict]:
    """
    Score a single completion. Returns (reward, reason, verifier_result_or_empty).

    Catches verifier OS-level exceptions so the training loop never crashes
    on a bad completion.
    """
    w = weights or REWARD_WEIGHTS
    code = extract_code(text)
    if code is None:
        return w["no_code"], "no_code", {}

    try:
        result = execute_and_verify(code)
    except Exception as exc:  # OS-level / unexpected failure
        logger.exception("verifier raised: %s", exc)
        return w["default"], "verifier_exception", {"exception": repr(exc)}

    reason = _classify(result)
    return w.get(reason, w["default"]), reason, result


# ---------------------------------------------------------------------------
# Rollout logger (per-completion JSONL trace for debugging RL collapse)
# ---------------------------------------------------------------------------

class RolloutLogger:
    """Thread-safe append-only JSONL writer for per-completion telemetry."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._call_count = 0

    def log(self, record: dict) -> None:
        with self._lock:
            self._call_count += 1
            record = {"_rollout_idx": self._call_count, "_t": time.time(), **record}
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(record, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Reward function factories (closures over config)
# ---------------------------------------------------------------------------

def _completion_text(completion: Any) -> str:
    """Pull the assistant text out of a TRL completion entry."""
    if isinstance(completion, list) and completion:
        first = completion[0]
        if isinstance(first, dict):
            return str(first.get("content", ""))
        return str(first)
    if isinstance(completion, dict):
        return str(completion.get("content", ""))
    return str(completion)


def _prompt_text(prompt: Any) -> str:
    """Best-effort extraction of the user message from a prompt for logging."""
    if isinstance(prompt, list):
        for msg in reversed(prompt):
            if isinstance(msg, dict) and msg.get("role") == "user":
                return str(msg.get("content", ""))[:500]
    if isinstance(prompt, str):
        return prompt[:500]
    return ""


def make_verifier_reward(
    weights: dict[str, float] | None = None,
    rollout_logger: RolloutLogger | None = None,
    pool_workers: int = 4,
):
    """
    Build a TRL-compatible reward function bound to a fixed reward table and
    optional rollout logger.

    The function signature follows TRL's protocol:
        reward_fn(prompts, completions, **kwargs) -> list[float]
    where `completions` is `list[list[{"role": ..., "content": ...}]]` for
    conversational data.
    """
    weights = weights or REWARD_WEIGHTS

    def _score_one(text: str) -> tuple[float, str, dict]:
        return score_completion(text, weights)

    def verifier_reward(
        prompts: list | None = None,
        completions: list | None = None,
        **kwargs,
    ) -> list[float]:
        completions = completions or []
        prompts = prompts or [None] * len(completions)
        texts = [_completion_text(c) for c in completions]

        # Parallelise the sandbox subprocess calls. The GIL is released during
        # subprocess.run, so threading gives near-linear speedup.
        if len(texts) > 1 and pool_workers > 1:
            with ThreadPoolExecutor(max_workers=min(pool_workers, len(texts))) as pool:
                results = list(pool.map(_score_one, texts))
        else:
            results = [_score_one(t) for t in texts]

        rewards = [r for r, _, _ in results]

        if rollout_logger is not None:
            trainer_state = kwargs.get("trainer_state")
            global_step = getattr(trainer_state, "global_step", None) if trainer_state else None
            for i, ((reward, reason, vresult), text, prompt) in enumerate(
                zip(results, texts, prompts)
            ):
                rollout_logger.log({
                    "global_step": global_step,
                    "in_batch_idx": i,
                    "reward": reward,
                    "reason": reason,
                    "prompt_user": _prompt_text(prompt),
                    "completion": text,
                    "verifier": {
                        k: vresult.get(k)
                        for k in (
                            "success", "exit_code", "timed_out",
                            "syntax_error", "runtime_error",
                            "negation_form_ok", "safety_ok",
                            "error_message",
                        )
                        if k in vresult
                    },
                })

        return rewards

    verifier_reward.__name__ = "verifier_reward"
    return verifier_reward


# ---------------------------------------------------------------------------
# Optional secondary format reward
# ---------------------------------------------------------------------------

_HAS_PY_FENCE = re.compile(r"```(?:python|py)\b", re.IGNORECASE)
_HAS_ASSERT = re.compile(r"\bassert\b")


def format_reward(prompts=None, completions=None, **kwargs) -> list[float]:
    """
    +1.0 if the completion contains a ```python fence AND at least one
    `assert` keyword (a cheap proxy for "looks like a counterexample script").
    Otherwise 0.0. Final contribution is scaled via GRPOConfig.reward_weights.
    """
    completions = completions or []
    out: list[float] = []
    for c in completions:
        text = _completion_text(c)
        ok = bool(_HAS_PY_FENCE.search(text)) and bool(_HAS_ASSERT.search(text))
        out.append(1.0 if ok else 0.0)
    return out
