"""
Load a RLVR prompts JSONL into a HF Dataset shaped for TRL GRPO.

Two record shapes are supported:

1. **Legacy / v1.0 records:**

       {"messages": [
           {"role": "system",    "content": "..."},
           {"role": "user",      "content": "..."}
       ]}

   The returned Dataset has one column: ``prompt`` (list[dict] - the
   conversational prompt that GRPOTrainer accepts).

2. **v2.0 records produced by ``tools/build_splits.py``:**

       {"messages": [system, user],
        "verifier_module_path": "data/verifiers/<dom>/<id>__<hyp>.py",
        "n_hyp": 1,
        "neg_q_index": 1,
        "n_conditions": 2,
        "theorem_id": "..."}

   The returned Dataset has columns: ``prompt``, ``verifier_module_path``,
   ``n_hyp``, ``neg_q_index``, ``n_conditions``, ``theorem_id``.

   These match ``training/rlvr/reward_oracle._REQUIRED_RECORD_KWARGS`` so that
   when ``RLVRConfig.reward_mode == "oracle"`` is wired in P4, TRL forwards
   the columns as per-rollout kwargs to ``make_oracle_reward`` with zero
   further plumbing.

The shape is auto-detected per-line. Mixing shapes within a file raises.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from datasets import Dataset

from training.common.paths import repo_path

logger = logging.getLogger(__name__)


_V2_REQUIRED_FIELDS: tuple[str, ...] = (
    "verifier_module_path", "n_hyp", "neg_q_index", "n_conditions",
)


def _is_v2_record(rec: dict) -> bool:
    """A record is v2-shaped iff all four required oracle metadata fields are
    present at the top level of the JSONL line.
    """
    return all(k in rec for k in _V2_REQUIRED_FIELDS)


def load_rlvr_dataset(cfg) -> Dataset:
    """Load the RLVR prompts JSONL into a TRL-compatible Dataset.

    Auto-detects v1 vs v2 shape; if the first line carries oracle metadata,
    every subsequent line must too (mixed-shape files raise ValueError so
    config mistakes surface immediately rather than at rollout time).
    """
    jsonl_path: Path = repo_path(cfg.train_jsonl)
    logger.info("Loading RLVR prompts from %s", jsonl_path)

    prompts: list[list[dict]] = []
    v2_cols: dict[str, list] = {k: [] for k in _V2_REQUIRED_FIELDS}
    theorem_ids: list[str | None] = []
    detected_v2: bool | None = None

    with jsonl_path.open() as fh:
        for i, raw in enumerate(fh, 1):
            raw = raw.strip()
            if not raw:
                continue
            rec = json.loads(raw)

            msgs = rec.get("messages")
            if not msgs or len(msgs) < 2:
                raise ValueError(f"line {i}: expected >=2 messages, got {msgs!r}")
            roles = [m["role"] for m in msgs]
            if roles[0] != "system" or "user" not in roles:
                raise ValueError(f"line {i}: unexpected roles {roles}")

            # Strip any accidental assistant turn - RLVR is prompt-only.
            prompt_msgs = [m for m in msgs if m["role"] in ("system", "user")]
            prompts.append(prompt_msgs)

            is_v2_line = _is_v2_record(rec)
            if detected_v2 is None:
                detected_v2 = is_v2_line
            elif detected_v2 != is_v2_line:
                raise ValueError(
                    f"line {i}: mixed v1/v2 records in {jsonl_path}. "
                    "Regenerate the file via tools/build_splits.py."
                )

            if detected_v2:
                for k in _V2_REQUIRED_FIELDS:
                    v2_cols[k].append(rec[k])
                theorem_ids.append(rec.get("theorem_id"))

    if not prompts:
        raise ValueError(f"No records loaded from {jsonl_path}")

    if detected_v2:
        logger.info(
            "Loaded %d v2 RLVR prompts with oracle metadata columns: %s",
            len(prompts), list(_V2_REQUIRED_FIELDS) + ["theorem_id"],
        )
        cols = {"prompt": prompts, **v2_cols, "theorem_id": theorem_ids}
        return Dataset.from_dict(cols)

    logger.info("Loaded %d legacy (v1) RLVR prompts (prompt-only)", len(prompts))
    return Dataset.from_dict({"prompt": prompts})
