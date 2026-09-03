#!/usr/bin/env python3
"""Assemble the twelve Hugging Face model repositories for the Qwen3-4B adapters.

Four seeds (42, 19, 31, 64) x three arms (SFT, RLVR-dense, RLVR-sparse). Each is
a LoRA adapter over ``unsloth/Qwen3-4B``.

Runs are discovered from ``runs/rlvr/*/config.json``: the arm is decided by the
oracle reward weights actually recorded in the run, and the SFT parent is read
from that run's ``sft_checkpoint``. Nothing is hard-coded, so the cards cannot
describe a run that was not used.

On the training machine, where the adapters exist:

    python hf_release/build_model_repos.py --runs-root runs
    bash hf_release/build/models/upload.sh

Anywhere else, to inspect or edit the cards first:

    python hf_release/build_model_repos.py --cards-only

Evaluation numbers come from paper_preparation/results/camera_ready_tables.json,
so the cards agree with the paper by construction.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SEEDS = [42, 19, 31, 64]
DENSE_W = {"alpha": 0.25, "beta": 0.65, "gamma": 0.1, "delta": 0.3, "epsilon": 1.0}
SPARSE_W = {"alpha": 0, "beta": 1, "gamma": 0, "delta": 0, "epsilon": 1}
BASE_MODEL = "unsloth/Qwen3-4B"
DATASET_REPO = "ce-rlvr/SymCE"

# Files that make up a PEFT adapter. Anything else in the run directory
# (optimizer state, rollout logs, wandb) is deliberately not shipped.
ADAPTER_FILES = [
    "adapter_config.json", "adapter_model.safetensors", "adapter_model.bin",
    "README.md", "tokenizer.json", "tokenizer_config.json",
    "special_tokens_map.json", "chat_template.jinja", "added_tokens.json",
    "vocab.json", "merges.txt",
]

ARM_BLURB = {
    "sft": (
        "Supervised fine-tuning on 1,000 counterexample demonstrations. "
        "**This checkpoint is a negative result and is published as one.**"
    ),
    "dense": (
        "GRPO from the SFT adapter with the dense, partial-credit reward "
        "(alpha=0.25, beta=0.65, gamma=0.10, delta=0.30, epsilon=1.00)."
    ),
    "sparse": (
        "GRPO from the SFT adapter with the sparse, outcome-only reward "
        "(beta=epsilon=1, everything else 0), giving a {-1, 0, +1} signal."
    ),
}

WARNING = """> [!WARNING]
> This adapter has lost calibration on purpose-built probes. Trained only on
> counterexamples, it recognises **0.00** of 347 true theorems under the training
> prompt style and asserts that 70 % of true theorems are false under an explicit
> true/false question. It exists so the pathology can be reproduced and studied.
> For a usable falsification model, take the `rlvr-sparse` adapter for the same
> seed."""


def load_runs(runs_root: Path) -> dict[tuple[int, str], dict]:
    """Map (seed, arm) -> {'rlvr_dir', 'sft_dir', 'weights'}."""
    found: dict[tuple[int, str], dict] = {}
    for cfg_path in sorted((runs_root / "rlvr").glob("*/config.json")):
        cfg = json.loads(cfg_path.read_text())
        rl = cfg.get("rlvr", cfg)
        seed, weights = rl.get("seed"), rl.get("oracle_reward_weights")
        if seed not in SEEDS or not weights:
            continue
        if weights == DENSE_W:
            arm = "dense"
        elif weights == SPARSE_W:
            arm = "sparse"
        else:
            continue
        sft_name = Path(str(rl.get("sft_checkpoint", ""))).parent.name
        found[(seed, arm)] = {
            "rlvr_dir": cfg_path.parent,
            "sft_dir": runs_root / "sft" / sft_name if sft_name else None,
            "weights": weights,
        }
    return found


def copy_adapter(src_dir: Path | None, dst: Path) -> list[str]:
    """Copy adapter files. Returns the names copied (empty if src is absent)."""
    if src_dir is None or not src_dir.is_dir():
        return []
    copied = []
    for name in ADAPTER_FILES:
        f = src_dir / name
        if f.is_file():
            # The run directory's own README is training scaffolding, not a card.
            if name == "README.md":
                continue
            shutil.copy2(f, dst / name)
            copied.append(name)
    return copied


CARD = """---
base_model: {base_model}
library_name: peft
license: apache-2.0
language:
- en
pipeline_tag: text-generation
datasets:
- {dataset}
tags:
- peft
- lora
- mathematics
- counterexample-generation
- symbolic-verification
{extra_tags}---

# {repo_name}

{blurb}

LoRA adapter (rank 16, all attention and MLP projections) over
[`{base_model}`]({base_url}), seed **{seed}**. One of twelve checkpoints from
*Counterexample Generation via Per-Theorem Symbolic Verifiers: When Imitation
Hurts and Reinforcement Repairs* (Findings of EMNLP 2026).

- Code: https://github.com/ce-rlvr/SymCE
- Data: https://huggingface.co/datasets/{dataset}
{warning}
## Results (seed {seed})

| Metric | This checkpoint | Untrained base |
|---|---:|---:|
| Counterexample Pass@1 (greedy, n=201) | {ce1} | {ce1_base} |
| Counterexample Pass@8 (sampled, n=201) | {ce8} | {ce8_base} |
| True theorems recognised, training prompt style (n=347) | {tv2} | {tv2_base} |
| True theorems recognised, explicit true/false (n=347) | {tcl} | {tcl_base} |

Regenerate with `python -m paper_preparation.scripts.build_camera_ready_tables`
in the code repository.

## Usage

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base = AutoModelForCausalLM.from_pretrained("{base_model}", dtype="bfloat16",
                                            device_map="auto")
model = PeftModel.from_pretrained(base, "{org}/{repo_name}")
tok = AutoTokenizer.from_pretrained("{base_model}")
```

The model is prompted with a false conjecture plus a one-line witness schema and
emits `[COUNTEREXAMPLE: <python expression>]`, or `[COUNTEREXAMPLE: NONE]` to
assert that no counterexample exists. The prompt templates are in `prompts/` in
the code repository; scoring runs the emitted expression through the record's own
Python verifier.

## Training

| | |
|---|---|
| Base | `{base_model}` |
| LoRA rank / alpha | 16 / 16 |
| Precision | bfloat16 |
| Hardware | one NVIDIA RTX 5090 (32 GB) |
{training_rows}
| Run directory | `{run_dir}` |

## Intended use and limits

Research on falsification and on how reward shape affects calibration. The model
is specialised to undergraduate group, ring, number and field theory, linear
algebra and real analysis, and to one output format. It is not a general
mathematics assistant and was not evaluated for deployment. Every checkpoint here
is 4B and LoRA-adapted; whether the reported effects hold at larger scale or
under full-parameter fine-tuning is untested.

## Citation

```bibtex
@inproceedings{{zouak2026symce,
  title     = {{Counterexample Generation via Per-Theorem Symbolic Verifiers:
               When Imitation Hurts and Reinforcement Repairs}},
  author    = {{Zouak, Omar Farouk and Boukhalfa, Houssam Eddine and
               Soumaya, Lakehal and Katiyar, Shiv and Nefti-Meziani, Samia}},
  booktitle = {{Findings of the Association for Computational Linguistics: EMNLP 2026}},
  year      = {{2026}}
}}
```
"""


def fmt(v) -> str:
    return " - " if v is None else f"{v:.2f}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs-root", default="runs")
    ap.add_argument("--adapter-subdir", default="lora")
    ap.add_argument("--out", default="hf_release/build/models")
    ap.add_argument("--org", default="ce-rlvr")
    ap.add_argument("--cards-only", action="store_true",
                    help="write cards without adapter weights (for review off-GPU)")
    args = ap.parse_args()

    runs_root = REPO_ROOT / args.runs_root
    out = REPO_ROOT / args.out
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    tables = json.loads(
        (REPO_ROOT / "paper_preparation" / "results" / "camera_ready_tables.json").read_text()
    )["multiseed"]

    def metric(key: str, arm: str, seed: int):
        node = tables[key][arm]
        return node["value"] if arm == "base" else node["per_seed"].get(str(seed))

    runs = load_runs(runs_root)
    missing_runs = [(s, a) for s in SEEDS for a in ("dense", "sparse") if (s, a) not in runs]
    if missing_runs:
        print(f"WARNING: no run found for {missing_runs}", file=sys.stderr)

    upload_lines = ["#!/usr/bin/env bash",
                    "# Created by hf_release/build_model_repos.py",
                    "set -euo pipefail", ""]
    built = 0
    no_weights: list[str] = []

    for seed in SEEDS:
        for arm in ("sft", "dense", "sparse"):
            src_arm = "dense" if arm == "sft" else arm
            info = runs.get((seed, src_arm))
            if info is None:
                continue
            slug = "sft" if arm == "sft" else f"rlvr-{arm}"
            repo_name = f"symce-qwen3-4b-{slug}-seed{seed}"
            dst = out / repo_name
            dst.mkdir(parents=True)

            src_dir = (info["sft_dir"] if arm == "sft" else info["rlvr_dir"])
            run_dir = src_dir.relative_to(REPO_ROOT) if src_dir else Path("?")
            adapter_src = (src_dir / args.adapter_subdir) if src_dir else None
            copied = [] if args.cards_only else copy_adapter(adapter_src, dst)
            if not copied and not args.cards_only:
                no_weights.append(f"{repo_name}  (expected {adapter_src})")

            if arm == "sft":
                training_rows = ("| Stage | SFT on 1,000 counterexample demonstrations |\n"
                                 "| Learning rate | 2e-4, cosine, warmup 0.05 |\n"
                                 "| Effective batch | 32 |\n")
                extra_tags = "- negative-result\n- calibration\n"
            else:
                w = info["weights"]
                training_rows = (
                    "| Stage | GRPO from the seed's SFT adapter |\n"
                    f"| Reward weights | alpha={w['alpha']}, beta={w['beta']}, "
                    f"gamma={w['gamma']}, delta={w['delta']}, epsilon={w['epsilon']} |\n"
                    "| Generations per prompt | 4 |\n"
                    "| KL to SFT reference | 0.02 |\n"
                    "| Learning rate | 5e-6, constant, warmup 0.1 |\n"
                    "| Steps | ~1,752 (4 epochs over 3,506 prompts) |\n"
                    f"| Initialised from | `{info['sft_dir'].name if info['sft_dir'] else '?'}` |\n"
                )
                extra_tags = "- grpo\n- rlvr\n- reinforcement-learning\n"

            card = CARD.format(
                base_model=BASE_MODEL,
                base_url=f"https://huggingface.co/{BASE_MODEL}",
                dataset=DATASET_REPO,
                org=args.org,
                repo_name=repo_name,
                seed=seed,
                blurb=ARM_BLURB[arm],
                warning=f"\n{WARNING}\n" if arm == "sft" else "",
                extra_tags=extra_tags,
                training_rows=training_rows.rstrip("\n"),
                run_dir=run_dir,
                ce1=fmt(metric("counterexample_pass_at_1_greedy",
                               "SFT" if arm == "sft" else arm, seed)),
                ce1_base=fmt(metric("counterexample_pass_at_1_greedy", "base", seed)),
                ce8=fmt(metric("counterexample_pass_at_8_sampled",
                               "SFT" if arm == "sft" else arm, seed)),
                ce8_base=fmt(metric("counterexample_pass_at_8_sampled", "base", seed)),
                tv2=fmt(metric("truth_v2_strict", "SFT" if arm == "sft" else arm, seed)),
                tv2_base=fmt(metric("truth_v2_strict", "base", seed)),
                tcl=fmt(metric("truth_classify", "SFT" if arm == "sft" else arm, seed)),
                tcl_base=fmt(metric("truth_classify", "base", seed)),
            )
            (dst / "README.md").write_text(card, encoding="utf-8")
            upload_lines.append(
                f'hf upload {args.org}/{repo_name} "$(dirname "$0")/{repo_name}" . '
                f'--commit-message "SymCE {slug} seed {seed}"'
            )
            built += 1
            print(f"  {repo_name:38s} card + {len(copied)} adapter file(s)")

    upload_sh = out / "upload.sh"
    upload_sh.write_text("\n".join(upload_lines) + "\n", encoding="utf-8")
    upload_sh.chmod(0o755)

    print(f"\nBuilt {built} repo folder(s) in {out}")
    if no_weights:
        print("\nNo adapter weights found for:", file=sys.stderr)
        for line in no_weights:
            print("  " + line, file=sys.stderr)
        print("\nRun this on the training machine, or point --runs-root at the "
              "directory holding runs/sft and runs/rlvr.", file=sys.stderr)
    else:
        print(f"\nUpload all twelve with:\n  bash {upload_sh.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
