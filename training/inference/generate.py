"""
Smoke-test inference from a saved LoRA (or merged) checkpoint.

Usage (from repo root):
    python -m training.inference.generate --checkpoint checkpoints/sft/qwen25-math-1_5b-r8-bf16/lora
    python -m training.inference.generate --checkpoint checkpoints/sft/qwen25-math-1_5b-r8-bf16/merged --num-samples 5
"""

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import torch
from unsloth import FastLanguageModel

from training.common.chat_template import apply_chat_template

from training.common.paths import repo_path


def _parse_args():
    p = argparse.ArgumentParser(description="Run inference on a saved checkpoint")
    p.add_argument("--checkpoint", required=True,
                   help="Path to LoRA or merged checkpoint directory")
    p.add_argument("--prompts", default="data/rlvr_prompts.jsonl",
                   help="JSONL file of {messages:[system,user]} prompts")
    p.add_argument("--num-samples", type=int, default=3)
    p.add_argument("--max-new-tokens", type=int, default=512)
    p.add_argument("--max-seq-length", type=int, default=2048)
    p.add_argument("--chat-template", default="auto",
                   help="Unsloth chat template name (or 'auto' to infer).")
    return p.parse_args()


def main() -> None:
    args = _parse_args()

    ckpt = Path(args.checkpoint)
    if not ckpt.is_absolute():
        ckpt = repo_path(args.checkpoint)

    print(f"[load]  {ckpt}")
    model, tokenizer = FastLanguageModel.from_pretrained(
        str(ckpt),
        max_seq_length=args.max_seq_length,
        dtype=torch.bfloat16,
        load_in_4bit=False,
    )
    tokenizer = apply_chat_template(
        tokenizer,
        checkpoint_path=ckpt,
        chat_template=args.chat_template,
    )
    FastLanguageModel.for_inference(model)

    prompts_path = repo_path(args.prompts)
    samples = []
    with open(prompts_path) as fh:
        for raw in fh:
            raw = raw.strip()
            if raw:
                samples.append(json.loads(raw))
            if len(samples) >= args.num_samples:
                break

    print(f"[gen]   {len(samples)} sample(s) from {prompts_path.name}\n{''*60}")

    for i, record in enumerate(samples, 1):
        messages = record["messages"]   # [system, user]
        prompt_text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)
        with torch.no_grad():
            out_ids = model.generate(
                **inputs,
                max_new_tokens=args.max_new_tokens,
                do_sample=False,
                temperature=1.0,
                use_cache=True,
            )
        new_tokens = out_ids[0][inputs["input_ids"].shape[1]:]
        completion = tokenizer.decode(new_tokens, skip_special_tokens=True)

        user_snippet = messages[-1]["content"][:200].replace("\n", " ")
        print(f"\n-- Sample {i} --")
        print(f"[user]      {user_snippet}...")
        print(f"[assistant]\n{completion}")

    print(f"\n{''*60}\n[done]")


if __name__ == "__main__":
    main()
