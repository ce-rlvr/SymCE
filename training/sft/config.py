import json
from dataclasses import asdict, dataclass, field, fields
from typing import List


@dataclass
class SFTConfig:
    # Model
    model_name: str = "unsloth/Qwen3-4B"
    chat_template: str = "auto"  # "auto" or a concrete Unsloth chat template
    max_seq_length: int = 2048
    dtype: str = "bfloat16"    # "bfloat16" | "float16" | "float32"
    load_in_4bit: bool = False  # keep False on Blackwell for stability

    # LoRA
    use_lora: bool = True       # Set to False for full fine-tuning
    lora_r: int = 8             # bump to 16 for full-scale runs per proposal
    lora_alpha: int = 16
    lora_dropout: float = 0.0
    target_modules: List[str] = field(default_factory=lambda: [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ])
    use_gradient_checkpointing: str = "unsloth"

    # Data
    train_jsonl: str = "data/sft_data.jsonl"
    eval_fraction: float = 0.05  # ~65 held-out records from the 1 300

    # task_mode selects the expected assistant-target shape:
    #   - "legacy":              ```python ... ``` code block (v1.0 SFT data).
    #   - "counterexample_only": <reasoning>...</reasoning>\n[COUNTEREXAMPLE: ...]
    #                            (v2.0 SFT data; P3 onwards).
    # The "legacy" default keeps backwards-compat with existing checkpoints
    # until configs explicitly opt in to v2.
    task_mode: str = "legacy"

    # Optimisation
    per_device_train_batch_size: int = 2
    gradient_accumulation_steps: int = 4  # effective batch = 8
    num_train_epochs: float = 1.0
    max_steps: int = -1          # -1 means derive from epochs
    learning_rate: float = 2e-4
    warmup_ratio: float = 0.05
    lr_scheduler_type: str = "cosine"
    optim: str = "adamw_torch"   # not adamw_8bit - avoids bnb on Blackwell
    weight_decay: float = 0.0
    max_grad_norm: float = 1.0
    seed: int = 42

    # Eval / logging / checkpointing
    eval_strategy: str = "steps"
    eval_steps: int = 25
    logging_steps: int = 5
    save_strategy: str = "steps"
    save_steps: int = 50
    save_total_limit: int = 2

    # Output
    # Legacy field, retained for backwards-compat with the v1 trainer. The v2
    # entry point (training/sft/train.py) routes through training.common.run_dir,
    # which produces a fresh runs/sft/<ts>__<cfg>__seed<N>__<sha>/ directory per
    # launch - this string is now only used as a fallback when --no-run-dir is
    # passed, and as the location read by tools/migrate_legacy_checkpoints.py
    # for one-time imports of pre-runs/ artefacts.
    output_dir: str = "checkpoints/sft/qwen3-4b-r8-bf16"

    # Run-directory + experiment tracking
    # When True (default), training writes to runs/sft/<auto-name>/ instead of
    # output_dir. Flip to False only for one-off debugging where you want to
    # land in a hand-picked path.
    use_run_dir: bool = True

    # TRL reporter integration. "none" disables all backends; "wandb" expects
    # wandb to be authenticated (`wandb login`) or WANDB_MODE=offline in env.
    # Set to "tensorboard" for local-only event files.
    report_to: str = "none"

    # W&B project + group. When report_to == "wandb", these are exported via
    # WANDB_PROJECT / WANDB_RUN_GROUP at launch so the run lands in the right
    # dashboard. Defaults derived from the run-dir leaf if left empty.
    wandb_project: str = ""        # "" -> derive ("pfe-rlvr-sft")
    wandb_group: str = ""          # "" -> derive (config_basename)

    # Post-training held-out probe
    # Generates K samples per prompt on a small slice of v2 test records and
    # scores each completion through the oracle. Catches the "SFT didn't learn
    # the [COUNTEREXAMPLE: ...] tag" failure mode *before* you launch a 3-day
    # RLVR run. ~2 minutes added per SFT run on a 50-prompt slice with K=8.
    holdout_probe_enabled: bool = True
    holdout_probe_jsonl: str = "data/test_set.jsonl"
    holdout_probe_n_prompts: int = 50
    holdout_probe_k_samples: int = 8
    holdout_probe_temperature: float = 1.0
    holdout_probe_max_new_tokens: int = 512

    # Helpers
    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "SFTConfig":
        valid = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in d.items() if k in valid})

    def save(self, path) -> None:
        with open(path, "w") as fh:
            json.dump(self.to_dict(), fh, indent=2)

    @classmethod
    def load(cls, path) -> "SFTConfig":
        with open(path) as fh:
            return cls.from_dict(json.load(fh))
