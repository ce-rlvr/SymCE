from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from unsloth.chat_templates import get_chat_template


_CHAT_TEMPLATE_MASK_PARTS: dict[str, tuple[str, str]] = {
    "qwen-2.5": ("<|im_start|>user\n", "<|im_start|>assistant\n"),
    "qwen-3": ("<|im_start|>user\n", "<|im_start|>assistant\n"),
    "llama-3": (
        "<|start_header_id|>user<|end_header_id|>\n\n",
        "<|start_header_id|>assistant<|end_header_id|>\n\n",
    ),
    "llama-3.1": (
        "<|start_header_id|>user<|end_header_id|>\n\n",
        "<|start_header_id|>assistant<|end_header_id|>\n\n",
    ),
    "llama-3.2": (
        "<|start_header_id|>user<|end_header_id|>\n\n",
        "<|start_header_id|>assistant<|end_header_id|>\n\n",
    ),
    "llama-3.3": (
        "<|start_header_id|>user<|end_header_id|>\n\n",
        "<|start_header_id|>assistant<|end_header_id|>\n\n",
    ),
    # Gemma-3 folds the system message into the first user turn, so masking on
    # the user/model turn markers still covers the system prompt correctly.
    "gemma-3": ("<start_of_turn>user\n", "<start_of_turn>model\n"),
}


def _read_json(path: Path) -> Optional[dict]:
    try:
        with path.open() as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def infer_base_model_name(checkpoint_path: Path) -> Optional[str]:
    """Best-effort: read base model name from a LoRA or merged checkpoint."""
    if not checkpoint_path.exists():
        return None

    for name in ("adapter_config.json", "config.json"):
        data = _read_json(checkpoint_path / name)
        if not data:
            continue
        for key in (
            "base_model_name_or_path",
            "_name_or_path",
            "model_name",
            "model_name_or_path",
        ):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def resolve_chat_template(model_name: Optional[str], chat_template: Optional[str]) -> Optional[str]:
    """Map a model name to an Unsloth chat template unless explicitly overridden."""
    if chat_template and chat_template.lower() not in ("auto", "none"):
        return chat_template
    if not model_name:
        return None

    name = model_name.lower()
    if "qwen3" in name or "qwen-3" in name:
        return "qwen-3"
    if "qwen2.5" in name or "qwen-2.5" in name:
        return "qwen-2.5"
    if "gemma-3" in name or "gemma3" in name:
        return "gemma-3"
    if "llama3.3" in name or "llama-3.3" in name or "llama33" in name or "llama-33" in name:
        return "llama-3.3"
    if "llama3.2" in name or "llama-3.2" in name or "llama32" in name or "llama-32" in name:
        return "llama-3.2"
    if "llama3.1" in name or "llama-3.1" in name or "llama31" in name or "llama-31" in name:
        return "llama-3.1"
    if "llama3" in name or "llama-3" in name:
        return "llama-3"
    return None


def resolve_response_mask_parts(
    model_name: Optional[str],
    chat_template: Optional[str],
    checkpoint_path: Optional[Path] = None,
) -> Optional[tuple[str, str]]:
    """Return the instruction/response markers used by response-only loss masking."""
    resolved_name = model_name
    if not resolved_name and checkpoint_path is not None:
        resolved_name = infer_base_model_name(checkpoint_path)

    template = resolve_chat_template(resolved_name, chat_template)
    if template is None:
        return None
    return _CHAT_TEMPLATE_MASK_PARTS.get(template)


def apply_chat_template(
    tokenizer,
    *,
    model_name: Optional[str] = None,
    chat_template: Optional[str] = None,
    checkpoint_path: Optional[Path] = None,
):
    """Apply an Unsloth chat template if one can be resolved."""
    resolved_name = model_name
    if not resolved_name and checkpoint_path is not None:
        resolved_name = infer_base_model_name(checkpoint_path)

    template = resolve_chat_template(resolved_name, chat_template)
    if template is None:
        return tokenizer
    return get_chat_template(tokenizer, chat_template=template)
