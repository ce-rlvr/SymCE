"""
RLVR (GRPO) training configuration.

REWARD_WEIGHTS lives at module scope so reward-shaping ablations only require
editing this dict (or passing --reward-* flags). Priority order is enforced
in training/rlvr/reward.py — see the docstring there.
"""

import json
from dataclasses import asdict, dataclass, field, fields
from typing import List

# Oracle-mode reward weights are defined in training.rlvr.reward_oracle (single
# source of truth — that's where the formula actually consumes them). Re-export
# here so callers that already do `from training.rlvr.config import
# ORACLE_REWARD_WEIGHTS_DEFAULT` keep working without an import shuffle.
from training.rlvr.reward_oracle import (  # noqa: F401
    ORACLE_REWARD_WEIGHTS_DEFAULT,
    ORACLE_REWARD_WEIGHTS_SPARSE,
)


# ─────────────────────────────────────────────────────────────────────────────
# Legacy (v1.0) reward shaping table. Used by reward._classify() under
# `reward_mode: legacy`. The v2.0 oracle path (`reward_mode: oracle`, the
# `full_run.yaml` default) uses ORACLE_REWARD_WEIGHTS_DEFAULT instead — see
# training/rlvr/reward_oracle.py.
#
# Classification priority is enforced in reward._classify():
#   1. no_code                → returned without invoking the verifier.
#   2. safety_invalid         → blocked by static safety check, never executed.
#   3. syntax_error           → SyntaxError in stderr (execution-based).
#   4. timed_out              → 5 s sandbox timeout.
#   5. success                → exit code 0 AND negation_form_ok.
#   6. execution_ok_no_negation → exit code 0 but negation_form_ok=False.
#                               Partial credit: hypotheses were likely satisfied
#                               but the conclusion was asserted True (wrong direction).
#   7. runtime_error          → AssertionError or other non-zero exit.
#   8. negation_invalid       → no execution error, static negation scan failed.
#   9. default                → none of the above (e.g. ImportError).
#
# To ablate reward shaping, replace all non-success values with -1.0.
# ─────────────────────────────────────────────────────────────────────────────
REWARD_WEIGHTS: dict[str, float] = {
    "no_code":                  -1.0,
    "safety_invalid":           -1.0,
    "syntax_error":             -1.0,   # hardest failure: model can't even produce valid Python
    "timed_out":                -0.8,   # valid Python but search too slow
    "runtime_error":            -0.5,   # valid Python, some assertion failed
    "negation_invalid":         -0.5,   # unknown error + no negation form
    "execution_ok_no_negation": -0.2,   # ran OK but logical direction wrong (partial credit)
    "success":                  +1.0,   # exit 0 AND negation_form_ok
    "default":                   0.0,
}


@dataclass
class RLVRConfig:
    # ── Resume from SFT ──────────────────────────────────────────────────────
    # Must match the SFT output_dir + "/lora". Keep in sync with SFTConfig.
    sft_checkpoint: str = "checkpoints/sft/qwen3-4b-r16-bf16/lora"

    # ── Model ────────────────────────────────────────────────────────────────
    max_seq_length: int = 2048
    dtype: str = "bfloat16"
    load_in_4bit: bool = False
    chat_template: str = "auto"  # "auto" or a concrete Unsloth chat template

    # ── vLLM ─────────────────────────────────────────────────────────────────
    use_vllm: bool = False
    vllm_gpu_memory_utilization: float = 0.5
    max_lora_rank: int = 16   # must match SFT lora_r when fast_inference is on

    # ── Data ─────────────────────────────────────────────────────────────────
    train_jsonl: str = "data/rlvr_prompts.jsonl"

    # ── GRPO generation ──────────────────────────────────────────────────────
    # G=8: larger group → better advantage estimation (more rollouts to compare
    # against per prompt), at the cost of higher VRAM. 8 is a good balance for
    # a 1.5B model. Do NOT reduce below 4 or GRPO has too little diversity.
    num_generations: int = 8
    max_prompt_length: int = 1024
    max_completion_length: int = 1024
    # temperature=1.0 is mandatory for GRPO rollouts: the group of completions
    # MUST be diverse so different reward outcomes can be compared. temperature=0
    # collapses all G rollouts to the same text → advantage variance = 0 → no update.
    temperature: float = 1.0
    top_p: float = 1.0

    # Extra stop strings forwarded to vLLM SamplingParams (or HF GenerationConfig)
    # via TRL's GRPOConfig.generation_kwargs["stop"]. Useful for cutting off
    # learned drift past the [COUNTEREXAMPLE: …] tag (e.g. `<tool_call>`,
    # `\boxed{`). Empty list → leave generation_kwargs untouched.
    stop_strings: List[str] = field(default_factory=list)

    # ── Length penalty (fix 3) ───────────────────────────────────────────────
    # When enabled, subtracts a soft penalty from each rollout's reward once
    # its completion exceeds `length_penalty_threshold` tokens. The penalty is
    #     min(length_penalty_max,
    #         length_penalty_per_token * max(0, len_tokens - threshold))
    # The default (per_token=8e-4, threshold=600, max=0.3) lifts gently up to
    # a 0.3 floor at len_tokens ≈ 975, which is enough to outweigh the
    # α·(s_hyp/n_hyp) ≤ 0.10 partial-credit floor without overwhelming a
    # genuine β=0.80 disproof signal.
    length_penalty_enabled: bool = False
    length_penalty_threshold: int = 600
    length_penalty_per_token: float = 8e-4
    length_penalty_max: float = 0.3

    # ── Reward shaping ───────────────────────────────────────────────────────
    enable_format_reward: bool = True
    format_reward_weight: float = 0.1
    verifier_reward_weight: float = 1.0
    reward_pool_workers: int = 4
    rollouts_log: str = "rollouts.jsonl"

    # ── v2.0 oracle reward path (P2) ─────────────────────────────────────────
    # reward_mode selects between the legacy classifier reward (v1.0,
    # operates on the model's own counterexample script) and the oracle
    # reward (v2.0, scores the model's witness expression against the
    # independent per-theorem verifier).
    #
    # P2 default remains "legacy" because the data loader and GRPOTrainer
    # are not yet wired through (those land in P3/P4). Flip to "oracle"
    # only after the v2 dataset + data loader are in place.
    reward_mode: str = "legacy"             # "legacy" | "oracle"

    # task_mode controls how NONE / TRUE-conjecture inputs are scored.
    # P2 ships only "counterexample_only" (Stage 1, FALSE-only). The other
    # modes are placeholders for the P7 curriculum work.
    task_mode: str = "counterexample_only"  # "counterexample_only" | "counterexample_or_none" | "classify_then_generate"

    # Oracle reward weights {alpha, beta, gamma, delta, epsilon}.
    # See ORACLE_REWARD_WEIGHTS_DEFAULT / _SPARSE for documented defaults.
    oracle_reward_weights: dict = field(
        default_factory=lambda: dict(ORACLE_REWARD_WEIGHTS_DEFAULT)
    )

    # Per-rollout oracle subprocess timeout. Verifier modules typically
    # complete in < 200 ms; 8 s is the safety ceiling.
    oracle_timeout_seconds: float = 8.0

    # ── Optimisation ─────────────────────────────────────────────────────────
    per_device_train_batch_size: int = 1
    # effective batch = pdbs(1) × gas(4) × G(8) = 32 rollouts per optimizer step.
    gradient_accumulation_steps: int = 4
    # ~3 epochs over 5103 prompts with pdbs=1, gas=4 → ~500 steps.
    max_steps: int = 500
    num_train_epochs: float = 1.0
    # Conservative LR for RL: RL gradients are noisier than SFT; too-large steps
    # cause policy collapse. 5e-6 is roughly 40× smaller than SFT's 2e-4.
    learning_rate: float = 5e-6
    warmup_ratio: float = 0.1
    # Constant schedule: GRPO's reward landscape is non-stationary (it shifts as
    # the policy improves), so cosine decay can underfit toward the end.
    lr_scheduler_type: str = "constant"
    optim: str = "adamw_torch"
    weight_decay: float = 0.0
    # 1.0 is the standard clip. The smoke run used 0.1, which is too tight and
    # may have blocked meaningful gradient updates.
    max_grad_norm: float = 1.0
    # beta=0.04: KL anchor against the SFT reference policy. 0.0 = no reference
    # model (less VRAM, but no constraint against policy collapse). 0.04 provides
    # a mild anchor that keeps the policy close to the SFT initialisation.
    beta: float = 0.04
    epsilon: float = 0.2
    seed: int = 42

    # ── Logging / checkpoints ────────────────────────────────────────────────
    logging_steps: int = 1
    save_strategy: str = "steps"
    save_steps: int = 50
    save_total_limit: int = 3
    log_completions: bool = True
    # report_to is forwarded directly to TRL's GRPOConfig. "none" disables all
    # integrations; "wandb" expects WANDB_PROJECT / WANDB_API_KEY in env. Kept
    # off-by-default so a misconfigured environment doesn't block the trainer.
    report_to: str = "none"

    # ── Output ───────────────────────────────────────────────────────────────
    # Same legacy semantics as SFTConfig.output_dir — only used when
    # use_run_dir=False; the default v2 path routes through runs/rlvr/.
    output_dir: str = "checkpoints/rlvr/qwen3-4b-grpo"

    # ── Run-directory + experiment tracking ────────────────────────────────
    use_run_dir: bool = True
    wandb_project: str = ""        # "" → derive ("pfe-rlvr-rlvr")
    wandb_group: str = ""          # "" → derive (config_basename)

    # ── Helpers ──────────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "RLVRConfig":
        valid = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in valid})

    def save(self, path) -> None:
        with open(path, "w") as fh:
            json.dump(self.to_dict(), fh, indent=2)

    @classmethod
    def load(cls, path) -> "RLVRConfig":
        with open(path) as fh:
            return cls.from_dict(json.load(fh))
