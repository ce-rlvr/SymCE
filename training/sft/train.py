"""
SFT training entry point.

Usage (from repo root, with pfe-rlvr-env active):
    python -m training.sft.train                           # soft-start defaults
    python -m training.sft.train --num-train-epochs 2      # scale up
    python -m training.sft.train --max-steps 5             # 5-step smoke run
    python -m training.sft.train --lora-r 16               # proposal target rank

Outputs land under ``runs/sft/<YYYYMMDD-HHMMSS>__<config>__seed<N>__<sha>/``
unless ``--no-use-run-dir`` is passed, in which case the legacy
``cfg.output_dir`` path is used. Each run dir carries:
    config.json, invocation.json, git_info.json, dataset_fingerprint.json,
    status.json, lora/, merged/, train_log.csv, sft_diagnostics.json,
    run_summary.md.
"""

import argparse
import csv
import os

# Force Accelerate to use bfloat16 defaults
os.environ["ACCELERATE_MIXED_PRECISION"] = "bf16"
import json
import sys
from dataclasses import fields
from pathlib import Path

# Make repo root importable when invoked directly or as a module
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from training.common.config_loader import load_config_for_section
from training.common.diagnostics import sft_holdout_probe, write_run_summary_md
from training.common.paths import repo_path
from training.common.run_dir import (
    RUNS_ROOT,
    build_run_dir,
    derive_wandb_names,
    finalise_run,
    write_run_metadata,
)
from training.common.seed import set_seed
from training.sft.config import SFTConfig
from training.sft.data import load_sft_dataset
from training.sft.model import build_model_and_tokenizer
from training.sft.trainer import build_trainer


def _build_parser(cfg: SFTConfig) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="SFT fine-tuning — Qwen2.5-Math-1.5B + LoRA via Unsloth",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument(
        "--config",
        default=None,
        metavar="PATH",
        help=(
            "Optional YAML config file. The [sft] section overrides dataclass "
            "defaults; CLI flags below override the config file."
        ),
    )
    for f in fields(cfg):
        flag = f"--{f.name.replace('_', '-')}"
        if f.type == "List[str]" or isinstance(getattr(cfg, f.name), list):
            p.add_argument(flag, type=str, nargs="+", default=None,
                           metavar="MODULE", help=f"override {f.name}")
        elif f.type == "bool" or isinstance(getattr(cfg, f.name), bool):
            p.add_argument(flag, default=None,
                           action=argparse.BooleanOptionalAction,
                           help=f"override {f.name}")
        else:
            p.add_argument(flag, type=type(getattr(cfg, f.name)), default=None,
                           help=f"override {f.name}")
    return p


def _parse() -> tuple[SFTConfig, argparse.Namespace]:
    parser = _build_parser(SFTConfig())
    parsed = parser.parse_args()
    cfg = load_config_for_section(
        cfg_class=SFTConfig,
        section="sft",
        config_path=parsed.config,
        cli_namespace=parsed,
    )
    return cfg, parsed


def _save_train_log(trainer, output_dir: Path) -> dict:
    """Dump trainer.state.log_history → train_log.csv. Return a small headline dict."""
    history = trainer.state.log_history
    if not history:
        return {}
    log_path = output_dir / "train_log.csv"
    fieldnames = sorted({k for entry in history for k in entry})
    with open(log_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(history)
    print(f"  train_log.csv  → {log_path}")

    # Headline metrics: final train loss + final eval loss if present
    final_train = None
    final_eval = None
    for entry in reversed(history):
        if final_train is None and "loss" in entry:
            final_train = entry["loss"]
        if final_eval is None and "eval_loss" in entry:
            final_eval = entry["eval_loss"]
        if final_train is not None and final_eval is not None:
            break
    return {"final_loss": final_train, "final_eval_loss": final_eval}


def _load_probe_records(jsonl_path: Path, n: int) -> list[dict]:
    """Load the first ``n`` usable v2 records (drop migration_failed / witness_passes_verifier=false)."""
    records: list[dict] = []
    if not jsonl_path.exists():
        print(f"[probe]    skipped — {jsonl_path} not found")
        return records
    with open(jsonl_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("migration_failed") or r.get("witness_passes_verifier") is False:
                continue
            v = r.get("verifier") or {}
            if not v.get("module_path"):
                continue
            records.append(r)
            if len(records) >= n:
                break
    return records


def _maybe_setup_wandb(cfg: SFTConfig, wandb_names: dict[str, str]) -> None:
    """Export WANDB_* env vars so TRL's report_to=wandb picks them up."""
    if cfg.report_to != "wandb":
        return
    os.environ.setdefault("WANDB_PROJECT", cfg.wandb_project or wandb_names["project"])
    os.environ.setdefault("WANDB_RUN_GROUP", cfg.wandb_group or wandb_names["group"])
    os.environ.setdefault("WANDB_NAME", wandb_names["name"])


def main() -> None:
    cfg, parsed_args = _parse()
    set_seed(cfg.seed)

    # ── Run directory ──────────────────────────────────────────────────────
    if cfg.use_run_dir:
        run_dir = build_run_dir(
            phase="sft",
            config_yaml=parsed_args.config,
            seed=cfg.seed,
        )
        wandb_names = derive_wandb_names(
            run_dir, phase="sft",
            project_override=cfg.wandb_project or None,
            group_override=cfg.wandb_group or None,
        )
        write_run_metadata(
            run_dir=run_dir, cfg=cfg, phase="sft",
            cli_namespace=parsed_args, argv=sys.argv,
            config_yaml=parsed_args.config,
            dataset_paths=[cfg.train_jsonl, cfg.holdout_probe_jsonl] if cfg.holdout_probe_enabled else [cfg.train_jsonl],
            extra={"wandb": wandb_names if cfg.report_to == "wandb" else None},
        )
        output_dir = run_dir
        print(f"[run-dir]  {run_dir.relative_to(_REPO_ROOT)}")
    else:
        run_dir = None
        output_dir = repo_path(cfg.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        cfg.save(output_dir / "config.json")
        wandb_names = derive_wandb_names(Path(output_dir), phase="sft")
        print(f"[run-dir]  (disabled) → {output_dir}")

    _maybe_setup_wandb(cfg, wandb_names)

    lora_dir = output_dir / "lora"
    merged_dir = output_dir / "merged"

    # ── Model + data ───────────────────────────────────────────────────────
    print(f"[model]    Loading {cfg.model_name} …")
    model, tokenizer = build_model_and_tokenizer(cfg)

    print(f"[data]     Loading {cfg.train_jsonl} …")
    train_ds, eval_ds = load_sft_dataset(cfg, tokenizer)
    print(f"           train={len(train_ds)}  eval={len(eval_ds)}")

    # ── Train ──────────────────────────────────────────────────────────────
    print("[trainer]  Building SFTTrainer …")
    trainer = build_trainer(
        cfg, model, tokenizer, train_ds, eval_ds,
        output_dir=output_dir, run_name=wandb_names["name"],
    )

    print("[train]    Starting training …")
    try:
        trainer.train()
    except Exception as exc:
        if run_dir is not None:
            finalise_run(run_dir, status="failed", extra={"exception": repr(exc)})
        raise

    # ── Save artefacts ─────────────────────────────────────────────────────
    print("[save]     Saving artefacts …")
    if cfg.use_lora:
        model.save_pretrained(str(lora_dir))
        tokenizer.save_pretrained(str(lora_dir))
        print(f"  LoRA adapters  → {lora_dir}")

        try:
            model.save_pretrained_merged(str(merged_dir), tokenizer, save_method="merged_16bit")
            print(f"  Merged 16-bit  → {merged_dir}")
        except Exception as exc:
            print(f"  [warn] merged save skipped: {exc}")
    else:
        # Full finetuning: save the full model directly
        model.save_pretrained(str(output_dir / "full_model"))
        tokenizer.save_pretrained(str(output_dir / "full_model"))
        print(f"  Full model  → {output_dir / 'full_model'}")

    train_headlines = _save_train_log(trainer, output_dir)

    # ── Post-train held-out probe ──────────────────────────────────────────
    probe_summary: dict = {}
    if cfg.holdout_probe_enabled:
        print(f"[probe]    Held-out probe on {cfg.holdout_probe_jsonl} "
              f"(n={cfg.holdout_probe_n_prompts}, k={cfg.holdout_probe_k_samples}) …")
        from unsloth import FastLanguageModel
        FastLanguageModel.for_inference(model)
        probe_records = _load_probe_records(
            repo_path(cfg.holdout_probe_jsonl), cfg.holdout_probe_n_prompts,
        )
        if probe_records:
            probe_summary = sft_holdout_probe(
                model=model, tokenizer=tokenizer,
                probe_records=probe_records,
                k_samples=cfg.holdout_probe_k_samples,
                max_new_tokens=cfg.holdout_probe_max_new_tokens,
                temperature=cfg.holdout_probe_temperature,
                base_seed=cfg.seed,
                output_path=output_dir / "sft_diagnostics.json",
            )
            print(f"  sft_diagnostics.json → {output_dir / 'sft_diagnostics.json'}")
            print(f"    tag_parse_rate          = {probe_summary['tag_parse_rate']:.3f}")
            print(f"    witness_parse_ok_rate   = {probe_summary['witness_parse_ok_rate']:.3f}")
            print(f"    oracle_pass_at_1        = {probe_summary['oracle_pass_at_1']:.3f}")
            print(f"    oracle_pass_at_{cfg.holdout_probe_k_samples}        = "
                  f"{probe_summary[f'oracle_pass_at_{cfg.holdout_probe_k_samples}']:.3f}")
            if not probe_summary["advisory_gate_passed"]:
                print("  [warn] tag_parse_rate < 0.80 — RLVR will likely struggle. "
                      "Consider revisiting SFT data quality before continuing.")
        else:
            print("  [warn] no probe records loaded — skipping diagnostics")

    # ── Summary + finalise ─────────────────────────────────────────────────
    write_run_summary_md(
        output_dir / "run_summary.md",
        title=f"SFT run — {output_dir.name}",
        sections={
            "Configuration": {
                "config_yaml": parsed_args.config,
                "seed": cfg.seed,
                "train_jsonl": cfg.train_jsonl,
                "task_mode": cfg.task_mode,
                "lora_r": cfg.lora_r,
                "num_train_epochs": cfg.num_train_epochs,
                "report_to": cfg.report_to,
            },
            "Training": train_headlines,
            "Held-out probe": {
                "n_prompts": probe_summary.get("n_prompts"),
                "k_samples": probe_summary.get("k_samples"),
                "tag_parse_rate": probe_summary.get("tag_parse_rate"),
                "witness_parse_ok_rate": probe_summary.get("witness_parse_ok_rate"),
                "oracle_pass_at_1": probe_summary.get("oracle_pass_at_1"),
                "advisory_gate_passed": probe_summary.get("advisory_gate_passed"),
            },
        },
    )

    if run_dir is not None:
        finalise_run(
            run_dir, status="completed",
            extra={
                **train_headlines,
                "tag_parse_rate": probe_summary.get("tag_parse_rate"),
                "oracle_pass_at_1": probe_summary.get("oracle_pass_at_1"),
            },
        )
    print("[done]")


if __name__ == "__main__":
    main()
