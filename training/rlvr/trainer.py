"""
Build a TRL GRPOTrainer wired to either the legacy (v1.0) verifier reward or
the v2.0 oracle reward (independent per-theorem verifier scoring a witness
expression). The selection is controlled by ``RLVRConfig.reward_mode``:

- ``"legacy"`` — the v1.0 path. The model is expected to emit a SymPy/Z3
  *script* in a ```python fence; ``src/verifier.execute_and_verify`` runs it
  and ``training/rlvr/reward._classify`` maps the result to a scalar via
  ``REWARD_WEIGHTS``. Optionally combined with the legacy ``format_reward``
  (which greps for the fence + an ``assert`` keyword).

- ``"oracle"`` — the v2.0 path. The model is expected to emit a
  ``[COUNTEREXAMPLE: <expr>]`` tag; the per-theorem verifier evaluates the
  witness and returns one boolean per condition. The oracle reward already
  includes a ``γ·format_ok`` term for the tag, so the legacy
  ``format_reward`` is intentionally *not* attached under oracle mode
  (would double-count and pollute the dense-vs-sparse RQ2 ablation).

The trainer also writes a per-rollout JSONL telemetry trace via the matching
rollout-logger class (``RolloutLogger`` for legacy, ``OracleRolloutLogger``
for oracle).
"""

from __future__ import annotations

from pathlib import Path

from trl import GRPOConfig, GRPOTrainer

from training.rlvr.config import REWARD_WEIGHTS
from training.rlvr.reward import (
    RolloutLogger,
    format_reward,
    make_verifier_reward,
)
from training.rlvr.reward_oracle import (
    OracleRolloutLogger,
    make_oracle_reward,
)


_VALID_REWARD_MODES: tuple[str, ...] = ("legacy", "oracle")


def _build_reward_funcs(cfg, output_dir: Path):
    """Return (reward_funcs, reward_weights) for the selected reward_mode.

    Raises ValueError if cfg.reward_mode is unknown so config typos surface
    immediately rather than silently falling back to a default.
    """
    mode = getattr(cfg, "reward_mode", "legacy")
    if mode not in _VALID_REWARD_MODES:
        raise ValueError(
            f"RLVRConfig.reward_mode={mode!r} not in {_VALID_REWARD_MODES!r}"
        )

    if mode == "legacy":
        rollout_logger = RolloutLogger(output_dir / cfg.rollouts_log)
        verifier_reward = make_verifier_reward(
            weights=REWARD_WEIGHTS,
            rollout_logger=rollout_logger,
            pool_workers=cfg.reward_pool_workers,
        )
        if cfg.enable_format_reward:
            return (
                [verifier_reward, format_reward],
                [cfg.verifier_reward_weight, cfg.format_reward_weight],
            )
        return [verifier_reward], [cfg.verifier_reward_weight]

    # mode == "oracle"
    oracle_logger = OracleRolloutLogger(output_dir / cfg.rollouts_log)
    oracle_reward = make_oracle_reward(
        weights=cfg.oracle_reward_weights,
        task_mode=cfg.task_mode,
        rollout_logger=oracle_logger,
        pool_workers=cfg.reward_pool_workers,
        timeout_seconds=cfg.oracle_timeout_seconds,
        length_penalty_enabled=getattr(cfg, "length_penalty_enabled", False),
        length_penalty_threshold=getattr(cfg, "length_penalty_threshold", 600),
        length_penalty_per_token=getattr(cfg, "length_penalty_per_token", 8e-4),
        length_penalty_max=getattr(cfg, "length_penalty_max", 0.3),
    )
    # The oracle reward already includes γ·format_ok internally; we do NOT
    # attach the legacy format_reward here. The outer TRL weight stays at
    # cfg.verifier_reward_weight (default 1.0) so users can globally scale
    # the oracle signal without touching α/β/γ/δ/ε.
    return [oracle_reward], [cfg.verifier_reward_weight]


def build_trainer(cfg, model, tokenizer, train_ds, *, output_dir=None, run_name=None):
    """Build the TRL GRPOTrainer. ``output_dir``/``run_name`` are injected by the
    entry point so the v2 run-dir layout (runs/rlvr/<auto-name>/) takes effect
    without round-tripping through ``cfg.output_dir``."""
    output_dir = Path(output_dir) if output_dir is not None else Path(cfg.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    reward_funcs, reward_weights = _build_reward_funcs(cfg, output_dir)

    # ── Stop strings (fix 1) ────────────────────────────────────────────────
    # Forwarded into TRL → vLLM SamplingParams.stop (or HF
    # GenerationConfig.stop_strings, depending on backend). Empty list = leave
    # TRL's default generation behaviour intact.
    stop_strings = list(getattr(cfg, "stop_strings", []) or [])
    generation_kwargs = {"stop": stop_strings} if stop_strings else None

    grpo_cfg = GRPOConfig(
        output_dir=str(output_dir),
        run_name=run_name or None,
        # ── Generation ──────────────────────────────────────────────────────
        num_generations=cfg.num_generations,
        max_prompt_length=cfg.max_prompt_length,
        max_completion_length=cfg.max_completion_length,
        temperature=cfg.temperature,
        top_p=cfg.top_p,
        generation_kwargs=generation_kwargs,
        # ── Optimisation ────────────────────────────────────────────────────
        per_device_train_batch_size=cfg.per_device_train_batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        max_steps=cfg.max_steps,
        num_train_epochs=cfg.num_train_epochs,
        learning_rate=cfg.learning_rate,
        warmup_ratio=cfg.warmup_ratio,
        lr_scheduler_type=cfg.lr_scheduler_type,
        optim=cfg.optim,
        weight_decay=cfg.weight_decay,
        max_grad_norm=cfg.max_grad_norm,
        beta=cfg.beta,
        epsilon=cfg.epsilon,
        # ── Reward weights (matches reward_funcs order) ─────────────────────
        reward_weights=reward_weights,
        # ── Precision / VRAM ────────────────────────────────────────────────
        bf16=True,
        fp16=False,
        gradient_checkpointing=False,    # Unsloth handles this internally
        # ── vLLM ────────────────────────────────────────────────────────────
        use_vllm=cfg.use_vllm,
        # ── Logging / saving ────────────────────────────────────────────────
        logging_steps=cfg.logging_steps,
        log_completions=cfg.log_completions,
        save_strategy=cfg.save_strategy,
        save_steps=cfg.save_steps,
        save_total_limit=cfg.save_total_limit,
        report_to=cfg.report_to,
        seed=cfg.seed,
    )

    trainer = GRPOTrainer(
        model=model,
        processing_class=tokenizer,
        reward_funcs=reward_funcs,
        args=grpo_cfg,
        train_dataset=train_ds,
    )
    return trainer
