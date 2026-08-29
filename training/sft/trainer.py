from trl import SFTConfig as TRLSFTConfig
from trl import SFTTrainer
from unsloth.chat_templates import train_on_responses_only

from training.common.chat_template import resolve_response_mask_parts


def build_trainer(cfg, model, tokenizer, train_ds, eval_ds, *, output_dir=None, run_name=None):
    """
    Build a TRL SFTTrainer with Unsloth's response-only loss masking.

    Loss is computed only on assistant tokens — system + user turns are masked.
    The instruction/response delimiters are derived from the configured chat
    template so Qwen and Llama-family checkpoints train correctly.

    ``output_dir`` and ``run_name`` are injected by the entry point so the v2
    run-dir layout (runs/sft/<auto-name>/) takes effect without round-tripping
    through cfg.output_dir.
    """
    trl_cfg = TRLSFTConfig(
        output_dir=str(output_dir) if output_dir is not None else cfg.output_dir,
        run_name=run_name or None,
        # Batch / accumulation
        per_device_train_batch_size=cfg.per_device_train_batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        # Epochs / steps
        num_train_epochs=cfg.num_train_epochs,
        max_steps=cfg.max_steps,
        # LR schedule
        learning_rate=cfg.learning_rate,
        warmup_ratio=cfg.warmup_ratio,
        lr_scheduler_type=cfg.lr_scheduler_type,
        # Optimiser
        optim=cfg.optim,
        weight_decay=cfg.weight_decay,
        max_grad_norm=cfg.max_grad_norm,
        # Precision — Unsloth handles gradient checkpointing via get_peft_model
        bf16=True,
        # Eval / logging / save
        eval_strategy=cfg.eval_strategy,
        eval_steps=cfg.eval_steps,
        logging_steps=cfg.logging_steps,
        save_strategy=cfg.save_strategy,
        save_steps=cfg.save_steps,
        save_total_limit=cfg.save_total_limit,
        # Data
        dataset_text_field="text",
        max_length=cfg.max_seq_length,
        dataset_num_proc=1,
        # Misc
        seed=cfg.seed,
        report_to=getattr(cfg, "report_to", "none"),
    )

    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
        args=trl_cfg,
    )

    mask_parts = resolve_response_mask_parts(
        getattr(cfg, "model_name", None),
        getattr(cfg, "chat_template", None),
    )
    if mask_parts is None:
        raise ValueError(
            "Unsupported chat template for response-only masking: "
            f"model_name={getattr(cfg, 'model_name', None)!r}, "
            f"chat_template={getattr(cfg, 'chat_template', None)!r}"
        )

    # Mask loss on system + user turns; only assistant output trains the model.
    trainer = train_on_responses_only(
        trainer,
        instruction_part=mask_parts[0],
        response_part=mask_parts[1],
    )

    return trainer
