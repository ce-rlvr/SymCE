import torch
from unsloth import FastLanguageModel

from training.common.chat_template import apply_chat_template


_DTYPE_MAP = {
    "bfloat16": torch.bfloat16,
    "float16": torch.float16,
    "float32": torch.float32,
}


def build_model_and_tokenizer(cfg):
    """Load the base model and attach LoRA adapters via Unsloth."""
    dtype = _DTYPE_MAP[cfg.dtype]

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=cfg.model_name,
        max_seq_length=cfg.max_seq_length,
        dtype=dtype,
        load_in_4bit=cfg.load_in_4bit,
    )

    tokenizer = apply_chat_template(
        tokenizer,
        model_name=cfg.model_name,
        chat_template=cfg.chat_template,
    )

    if cfg.use_lora:
        model = FastLanguageModel.get_peft_model(
            model,
            r=cfg.lora_r,
            target_modules=list(cfg.target_modules),
            lora_alpha=cfg.lora_alpha,
            lora_dropout=cfg.lora_dropout,
            bias="none",
            use_gradient_checkpointing=cfg.use_gradient_checkpointing,
            random_state=cfg.seed,
            max_seq_length=cfg.max_seq_length,
        )

    return model, tokenizer
