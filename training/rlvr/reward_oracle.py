"""
Oracle-based reward function for the v2.0 task framing.

The v2.0 policy emits a free-form chain of thought followed by a single tagged
line:

    <reasoning>...</reasoning>
    [COUNTEREXAMPLE: <expression>]

`<expression>` is a Python expression that the per-theorem verifier evaluates
inside its own setup namespace (see ``src/oracle/sandbox.run_oracle``). The
sentinel ``[COUNTEREXAMPLE: NONE]`` lets the model decline to disprove; in
Stage 1 (``counterexample_only``) that is a "gave up" signal and is penalised.

This module is intentionally a *pure-function* contribution to P2:

- ``parse_counterexample_tag(text)`` — strict, case-sensitive tag extractor
  (last well-formed tag wins; single-line; bracket-balanced).
- ``compute_reward_oracle(record, completion_text, weights, task_mode)`` — the
  deterministic per-rollout reward; pulls verifier metadata off the record and
  delegates execution to ``run_oracle``.
- ``make_oracle_reward(...)`` — a TRL-shaped factory that *expects* per-prompt
  verifier metadata to arrive via ``**kwargs`` as parallel lists. It is not
  yet wired into ``training/rlvr/trainer.py``; that is P4.

The reward formula (per PROPOSAL §3.2, default weights from ``full_run.yaml``):

    r = α · (s_hyp / n_hyp)              # remaining-hypothesis credit
      + β · q_neg                          # negated-conclusion credit (the disproof)
      + γ · format_ok                      # structural format bonus
      − δ · gave_up_on_false               # NONE on a FALSE conjecture (Stage 1 only)
      − ε · (1 − parse_ok)                 # parse / namespace error

The legacy ``_classify`` / ``REWARD_WEIGHTS`` path stays in ``reward.py`` and
remains the default until P4 lands the trainer/data wiring.
"""

from __future__ import annotations

import json
import logging
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

# Ensure `src.oracle` is importable regardless of cwd.
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.oracle.sandbox import OracleResult, run_oracle  # noqa: E402

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Tag parser
# ─────────────────────────────────────────────────────────────────────────────

# Case-sensitive opener. We do not accept lowercase, missing colon, or
# surrounding whitespace inside the opener itself — those count as no-tag.
_TAG_OPENER: str = "[COUNTEREXAMPLE:"
_NONE_SENTINEL: str = "NONE"


@dataclass(frozen=True)
class ParsedTag:
    """Outcome of parsing a model completion for the structured tag.

    Attributes:
        payload:   The witness expression string (stripped) when a well-formed
                   tag was found, or the literal "NONE" sentinel, or None when
                   no parseable tag was present.
        format_ok: True iff at least one bracket-balanced single-line opener was
                   found and its payload was non-empty after stripping.
        is_none:   True iff ``payload == "NONE"`` exactly (case-sensitive).
    """

    payload: Optional[str]
    format_ok: bool
    is_none: bool


def _try_extract(text: str, opener_idx: int) -> Optional[str]:
    """From a tag-opener position, find the matching ``]`` on the same line.

    Returns the raw payload (text between the colon and the matching close
    bracket) or None if the tag spans a newline or has unbalanced brackets.

    The matching ``]`` is found by depth-counting: ``[`` increments, ``]``
    decrements, starting from depth=1 (the opener's ``[`` is already counted).
    A bare expression like ``Matrix([[1,0],[0,1]])`` therefore yields the
    correct closing bracket on the outermost level.
    """
    n = len(text)
    # The ':' is the last character of the opener; payload starts after it.
    colon = opener_idx + len(_TAG_OPENER) - 1
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


def parse_counterexample_tag(text: str) -> ParsedTag:
    """Extract the last well-formed ``[COUNTEREXAMPLE: <expr>]`` tag.

    Semantics (strict, by design):

    - Case-sensitive: ``[counterexample: ...]`` does NOT match.
    - Single-line: the tag must open and close on the same physical line.
    - Bracket-balanced: inner ``[`` / ``]`` are allowed and counted.
    - Multiple tags: the LAST well-formed occurrence wins. (A model that
      writes "candidate: ..." and then commits to a final answer is rewarded
      on the final.)
    - Empty payload after stripping → not format-ok; falls back to earlier
      candidates if any, otherwise reports no tag.
    - Whitespace around the payload is stripped.
    - ``NONE`` (case-sensitive, exact, after stripping) is recognised as a
      sentinel.
    """
    if not isinstance(text, str) or not text:
        return ParsedTag(payload=None, format_ok=False, is_none=False)

    # Collect all opener indices (occurrences of `[COUNTEREXAMPLE:`).
    opener_positions: list[int] = []
    cursor = 0
    while True:
        idx = text.find(_TAG_OPENER, cursor)
        if idx == -1:
            break
        opener_positions.append(idx)
        cursor = idx + 1
    if not opener_positions:
        return ParsedTag(payload=None, format_ok=False, is_none=False)

    # Try in reverse — last well-formed match wins.
    for opener_idx in reversed(opener_positions):
        raw = _try_extract(text, opener_idx)
        if raw is None:
            continue
        payload = raw.strip()
        if not payload:
            continue
        return ParsedTag(
            payload=payload,
            format_ok=True,
            is_none=(payload == _NONE_SENTINEL),
        )

    return ParsedTag(payload=None, format_ok=False, is_none=False)


# ─────────────────────────────────────────────────────────────────────────────
# Reward dataclasses + defaults
# ─────────────────────────────────────────────────────────────────────────────

# Default oracle reward weights (PROPOSAL §3.2).
ORACLE_REWARD_WEIGHTS_DEFAULT: dict[str, float] = {
    "alpha":   0.25,   # weight on (s_hyp / n_hyp)
    "beta":    0.60,   # weight on q_neg (the disproof)
    "gamma":   0.10,   # weight on format_ok
    "delta":   0.50,   # penalty on NONE-on-FALSE (Stage 1)
    "epsilon": 1.00,   # penalty on parse / namespace error
}

# Sparse outcome-only preset used in the RQ2 ablation (dense vs sparse).
# Recovers a binary signal: +β on disproof, −ε on parse error, 0 elsewhere.
ORACLE_REWARD_WEIGHTS_SPARSE: dict[str, float] = {
    "alpha":   0.0,
    "beta":    1.0,
    "gamma":   0.0,
    "delta":   0.0,
    "epsilon": 1.0,
}


@dataclass
class RewardBreakdown:
    """Structured per-rollout reward decomposition.

    All booleans are stored as Python bools; the integer ``q_neg`` is the value
    actually used in the formula. ``oracle_*`` fields mirror ``OracleResult``
    so that downstream telemetry need not re-import sandbox internals.
    """

    total: float
    format_ok: bool
    parse_ok: bool
    is_none: bool
    gave_up: bool
    s_hyp: int
    n_hyp: int
    q_neg: int
    n_conditions: int
    conditions: Optional[list[bool]]
    witness_expr: Optional[str]
    oracle_error: Optional[str]
    oracle_timed_out: bool
    oracle_elapsed_ms: int
    weights_used: dict[str, float]
    task_mode: str
    reason: str   # short label for telemetry / dashboards

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ─────────────────────────────────────────────────────────────────────────────
# Core reward computation
# ─────────────────────────────────────────────────────────────────────────────

_VALID_TASK_MODES: tuple[str, ...] = (
    "counterexample_only",
    "counterexample_or_none",
    "classify_then_generate",
)


def _validate_weights(weights: dict[str, float]) -> dict[str, float]:
    required = ("alpha", "beta", "gamma", "delta", "epsilon")
    missing = [k for k in required if k not in weights]
    if missing:
        raise KeyError(
            f"oracle reward weights missing keys: {missing}; "
            f"expected {list(required)}"
        )
    return {k: float(weights[k]) for k in required}


def _extract_verifier_meta(record: dict) -> dict:
    """Pull the verifier metadata out of a v2 record. Raises if shape is wrong."""
    verifier = record.get("verifier")
    if not isinstance(verifier, dict):
        raise KeyError("record is missing 'verifier' dict")
    for key in ("module_path", "n_hyp", "neg_q_index", "n_conditions"):
        if key not in verifier:
            raise KeyError(f"record['verifier'] is missing '{key}'")
    return verifier


def compute_reward_oracle(
    record: dict,
    completion_text: str,
    weights: dict[str, float] | None = None,
    task_mode: str = "counterexample_only",
    timeout_seconds: float = 8.0,
) -> RewardBreakdown:
    """Score one completion against the record's independent verifier.

    Args:
        record:           A v2 JSONL record (must contain ``verifier`` subdict).
        completion_text:  The model's raw output string.
        weights:          Mapping with keys {alpha, beta, gamma, delta, epsilon};
                          defaults to ORACLE_REWARD_WEIGHTS_DEFAULT.
        task_mode:        Currently only ``"counterexample_only"`` is wired in
                          P2; other modes raise NotImplementedError until P3+.
        timeout_seconds:  Hard subprocess timeout for the oracle.

    Returns:
        A RewardBreakdown with ``total`` and per-condition diagnostics.
    """
    if task_mode not in _VALID_TASK_MODES:
        raise ValueError(
            f"task_mode={task_mode!r} not in {_VALID_TASK_MODES!r}"
        )
    if task_mode != "counterexample_only":
        # Stage 2 / Stage 3 framing is deferred to P7 — see docs/PLAN.md.
        raise NotImplementedError(
            f"task_mode={task_mode!r} is reserved for P7; "
            "P2 implements only 'counterexample_only'."
        )

    w = _validate_weights(weights or ORACLE_REWARD_WEIGHTS_DEFAULT)
    alpha, beta, gamma, delta, epsilon = (
        w["alpha"], w["beta"], w["gamma"], w["delta"], w["epsilon"],
    )

    verifier = _extract_verifier_meta(record)
    n_hyp = int(verifier["n_hyp"])
    neg_q_index = int(verifier["neg_q_index"])
    n_conditions = int(verifier["n_conditions"])
    module_path = str(verifier["module_path"])

    parsed = parse_counterexample_tag(completion_text)
    format_ok = parsed.format_ok

    def _bd(
        *,
        total: float,
        parse_ok: bool,
        s_hyp: int,
        q_neg: int,
        conditions: Optional[list[bool]],
        witness: Optional[str],
        oracle_err: Optional[str],
        oracle_timed_out: bool,
        oracle_ms: int,
        gave_up: bool,
        reason: str,
    ) -> RewardBreakdown:
        return RewardBreakdown(
            total=float(total),
            format_ok=bool(format_ok),
            parse_ok=bool(parse_ok),
            is_none=bool(parsed.is_none),
            gave_up=bool(gave_up),
            s_hyp=int(s_hyp),
            n_hyp=int(n_hyp),
            q_neg=int(q_neg),
            n_conditions=int(n_conditions),
            conditions=conditions,
            witness_expr=witness,
            oracle_error=oracle_err,
            oracle_timed_out=bool(oracle_timed_out),
            oracle_elapsed_ms=int(oracle_ms),
            weights_used=dict(w),
            task_mode=task_mode,
            reason=reason,
        )

    # ── Case 1: no tag found ─────────────────────────────────────────────────
    if parsed.payload is None:
        return _bd(
            total=-epsilon,
            parse_ok=False,
            s_hyp=0,
            q_neg=0,
            conditions=None,
            witness=None,
            oracle_err=None,
            oracle_timed_out=False,
            oracle_ms=0,
            gave_up=False,
            reason="no_tag",
        )

    # ── Case 2: NONE sentinel on a FALSE conjecture (Stage 1) ────────────────
    # parse_ok=True by convention (sentinel does not require eval).
    if parsed.is_none:
        total = -delta + gamma * (1 if format_ok else 0)
        return _bd(
            total=total,
            parse_ok=True,
            s_hyp=0,
            q_neg=0,
            conditions=None,
            witness=_NONE_SENTINEL,
            oracle_err=None,
            oracle_timed_out=False,
            oracle_ms=0,
            gave_up=True,
            reason="none_on_false",
        )

    # ── Case 3: evaluate the witness expression in the oracle ────────────────
    oracle: OracleResult = run_oracle(
        verifier_module_path=module_path,
        witness_expr=parsed.payload,
        n_conditions=n_conditions,
        timeout_seconds=timeout_seconds,
    )

    if not oracle.parse_ok or oracle.conditions is None:
        return _bd(
            total=-epsilon,
            parse_ok=False,
            s_hyp=0,
            q_neg=0,
            conditions=oracle.conditions,
            witness=parsed.payload,
            oracle_err=oracle.error,
            oracle_timed_out=oracle.timed_out,
            oracle_ms=oracle.elapsed_ms,
            gave_up=False,
            reason="oracle_parse_error",
        )

    conds = list(oracle.conditions)

    # Schema sanity: the verifier metadata in the record must agree with what
    # the verifier module actually returned. Mismatch is a verifier-quality
    # bug; we surface it via a parse-level penalty rather than silently
    # ignoring trailing/missing booleans.
    if len(conds) != n_conditions:
        return _bd(
            total=-epsilon,
            parse_ok=False,
            s_hyp=0,
            q_neg=0,
            conditions=conds,
            witness=parsed.payload,
            oracle_err=(
                f"ConditionLengthMismatch: oracle returned {len(conds)} "
                f"booleans, record declares n_conditions={n_conditions}"
            ),
            oracle_timed_out=oracle.timed_out,
            oracle_ms=oracle.elapsed_ms,
            gave_up=False,
            reason="condition_length_mismatch",
        )

    if not (0 <= neg_q_index < len(conds)):
        return _bd(
            total=-epsilon,
            parse_ok=False,
            s_hyp=0,
            q_neg=0,
            conditions=conds,
            witness=parsed.payload,
            oracle_err=(
                f"InvalidNegQIndex: {neg_q_index} out of range for "
                f"{len(conds)} conditions"
            ),
            oracle_timed_out=oracle.timed_out,
            oracle_ms=oracle.elapsed_ms,
            gave_up=False,
            reason="invalid_neg_q_index",
        )

    # Hypothesis booleans live at conds[0:n_hyp]. They may overlap neg_q_index
    # only when n_hyp == 0 (rare, and α-term is 0 anyway).
    if n_hyp > 0:
        s_hyp = sum(1 for b in conds[:n_hyp] if b)
        hyp_term = alpha * (s_hyp / n_hyp)
    else:
        s_hyp = 0
        hyp_term = 0.0
    q_neg = 1 if conds[neg_q_index] else 0

    total = hyp_term + beta * q_neg + gamma * (1 if format_ok else 0)
    # parse_ok=True → ε·(1−parse_ok) = 0 → no ε contribution.

    # Reason label for telemetry / dashboards.
    if q_neg == 1 and (n_hyp == 0 or s_hyp == n_hyp):
        reason = "success"
    elif q_neg == 1:
        reason = "neg_q_only"   # disproved but not all hyps satisfied
    elif n_hyp > 0 and s_hyp == n_hyp:
        reason = "hyp_only"     # the "Learning to Disprove" failure mode
    else:
        reason = "partial"

    return _bd(
        total=total,
        parse_ok=True,
        s_hyp=s_hyp,
        q_neg=q_neg,
        conditions=conds,
        witness=parsed.payload,
        oracle_err=None,
        oracle_timed_out=oracle.timed_out,
        oracle_ms=oracle.elapsed_ms,
        gave_up=False,
        reason=reason,
    )


# ─────────────────────────────────────────────────────────────────────────────
# TRL-shaped factory (kwargs-driven; not wired into trainer.py in P2)
# ─────────────────────────────────────────────────────────────────────────────

# Per-prompt verifier metadata columns the reward fn expects in TRL kwargs.
# (P3/P4 will update training/rlvr/data.py to emit these.)
_REQUIRED_RECORD_KWARGS: tuple[str, ...] = (
    "verifier_module_path",
    "n_hyp",
    "neg_q_index",
    "n_conditions",
)


def _completion_text(completion: Any) -> str:
    """Pull the assistant text out of a TRL conversational completion entry."""
    if isinstance(completion, list) and completion:
        first = completion[0]
        if isinstance(first, dict):
            return str(first.get("content", ""))
        return str(first)
    if isinstance(completion, dict):
        return str(completion.get("content", ""))
    return str(completion)


def _records_from_kwargs(n_rollouts: int, kwargs: dict[str, Any]) -> list[dict]:
    """Reconstruct minimal record dicts from per-prompt kwargs lists.

    TRL forwards any dataset column that is not in {prompt, completion} as a
    kwarg whose value is a list of length ``n_rollouts``. We expect the data
    loader (P3) to emit one column per required field; here we just validate
    + zip.
    """
    missing = [k for k in _REQUIRED_RECORD_KWARGS if k not in kwargs]
    if missing:
        raise KeyError(
            f"oracle reward requires per-prompt kwargs {list(_REQUIRED_RECORD_KWARGS)}; "
            f"missing: {missing}. Make sure the dataset emits these columns "
            "(see training/rlvr/data.py in P3+)."
        )
    cols = {k: kwargs[k] for k in _REQUIRED_RECORD_KWARGS}
    for k, v in cols.items():
        if not isinstance(v, (list, tuple)) or len(v) != n_rollouts:
            raise ValueError(
                f"kwargs[{k!r}] must be a list of length {n_rollouts}; "
                f"got {type(v).__name__} of length "
                f"{len(v) if hasattr(v, '__len__') else 'N/A'}"
            )

    records: list[dict] = []
    for i in range(n_rollouts):
        records.append({
            "verifier": {
                "module_path": cols["verifier_module_path"][i],
                "n_hyp": cols["n_hyp"][i],
                "neg_q_index": cols["neg_q_index"][i],
                "n_conditions": cols["n_conditions"][i],
            }
        })
    return records


class OracleRolloutLogger:
    """Thread-safe append-only JSONL writer for oracle reward telemetry.

    One record per rollout; columns are RewardBreakdown.to_dict() plus
    context (global_step, in_batch_idx, prompt_user, completion).
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._counter = 0

    def log(self, record: dict[str, Any]) -> None:
        with self._lock:
            self._counter += 1
            payload = {"_rollout_idx": self._counter, "_t": time.time(), **record}
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(payload, ensure_ascii=False, default=str) + "\n")


def _prompt_user_text(prompt: Any) -> str:
    """Best-effort extraction of the user message from a prompt for logging."""
    if isinstance(prompt, list):
        for msg in reversed(prompt):
            if isinstance(msg, dict) and msg.get("role") == "user":
                return str(msg.get("content", ""))[:500]
    if isinstance(prompt, str):
        return prompt[:500]
    return ""


def _length_penalty(
    n_tokens: int,
    *,
    threshold: int,
    per_token: float,
    cap: float,
) -> float:
    """Soft hinge penalty on completion length, capped at ``cap``.

    Returns a non-negative scalar to be subtracted from the reward. The hinge
    is zero up to ``threshold`` and grows linearly with slope ``per_token``
    until it saturates at ``cap``.
    """
    if n_tokens <= threshold or per_token <= 0.0 or cap <= 0.0:
        return 0.0
    raw = per_token * (n_tokens - threshold)
    return float(min(cap, raw))


def make_oracle_reward(
    weights: dict[str, float] | None = None,
    task_mode: str = "counterexample_only",
    rollout_logger: OracleRolloutLogger | None = None,
    pool_workers: int = 4,
    timeout_seconds: float = 8.0,
    length_penalty_enabled: bool = False,
    length_penalty_threshold: int = 600,
    length_penalty_per_token: float = 8e-4,
    length_penalty_max: float = 0.3,
):
    """Build a TRL-compatible reward function bound to the oracle path.

    The returned callable has the TRL signature

        reward_fn(prompts, completions, **kwargs) -> list[float]

    and pulls per-prompt verifier metadata off ``kwargs`` (see
    ``_REQUIRED_RECORD_KWARGS``).

    When ``length_penalty_enabled=True``, a soft-hinge penalty proportional to
    the number of generated tokens (read from TRL's ``completion_ids`` kwarg)
    is subtracted from each rollout's reward. This counters the GRPO failure
    mode where the policy grows reasoning length to chase α-credit until the
    closing tag is amputated by the budget. The penalty is logged in the
    rollout breakdown for post-hoc analysis.
    """
    w = _validate_weights(weights or ORACLE_REWARD_WEIGHTS_DEFAULT)

    def _score_one(args: tuple[dict, str]) -> RewardBreakdown:
        rec, text = args
        try:
            return compute_reward_oracle(
                record=rec,
                completion_text=text,
                weights=w,
                task_mode=task_mode,
                timeout_seconds=timeout_seconds,
            )
        except Exception as exc:  # OS-level / unexpected failure
            logger.exception("oracle reward raised: %s", exc)
            # Fail safe: return a parse-level penalty so the training loop
            # never crashes on one bad rollout.
            return RewardBreakdown(
                total=-w["epsilon"],
                format_ok=False,
                parse_ok=False,
                is_none=False,
                gave_up=False,
                s_hyp=0,
                n_hyp=int(rec.get("verifier", {}).get("n_hyp", 0) or 0),
                q_neg=0,
                n_conditions=int(rec.get("verifier", {}).get("n_conditions", 0) or 0),
                conditions=None,
                witness_expr=None,
                oracle_error=f"RewardException: {type(exc).__name__}: {exc!s}"[:300],
                oracle_timed_out=False,
                oracle_elapsed_ms=0,
                weights_used=dict(w),
                task_mode=task_mode,
                reason="reward_exception",
            )

    def oracle_reward(
        prompts: list | None = None,
        completions: list | None = None,
        **kwargs,
    ) -> list[float]:
        completions = completions or []
        prompts = prompts or [None] * len(completions)
        texts = [_completion_text(c) for c in completions]
        n = len(texts)
        if n == 0:
            return []

        records = _records_from_kwargs(n, kwargs)

        pairs = list(zip(records, texts))
        if n > 1 and pool_workers > 1:
            with ThreadPoolExecutor(max_workers=min(pool_workers, n)) as pool:
                breakdowns = list(pool.map(_score_one, pairs))
        else:
            breakdowns = [_score_one(p) for p in pairs]

        # ── Length penalty (fix 3) ────────────────────────────────────────
        # TRL forwards completion_ids as a kwarg (list of per-rollout token
        # id lists). When length_penalty_enabled is True we subtract a soft
        # hinge from each rollout's reward; the per-rollout penalty value is
        # logged so we can audit it from rollouts.jsonl.
        completion_ids = kwargs.get("completion_ids")
        completion_lengths: list[int] = [0] * n
        length_penalties: list[float] = [0.0] * n
        if isinstance(completion_ids, (list, tuple)) and len(completion_ids) == n:
            for i, ids in enumerate(completion_ids):
                try:
                    completion_lengths[i] = int(len(ids))
                except TypeError:
                    completion_lengths[i] = 0
            if length_penalty_enabled:
                for i, L in enumerate(completion_lengths):
                    length_penalties[i] = _length_penalty(
                        L,
                        threshold=length_penalty_threshold,
                        per_token=length_penalty_per_token,
                        cap=length_penalty_max,
                    )

        rewards = [bd.total - length_penalties[i] for i, bd in enumerate(breakdowns)]

        if rollout_logger is not None:
            trainer_state = kwargs.get("trainer_state")
            global_step = getattr(trainer_state, "global_step", None) if trainer_state else None
            for i, (bd, text, prompt) in enumerate(zip(breakdowns, texts, prompts)):
                rollout_logger.log({
                    "global_step": global_step,
                    "in_batch_idx": i,
                    "reward": rewards[i],
                    "reward_pre_length_penalty": bd.total,
                    "length_penalty": length_penalties[i],
                    "completion_n_tokens": completion_lengths[i],
                    "reason": bd.reason,
                    "breakdown": bd.to_dict(),
                    "prompt_user": _prompt_user_text(prompt),
                    "completion": text[:2000],   # truncate, telemetry isn't archive
                })

        return rewards

    oracle_reward.__name__ = "oracle_reward"
    return oracle_reward


__all__ = [
    "ORACLE_REWARD_WEIGHTS_DEFAULT",
    "ORACLE_REWARD_WEIGHTS_SPARSE",
    "OracleRolloutLogger",
    "ParsedTag",
    "RewardBreakdown",
    "compute_reward_oracle",
    "make_oracle_reward",
    "parse_counterexample_tag",
]
