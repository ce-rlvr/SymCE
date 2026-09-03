"""
SFT data loader.

Reads a chat-format JSONL whose every line is ``{"messages": [system, user, assistant]}``,
applies the Qwen chat template, and returns ``(train_dataset, eval_dataset)``.

A ``task_mode`` switch on ``SFTConfig`` selects the expected assistant-target
shape:

- ``"legacy"`` - v1.0 SFT data, where the assistant message is a
  ```python``` code block. No further validation performed.
- ``"counterexample_only"`` - v2.0 SFT data (P3+). Each assistant message is
  validated against the v2 tag contract via
  ``parse_counterexample_tag``; lines that fail to parse a
  ``[COUNTEREXAMPLE: <expr>]`` tag are rejected at load time so a malformed
  dataset surfaces immediately rather than at training step N.

Only the assistant turn contributes to loss (``train_on_responses_only``
handles masking downstream).
"""

from __future__ import annotations

import json
import logging

from datasets import Dataset

from training.common.paths import repo_path
from training.rlvr.reward_oracle import parse_counterexample_tag

logger = logging.getLogger(__name__)


_VALID_TASK_MODES: tuple[str, ...] = ("legacy", "counterexample_only")


def _validate_assistant_v2(content: str, line_no: int) -> None:
    parsed = parse_counterexample_tag(content)
    if not parsed.format_ok or parsed.payload is None:
        raise ValueError(
            f"line {line_no}: v2 SFT record has no parseable "
            f"[COUNTEREXAMPLE: …] tag in the assistant message; "
            f"set task_mode='legacy' for v1 data or rebuild via "
            f"tools/build_splits.py."
        )


def load_sft_dataset(cfg, tokenizer):
    """
    Load ``cfg.train_jsonl``, apply the Qwen chat template, and return
    ``(train_dataset, eval_dataset)``.

    Each record must be ``{"messages": [system, user, assistant]}``. When
    ``cfg.task_mode == "counterexample_only"``, the assistant content is also
    validated to contain a parseable ``[COUNTEREXAMPLE: ...]`` tag.
    """
    task_mode = getattr(cfg, "task_mode", "legacy")
    if task_mode not in _VALID_TASK_MODES:
        raise ValueError(
            f"SFTConfig.task_mode={task_mode!r} not in {_VALID_TASK_MODES!r}"
        )

    jsonl_path = repo_path(cfg.train_jsonl)
    logger.info("Loading SFT data from %s (task_mode=%s)", jsonl_path, task_mode)

    texts = []
    with open(jsonl_path) as fh:
        for i, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw:
                continue
            rec = json.loads(raw)
            msgs = rec.get("messages")
            if not msgs or len(msgs) != 3:
                raise ValueError(
                    f"line {i}: expected 3 messages, got "
                    f"{len(msgs) if msgs else None}"
                )
            roles = [m["role"] for m in msgs]
            if roles != ["system", "user", "assistant"]:
                raise ValueError(f"line {i}: unexpected roles {roles}")

            if task_mode == "counterexample_only":
                _validate_assistant_v2(msgs[2].get("content", ""), i)

            text = tokenizer.apply_chat_template(
                msgs,
                tokenize=False,
                add_generation_prompt=False,
            )
            texts.append(text)

    if not texts:
        raise ValueError(f"No records loaded from {jsonl_path}")

    ds = Dataset.from_dict({"text": texts})
    split = ds.train_test_split(test_size=cfg.eval_fraction, seed=cfg.seed)
    return split["train"], split["test"]
