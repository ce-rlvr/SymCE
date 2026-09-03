"""
RLVR (GRPO) training entry point.

Usage (from repo root, with pfe-rlvr-env active):
    python -m training.rlvr.train                              # smoke run
    python -m training.rlvr.train --max-steps 200              # scale up
    python -m training.rlvr.train --num-generations 8          # bigger group
    python -m training.rlvr.train --no-enable-format-reward    # ablation
    python -m training.rlvr.train --use-vllm                   # fast rollouts

Outputs land under ``runs/rlvr/<YYYYMMDD-HHMMSS>__<config>__seed<N>__<sha>/``
unless ``--no-use-run-dir`` is passed. Each run dir carries:
    config.json, invocation.json, git_info.json, dataset_fingerprint.json,
    status.json, lora/, merged/, train_log.csv, rollouts.jsonl,
    rollouts_summary.json, run_summary.md.
"""

import os
# Force Accelerate to use bfloat16 instead of falling back to fp16 or other defaults
os.environ["ACCELERATE_MIXED_PRECISION"] = "bf16"

# IMPORTANT: import unsloth BEFORE trl/transformers so its monkey-patches
# (including the GRPO speedups) are applied at import time.
import unsloth  # noqa: F401  (side-effect import)

import argparse
import csv
import sys
from dataclasses import fields
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from training.common.config_loader import load_config_for_section
from training.common.diagnostics import rollup_rollouts_jsonl, write_run_summary_md
from training.common.paths import repo_path
from training.common.run_dir import (
    build_run_dir,
    derive_wandb_names,
    finalise_run,
    write_run_metadata,
)
from training.common.seed import set_seed
from training.rlvr.config import RLVRConfig
from training.rlvr.data import load_rlvr_dataset
from training.rlvr.model import build_model_and_tokenizer
from training.rlvr.trainer import build_trainer


def _build_parser(cfg: RLVRConfig) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="RLVR (GRPO) - Qwen2.5-Math-1.5B + LoRA via Unsloth + TRL",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--config",
        default=None,
        metavar="PATH",
        help=(
            "Optional YAML config file. The [rlvr] section overrides dataclass "
            "defaults; CLI flags below override the config file."
        ),
    )
    for f in fields(cfg):
        flag = f"--{f.name.replace('_', '-')}"
        default_val = getattr(cfg, f.name)
        if isinstance(default_val, bool):
            p.add_argument(flag, default=None,
                           action=argparse.BooleanOptionalAction,
                           help=f"override {f.name}")
        elif isinstance(default_val, list):
            p.add_argument(flag, type=str, nargs="+", default=None,
                           help=f"override {f.name}")
        else:
            p.add_argument(flag, type=type(default_val), default=None,
                           help=f"override {f.name}")
    return p


def _parse() -> tuple[RLVRConfig, argparse.Namespace]:
    parser = _build_parser(RLVRConfig())
    parsed = parser.parse_args()
    cfg = load_config_for_section(
        cfg_class=RLVRConfig,
        section="rlvr",
        config_path=parsed.config,
        cli_namespace=parsed,
    )
    return cfg, parsed


def _save_train_log(trainer, output_dir: Path) -> dict:
    history = trainer.state.log_history
    if not history:
        return {}
    log_path = output_dir / "train_log.csv"
    fieldnames = sorted({k for entry in history for k in entry})
    with log_path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(history)
    print(f"  train_log.csv  -> {log_path}")

    # Headline reward + KL
    final_reward = None
    final_kl = None
    for entry in reversed(history):
        if final_reward is None and "reward" in entry:
            final_reward = entry["reward"]
        if final_kl is None and ("kl" in entry or "objective/kl" in entry):
            final_kl = entry.get("kl", entry.get("objective/kl"))
        if final_reward is not None and final_kl is not None:
            break
    return {"final_reward_mean": final_reward, "final_kl": final_kl}


def _maybe_setup_wandb(cfg: RLVRConfig, wandb_names: dict[str, str]) -> None:
    if cfg.report_to != "wandb":
        return
    os.environ.setdefault("WANDB_PROJECT", cfg.wandb_project or wandb_names["project"])
    os.environ.setdefault("WANDB_RUN_GROUP", cfg.wandb_group or wandb_names["group"])
    os.environ.setdefault("WANDB_NAME", wandb_names["name"])


def main() -> None:
    cfg, parsed_args = _parse()
    set_seed(cfg.seed)

    # Run directory
    if cfg.use_run_dir:
        run_dir = build_run_dir(
            phase="rlvr",
            config_yaml=parsed_args.config,
            seed=cfg.seed,
        )
        wandb_names = derive_wandb_names(
            run_dir, phase="rlvr",
            project_override=cfg.wandb_project or None,
            group_override=cfg.wandb_group or None,
        )
        write_run_metadata(
            run_dir=run_dir, cfg=cfg, phase="rlvr",
            cli_namespace=parsed_args, argv=sys.argv,
            config_yaml=parsed_args.config,
            dataset_paths=[cfg.train_jsonl],
            extra={
                "wandb": wandb_names if cfg.report_to == "wandb" else None,
                "sft_checkpoint": cfg.sft_checkpoint,
                "reward_mode": cfg.reward_mode,
                "task_mode": cfg.task_mode,
                "oracle_reward_weights": cfg.oracle_reward_weights,
            },
        )
        output_dir = run_dir
        print(f"[run-dir]   {run_dir.relative_to(_REPO_ROOT)}")
    else:
        run_dir = None
        output_dir = repo_path(cfg.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        cfg.save(output_dir / "config.json")
        wandb_names = derive_wandb_names(Path(output_dir), phase="rlvr")
        print(f"[run-dir]   (disabled) -> {output_dir}")

    _maybe_setup_wandb(cfg, wandb_names)

    # Model + data
    print(f"[model]     Loading SFT checkpoint {cfg.sft_checkpoint} ...")
    model, tokenizer = build_model_and_tokenizer(cfg)

    print(f"[data]      Loading {cfg.train_jsonl} ...")
    train_ds = load_rlvr_dataset(cfg)
    print(f"            train={len(train_ds)} prompts")

    if cfg.reward_mode == "oracle":
        w = cfg.oracle_reward_weights
        print(
            f"[reward]    oracle (task_mode={cfg.task_mode}) "
            f"α={w['alpha']} β={w['beta']} γ={w['gamma']} "
            f"δ={w['delta']} ε={w['epsilon']} "
            f"timeout={cfg.oracle_timeout_seconds}s "
            f"outer_w={cfg.verifier_reward_weight}"
        )
    else:
        print("[reward]    "
              f"legacy verifier_reward (w={cfg.verifier_reward_weight})"
              + (f" + format_reward (w={cfg.format_reward_weight})"
                 if cfg.enable_format_reward else " (format_reward disabled)"))

    # Train
    import warnings
    warnings.filterwarnings("ignore", message=".*max_new_tokens.*")
    warnings.filterwarnings("ignore", message=".*attention mask API.*")

    print("[trainer]   Building GRPOTrainer ...")
    trainer = build_trainer(
        cfg, model, tokenizer, train_ds,
        output_dir=output_dir, run_name=wandb_names["name"],
    )

    print(f"[train]     max_steps={cfg.max_steps}  G={cfg.num_generations}  "
          f"pdbs={cfg.per_device_train_batch_size}  "
          f"gas={cfg.gradient_accumulation_steps}  beta={cfg.beta}  "
          f"vllm={cfg.use_vllm}")
    try:
        trainer.train()
    except Exception as exc:
        if run_dir is not None:
            finalise_run(run_dir, status="failed", extra={"exception": repr(exc)})
        raise

    # Save artefacts
    print("[save]      Saving artefacts ...")
    lora_dir = output_dir / "lora"
    merged_dir = output_dir / "merged"
    model.save_pretrained(str(lora_dir))
    tokenizer.save_pretrained(str(lora_dir))
    print(f"  LoRA adapters  -> {lora_dir}")

    try:
        model.save_pretrained_merged(str(merged_dir), tokenizer, save_method="merged_16bit")
        print(f"  Merged 16-bit  -> {merged_dir}")
    except Exception as exc:
        print(f"  [warn] merged save skipped: {exc}")

    train_headlines = _save_train_log(trainer, output_dir)

    # Rollouts rollup
    rollouts_path = output_dir / cfg.rollouts_log
    rollouts_summary: dict = {}
    if rollouts_path.exists():
        rollouts_summary = rollup_rollouts_jsonl(
            rollouts_path,
            output_path=output_dir / "rollouts_summary.json",
        )
        print(f"  rollouts_summary.json -> {output_dir / 'rollouts_summary.json'}")
        print(f"    mean_reward        = {rollouts_summary.get('mean_reward')}")
        print(f"    format_ok_rate     = {rollouts_summary.get('format_ok_rate')}")
        print(f"    parse_ok_rate      = {rollouts_summary.get('parse_ok_rate')}")
        print(f"    q_neg_rate         = {rollouts_summary.get('q_neg_rate')}")
        print(f"    group_std_pos_rate = {rollouts_summary.get('group_std_pos_rate')} "
              f"({'PASS' if rollouts_summary.get('plan_p4_group_std_gate_pass') else 'FAIL'} P4 gate >=0.70)")
    else:
        print(f"  [warn] {rollouts_path} not found - skipping rollouts rollup")

    # Summary + finalise
    write_run_summary_md(
        output_dir / "run_summary.md",
        title=f"RLVR run - {output_dir.name}",
        sections={
            "Configuration": {
                "config_yaml": parsed_args.config,
                "seed": cfg.seed,
                "sft_checkpoint": cfg.sft_checkpoint,
                "train_jsonl": cfg.train_jsonl,
                "reward_mode": cfg.reward_mode,
                "task_mode": cfg.task_mode,
                "oracle_reward_weights": cfg.oracle_reward_weights if cfg.reward_mode == "oracle" else None,
                "num_generations": cfg.num_generations,
                "max_steps": cfg.max_steps,
                "report_to": cfg.report_to,
            },
            "Training": train_headlines,
            "Rollouts": {
                "total": rollouts_summary.get("total"),
                "mean_reward": rollouts_summary.get("mean_reward"),
                "format_ok_rate": rollouts_summary.get("format_ok_rate"),
                "parse_ok_rate":  rollouts_summary.get("parse_ok_rate"),
                "q_neg_rate":     rollouts_summary.get("q_neg_rate"),
                "group_std_pos_rate": rollouts_summary.get("group_std_pos_rate"),
                "plan_p4_group_std_gate_pass": rollouts_summary.get("plan_p4_group_std_gate_pass"),
                "reason_counts":  rollouts_summary.get("reason_counts"),
            },
        },
    )

    if run_dir is not None:
        finalise_run(
            run_dir, status="completed",
            extra={
                **train_headlines,
                "rollouts_total": rollouts_summary.get("total"),
                "rollouts_mean_reward": rollouts_summary.get("mean_reward"),
                "rollouts_group_std_pos_rate": rollouts_summary.get("group_std_pos_rate"),
            },
        )
    print("[done]")


if __name__ == "__main__":
    main()
