"""
Resume from the SFT LoRA checkpoint via Unsloth.

We deliberately do NOT call `FastLanguageModel.get_peft_model` again — the
adapter saved by the SFT stage is already trainable when loaded through
`from_pretrained`, and re-attaching would stack a fresh randomly-initialised
LoRA on top of the SFT one and discard the SFT signal.
"""

from types import MethodType

import torch
from unsloth import FastLanguageModel

from training.common.chat_template import apply_chat_template

from training.common.paths import repo_path

_DTYPE_MAP = {
    "bfloat16": torch.bfloat16,
    "float16": torch.float16,
    "float32": torch.float32,
}


def build_model_and_tokenizer(cfg):
    """Load base + SFT-LoRA from cfg.sft_checkpoint and apply Qwen-2.5 chat template."""
    dtype = _DTYPE_MAP[cfg.dtype]
    ckpt = repo_path(cfg.sft_checkpoint)
    if not ckpt.exists():
        raise FileNotFoundError(f"SFT checkpoint not found: {ckpt}")

    kwargs = dict(
        model_name=str(ckpt),
        max_seq_length=cfg.max_seq_length,
        dtype=dtype,
        load_in_4bit=cfg.load_in_4bit,
    )
    if cfg.use_vllm:
        kwargs.update(
            fast_inference=True,
            max_lora_rank=cfg.max_lora_rank,
            gpu_memory_utilization=cfg.vllm_gpu_memory_utilization,
        )

    model, tokenizer = FastLanguageModel.from_pretrained(**kwargs)

    # Unsloth's vLLM-backed GRPO path expects the loaded model to expose
    # `load_lora(...)`. Gemma-3 checkpoints currently come back as a PEFT
    # wrapper without that convenience method, so we attach a thin shim that
    # delegates to Unsloth's vLLM helper when fast inference is enabled.
    if cfg.use_vllm and not hasattr(model, "load_lora"):
        from unsloth_zoo.vllm_utils import load_lora as _load_lora

        def _load_lora_method(self, save_directory, load_tensors=False, lora_request_id=None):
            return _load_lora(
                self,
                save_directory,
                load_tensors=load_tensors,
                lora_request_id=lora_request_id,
            )

        model.load_lora = MethodType(_load_lora_method, model)

    # Multimodal Gemma-3 (Gemma3ForConditionalGeneration) requires token_type_ids
    # during training but GRPO passes None. Wrap forward to auto-generate them
    # (all zeros = text tokens) when missing. Text-only checkpoints
    # (Gemma3ForCausalLM, no vision_config) neither need nor accept
    # token_type_ids, so the wrapper must NOT be applied there.
    if getattr(model.config, "vision_config", None) is not None:
        _original_forward = model.forward

        def _gemma3_forward_wrapper(
            self,
            input_ids=None,
            attention_mask=None,
            token_type_ids=None,
            position_ids=None,
            past_key_values=None,
            inputs_embeds=None,
            labels=None,
            use_cache=None,
            output_attentions=None,
            output_hidden_states=None,
            return_dict=None,
            cache_position=None,
            num_logits_to_keep=0,
            **kwargs
        ):
            # If training and token_type_ids is missing, create default (all zeros for text).
            if self.training and token_type_ids is None and input_ids is not None:
                token_type_ids = torch.zeros_like(input_ids, dtype=torch.long, device=input_ids.device)

            return _original_forward(
                input_ids=input_ids,
                attention_mask=attention_mask,
                token_type_ids=token_type_ids,
                position_ids=position_ids,
                past_key_values=past_key_values,
                inputs_embeds=inputs_embeds,
                labels=labels,
                use_cache=use_cache,
                output_attentions=output_attentions,
                output_hidden_states=output_hidden_states,
                return_dict=return_dict,
                cache_position=cache_position,
                num_logits_to_keep=num_logits_to_keep,
                **kwargs
            )

        model.forward = MethodType(_gemma3_forward_wrapper, model)

    tokenizer = apply_chat_template(
        tokenizer,
        checkpoint_path=ckpt,
        chat_template=cfg.chat_template,
    )

    return model, tokenizer
