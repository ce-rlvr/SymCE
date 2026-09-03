#!/usr/bin/env python3
"""Run baseline eval -> SFT -> eval -> RLVR -> final eval."""

from __future__ import annotations

import argparse
import csv
import gc
import json
import multiprocessing as mp
import os
import shlex
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

# Force Accelerate to use bfloat16 defaults
os.environ["ACCELERATE_MIXED_PRECISION"] = "bf16"

# Unsloth must be imported before TRL/transformers for GRPO speedups.
import unsloth  # noqa: F401
import torch
from transformers import TrainerCallback

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from training.common.config_loader import load_config_for_section
from training.common.diagnostics import rollup_rollouts_jsonl, sft_holdout_probe, write_run_summary_md
from training.common.paths import repo_path
from training.common.run_dir import (
    RUNS_ROOT,
    build_run_dir,
    dataset_fingerprint,
    derive_wandb_names,
    finalise_run,
    write_run_metadata,
)
from training.common.seed import set_seed
from training.eval import eval_runner
from training.rlvr.config import RLVRConfig
from training.rlvr.data import load_rlvr_dataset
from training.rlvr.model import build_model_and_tokenizer as build_rlvr_model
from training.rlvr.trainer import build_trainer as build_rlvr_trainer
from training.sft.config import SFTConfig
from training.sft.data import load_sft_dataset
from training.sft.model import build_model_and_tokenizer as build_sft_model
from training.sft.trainer import build_trainer as build_sft_trainer


@dataclass
class FullExperimentConfig:
    config_path: str | None
    sft_args: list[str]
    rlvr_args: list[str]
    eval_args: list[str]
    test_file: str
    base_model: str
    eval_n_samples: int
    resume_from: str | None = None
    resume_run: str | None = None


_RESUME_STEPS: tuple[str, ...] = (
    "baseline_eval",
    "sft",
    "sft_eval",
    "rlvr",
    "rlvr_eval",
)


def _split_args(arg_str: str) -> list[str]:
    return shlex.split(arg_str) if arg_str else []


def _flag_present(tokens: list[str], flag: str) -> bool:
    return any(tok == flag or tok.startswith(f"{flag}=") for tok in tokens)


def _default_test_file() -> str:
    if repo_path("data/test_set.jsonl").exists():
        return "data/test_set.jsonl"
    return "data/test_set.jsonl"


def _build_cfg_parser(cfg) -> argparse.ArgumentParser:
    from dataclasses import fields

    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--config", default=None)
    for f in fields(cfg):
        flag = f"--{f.name.replace('_', '-')}"
        default_val = getattr(cfg, f.name)
        if isinstance(default_val, bool):
            p.add_argument(flag, default=None, action=argparse.BooleanOptionalAction)
        elif isinstance(default_val, list):
            p.add_argument(flag, type=str, nargs="+", default=None)
        else:
            p.add_argument(flag, type=type(default_val), default=None)
    return p


def _inject_config_arg(tokens: list[str], config_path: str | None) -> list[str]:
    if config_path and not _flag_present(tokens, "--config"):
        return ["--config", config_path, *tokens]
    return tokens


def _parse_sft_cfg(config_path: str | None, sft_args: str) -> tuple[SFTConfig, argparse.Namespace, list[str]]:
    tokens = _inject_config_arg(_split_args(sft_args), config_path)
    parser = _build_cfg_parser(SFTConfig())
    parsed = parser.parse_args(tokens)
    cfg = load_config_for_section(SFTConfig, "sft", parsed.config, parsed)
    return cfg, parsed, tokens


def _parse_rlvr_cfg(config_path: str | None, rlvr_args: str) -> tuple[RLVRConfig, argparse.Namespace, list[str]]:
    tokens = _inject_config_arg(_split_args(rlvr_args), config_path)
    parser = _build_cfg_parser(RLVRConfig())
    parsed = parser.parse_args(tokens)
    cfg = load_config_for_section(RLVRConfig, "rlvr", parsed.config, parsed)
    return cfg, parsed, tokens


def _parse_eval_args(eval_args: str, default_n_samples: int, test_file: str) -> tuple[argparse.Namespace, list[str]]:
    tokens = _split_args(eval_args)
    parser = eval_runner._build_parser()
    args = parser.parse_args(tokens)
    if not _flag_present(tokens, "--n-samples"):
        args.n_samples = default_n_samples
    args.test_file = test_file

    # Guard against the historical Pass@5 == Pass@1 bug:
    # greedy decoding (temperature == 0.0) + n_samples > 1 produces N
    # byte-identical completions, silently collapsing Pass@K to Pass@1.
    # If the caller asked for Pass@K but left temperature at the eval_runner
    # default (0.0), auto-bump to a sensible sampling temperature and emit a
    # loud warning so the choice is visible in the logs.
    if args.n_samples > 1 and args.temperature == 0.0 and not _flag_present(tokens, "--temperature"):
        new_temp = 0.7
        print(
            f"  [run_full_experiment] WARNING: eval n_samples={args.n_samples} "
            f"with temperature=0.0 would collapse Pass@K → Pass@1 "
            f"(greedy gives identical samples). Auto-bumping temperature to "
            f"{new_temp}. Pass --temperature explicitly to silence this."
        )
        args.temperature = new_temp
        # Reflect the change in the token stream so downstream argparse-aware
        # callers see the corrected value.
        tokens = tokens + ["--temperature", str(new_temp)]
    elif args.n_samples > 1 and args.temperature == 0.0:
        # User explicitly asked for greedy + multi-sample - keep it (we'll
        # still log the warning at generation time) but flag it once.
        print(
            f"  [run_full_experiment] WARNING: explicit temperature=0.0 with "
            f"n_samples={args.n_samples}. All samples will be identical; "
            f"Pass@K equals Pass@1."
        )

    return args, tokens


def _save_train_log(trainer, output_dir: Path) -> dict:
    history = trainer.state.log_history
    if not history:
        return {}
    log_path = output_dir / "train_log.csv"
    fieldnames = sorted({k for entry in history for k in entry})
    with open(log_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(history)
    print(f"  train_log.csv  -> {log_path}")

    final_loss = None
    final_eval_loss = None
    final_reward = None
    final_kl = None
    for entry in reversed(history):
        if final_loss is None and "loss" in entry:
            final_loss = entry["loss"]
        if final_eval_loss is None and "eval_loss" in entry:
            final_eval_loss = entry["eval_loss"]
        if final_reward is None and "reward" in entry:
            final_reward = entry["reward"]
        if final_kl is None and ("kl" in entry or "objective/kl" in entry):
            final_kl = entry.get("kl", entry.get("objective/kl"))
        if all(v is not None for v in (final_loss, final_eval_loss, final_reward, final_kl)):
            break

    headline = {
        "final_loss": final_loss,
        "final_eval_loss": final_eval_loss,
        "final_reward_mean": final_reward,
        "final_kl": final_kl,
    }
    return {k: v for k, v in headline.items() if v is not None}


def _load_probe_records(jsonl_path: Path, n: int) -> list[dict]:
    records: list[dict] = []
    if not jsonl_path.exists():
        print(f"[probe]    skipped -> {jsonl_path} not found")
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


def _maybe_setup_wandb(report_to: str, wandb_names: dict[str, str], project: str, group: str) -> None:
    if report_to != "wandb":
        return
    os.environ.setdefault("WANDB_PROJECT", project or wandb_names["project"])
    os.environ.setdefault("WANDB_RUN_GROUP", group or wandb_names["group"])
    os.environ.setdefault("WANDB_NAME", wandb_names["name"])


def _append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, default=str) + "\n")


def _clone_namespace(ns: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(**vars(ns))


def _write_eval_results(
    *,
    eval_args: argparse.Namespace,
    test_path: Path,
    records: list[dict],
    eval_format: str,
    load_stats: dict,
    model,
    tokenizer,
    model_type: str,
    producer_run_id: str,
    extra_meta: dict | None,
) -> tuple[Path, dict, dict]:
    t_start = time.time()
    per_record, summary = eval_runner.run_eval(
        records,
        eval_format,
        model=model,
        tokenizer=tokenizer,
        use_canonical_witness=eval_args.use_canonical_witness,
        n_samples=eval_args.n_samples,
        max_new_tokens=eval_args.max_new_tokens,
        temperature=eval_args.temperature,
        seed=eval_args.seed,
        reward_workers=eval_args.reward_workers,
        oracle_timeout=eval_args.oracle_timeout,
    )
    elapsed = time.time() - t_start

    effective_model_type = "calibration" if eval_args.use_canonical_witness else model_type
    testset_tag = test_path.stem

    if eval_args.output_dir is None:
        ts_leaf = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        leaf = f"{ts_leaf}__{producer_run_id}__{testset_tag}__{effective_model_type}"
        out_dir = RUNS_ROOT / "eval" / leaf
        out_dir.mkdir(parents=True, exist_ok=False)
        result_filename = "eval_result.json"
        summary_filename = "eval_summary.json"
        run_id = eval_args.run_id or leaf
        write_run_metadata(
            run_dir=out_dir,
            cfg=vars(eval_args),
            phase="eval",
            cli_namespace=eval_args,
            argv=sys.argv,
            config_yaml=None,
            dataset_paths=[eval_args.test_file],
            extra={
                "producer_run_id": producer_run_id,
                "model": eval_args.model,
                "lora_adapter": eval_args.lora_adapter,
                "model_type": effective_model_type,
                "use_canonical_witness": eval_args.use_canonical_witness,
            },
        )
    else:
        run_id = eval_args.run_id or datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        out_dir = Path(eval_args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        result_filename = f"{run_id}_{effective_model_type}.json"
        summary_filename = f"{run_id}_{effective_model_type}_summary.json"

    meta = {
        "run_id": run_id,
        "producer_run_id": producer_run_id,
        "model": eval_args.model,
        "lora_adapter": eval_args.lora_adapter,
        "model_type": effective_model_type,
        "eval_format": eval_format,
        "use_canonical_witness": eval_args.use_canonical_witness,
        "test_file": str(test_path),
        "test_file_fingerprint": dataset_fingerprint([eval_args.test_file]),
        "load_stats": load_stats,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "n_records": len(records),
        "n_samples": eval_args.n_samples,
        "temperature": eval_args.temperature,
        "max_new_tokens": eval_args.max_new_tokens,
        "seed": eval_args.seed,
        "elapsed_seconds": round(elapsed, 1),
        "extra": extra_meta or {},
    }

    full_results = {"meta": meta, "summary": summary, "per_record": per_record}
    full_path = out_dir / result_filename
    with open(full_path, "w", encoding="utf-8") as fh:
        json.dump(full_results, fh, indent=2, ensure_ascii=False, default=str)

    summary_path = out_dir / summary_filename
    with open(summary_path, "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "summary": summary}, fh, indent=2, ensure_ascii=False, default=str)

    if eval_args.output_dir is None:
        eval_runner._write_eval_summary_md(out_dir, meta, summary, eval_format)
        finalise_run(out_dir, status="completed", extra={
            "pass_at_1": summary.get("pass_at_1"),
            "elapsed_seconds": round(elapsed, 1),
        })

    print(f"[eval]     {effective_model_type} -> {out_dir}")
    return out_dir, summary, meta


class _EvalAfterEpochCallback(TrainerCallback):
    def __init__(self, eval_fn):
        self.eval_fn = eval_fn
        self.seen_epochs: set[int] = set()

    def on_epoch_end(self, args, state, control, **kwargs):
        if state.epoch is None:
            return control
        epoch_idx = int(state.epoch)
        if epoch_idx in self.seen_epochs:
            return control
        self.seen_epochs.add(epoch_idx)
        self.eval_fn(epoch_idx)
        return control

    def on_train_end(self, args, state, control, **kwargs):
        if state.epoch is None:
            self.eval_fn(None)
            return control
        epoch_idx = int(state.epoch)
        if epoch_idx not in self.seen_epochs:
            self.eval_fn(epoch_idx)
        return control


class _SaveAfterEpochCallback(TrainerCallback):
    def __init__(self, save_fn):
        self.save_fn = save_fn
        self.seen_epochs: set[int] = set()

    def on_epoch_end(self, args, state, control, **kwargs):
        if state.epoch is None:
            return control
        epoch_idx = int(state.epoch)
        if epoch_idx in self.seen_epochs:
            return control
        self.seen_epochs.add(epoch_idx)
        self.save_fn(epoch_idx)
        return control

    def on_train_end(self, args, state, control, **kwargs):
        if state.epoch is None:
            self.save_fn(None)
            return control
        epoch_idx = int(state.epoch)
        if epoch_idx not in self.seen_epochs:
            self.save_fn(epoch_idx)
        return control


def _cleanup_model(model, tokenizer) -> None:
    del model
    del tokenizer
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.synchronize()
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()


def _isolated_worker(queue, target_func, args, kwargs) -> None:
    try:
        result = target_func(*args, **kwargs)
        queue.put({"status": "ok", "result": result})
    except Exception as exc:
        import traceback

        queue.put({
            "status": "error",
            "error": repr(exc),
            "traceback": traceback.format_exc(),
        })


def _run_in_isolated_process(target_func, *args, **kwargs):
    ctx = mp.get_context("spawn")
    queue = ctx.Queue()
    proc = ctx.Process(target=_isolated_worker, args=(queue, target_func, args, kwargs))
    proc.start()
    proc.join()

    if proc.exitcode != 0:
        raise RuntimeError(
            f"Isolated process for {target_func.__name__} failed with exit code {proc.exitcode}"
        )

    if queue.empty():
        raise RuntimeError("Isolated process completed without returning a result.")

    payload = queue.get()
    if payload.get("status") == "error":
        raise RuntimeError(
            "Isolated process raised an exception:\n"
            f"{payload.get('error')}\n{payload.get('traceback')}"
        )
    return payload.get("result")


def _run_standalone_eval(eval_args, test_path, records, eval_format, load_stats, model_type, producer_run_id):
    from training.eval import eval_runner
    model_obj, tok = eval_runner.load_model_and_tokenizer(
        model_path=eval_args.model,
        lora_adapter=eval_args.lora_adapter,
        max_seq_length=eval_args.max_seq_length,
        dtype_str=eval_args.dtype,
        chat_template=eval_args.chat_template,
    )
    result = _write_eval_results(
        eval_args=eval_args,
        test_path=test_path,
        records=records,
        eval_format=eval_format,
        load_stats=load_stats,
        model=model_obj,
        tokenizer=tok,
        model_type=model_type,
        producer_run_id=producer_run_id,
        extra_meta=None,
    )
    return str(result[0]), result[1], result[2]


def _step_index(step: str) -> int:
    try:
        return _RESUME_STEPS.index(step)
    except ValueError as exc:
        raise ValueError(f"Unknown resume step: {step}") from exc


def _should_run(step: str, resume_from: str | None) -> bool:
    if resume_from is None:
        return True
    return _step_index(step) >= _step_index(resume_from)


def _load_resume_state(resume_run: Path) -> dict:
    state_path = resume_run / "full_experiment.json"
    if not state_path.exists():
        raise FileNotFoundError(f"resume run state not found: {state_path}")
    return json.loads(state_path.read_text())


def _run_sft(cfg: SFTConfig, parsed_args: argparse.Namespace) -> tuple[str, dict]:
    set_seed(cfg.seed)

    if cfg.use_run_dir:
        run_dir = build_run_dir(
            phase="sft",
            config_yaml=parsed_args.config,
            seed=cfg.seed,
        )
        wandb_names = derive_wandb_names(
            run_dir,
            phase="sft",
            project_override=cfg.wandb_project or None,
            group_override=cfg.wandb_group or None,
        )
        write_run_metadata(
            run_dir=run_dir,
            cfg=cfg,
            phase="sft",
            cli_namespace=parsed_args,
            argv=sys.argv,
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
        print(f"[run-dir]  (disabled) -> {output_dir}")

    _maybe_setup_wandb(cfg.report_to, wandb_names, cfg.wandb_project, cfg.wandb_group)

    lora_dir = output_dir / "lora"
    merged_dir = output_dir / "merged"

    print(f"[model]    Loading {cfg.model_name} ...")
    model, tokenizer = build_sft_model(cfg)

    print(f"[data]     Loading {cfg.train_jsonl} ...")
    train_ds, eval_ds = load_sft_dataset(cfg, tokenizer)
    print(f"           train={len(train_ds)}  eval={len(eval_ds)}")

    print("[trainer]  Building SFTTrainer ...")
    trainer = build_sft_trainer(
        cfg, model, tokenizer, train_ds, eval_ds,
        output_dir=output_dir, run_name=wandb_names["name"],
    )

    print("[train]    Starting training ...")
    try:
        trainer.train()
    except Exception:
        if run_dir is not None:
            finalise_run(run_dir, status="failed", extra={"exception": "sft_failed"})
        raise

    print("[save]     Saving artefacts ...")
    if cfg.use_lora:
        model.save_pretrained(str(lora_dir))
        tokenizer.save_pretrained(str(lora_dir))
        print(f"  LoRA adapters  -> {lora_dir}")

        try:
            model.save_pretrained_merged(str(merged_dir), tokenizer, save_method="merged_16bit")
            print(f"  Merged 16-bit  -> {merged_dir}")
        except Exception as exc:
            print(f"  [warn] merged save skipped: {exc}")
    else:
        model.save_pretrained(str(output_dir / "full_model"))
        tokenizer.save_pretrained(str(output_dir / "full_model"))
        print(f"  Full model  -> {output_dir / 'full_model'}")

    train_headlines = _save_train_log(trainer, output_dir)
    del trainer
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

    probe_summary: dict = {}
    if cfg.holdout_probe_enabled:
        print(
            f"[probe]    Held-out probe on {cfg.holdout_probe_jsonl} "
            f"(n={cfg.holdout_probe_n_prompts}, k={cfg.holdout_probe_k_samples}) ..."
        )
        from unsloth import FastLanguageModel
        FastLanguageModel.for_inference(model)
        probe_records = _load_probe_records(
            repo_path(cfg.holdout_probe_jsonl), cfg.holdout_probe_n_prompts,
        )
        if probe_records:
            probe_summary = sft_holdout_probe(
                model=model,
                tokenizer=tokenizer,
                probe_records=probe_records,
                k_samples=cfg.holdout_probe_k_samples,
                max_new_tokens=cfg.holdout_probe_max_new_tokens,
                temperature=cfg.holdout_probe_temperature,
                base_seed=cfg.seed,
                output_path=output_dir / "sft_diagnostics.json",
            )
            print(f"  sft_diagnostics.json -> {output_dir / 'sft_diagnostics.json'}")
            print(f"    tag_parse_rate        = {probe_summary.get('tag_parse_rate')}")
            print(f"    witness_parse_ok_rate = {probe_summary.get('witness_parse_ok_rate')}")
            print(f"    oracle_pass_at_1      = {probe_summary.get('oracle_pass_at_1')}")
        else:
            print("  [warn] no probe records loaded - skipping diagnostics")

    write_run_summary_md(
        output_dir / "run_summary.md",
        title=f"SFT run - {output_dir.name}",
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
            run_dir,
            status="completed",
            extra={
                **train_headlines,
                "tag_parse_rate": probe_summary.get("tag_parse_rate"),
                "oracle_pass_at_1": probe_summary.get("oracle_pass_at_1"),
            },
        )

    print("[done]    SFT complete")
    return str(output_dir), probe_summary


def _run_rlvr(
    cfg: RLVRConfig,
    parsed_args: argparse.Namespace,
    eval_args: argparse.Namespace,
    eval_records: list[dict],
    eval_format: str,
    eval_load_stats: dict,
    full_log_path: Path,
    base_model: str,
) -> tuple[str, list[dict]]:
    set_seed(cfg.seed)

    if cfg.use_run_dir:
        run_dir = build_run_dir(
            phase="rlvr",
            config_yaml=parsed_args.config,
            seed=cfg.seed,
        )
        wandb_names = derive_wandb_names(
            run_dir,
            phase="rlvr",
            project_override=cfg.wandb_project or None,
            group_override=cfg.wandb_group or None,
        )
        write_run_metadata(
            run_dir=run_dir,
            cfg=cfg,
            phase="rlvr",
            cli_namespace=parsed_args,
            argv=sys.argv,
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
        print(f"[run-dir]  {run_dir.relative_to(_REPO_ROOT)}")
    else:
        run_dir = None
        output_dir = repo_path(cfg.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        cfg.save(output_dir / "config.json")
        wandb_names = derive_wandb_names(Path(output_dir), phase="rlvr")
        print(f"[run-dir]  (disabled) -> {output_dir}")

    _maybe_setup_wandb(cfg.report_to, wandb_names, cfg.wandb_project, cfg.wandb_group)

    print(f"[model]    Loading checkpoint {cfg.sft_checkpoint} ...")
    model, tokenizer = build_rlvr_model(cfg)

    print(f"[data]     Loading {cfg.train_jsonl} ...")
    train_ds = load_rlvr_dataset(cfg)
    print(f"           train={len(train_ds)} prompts")

    print("[trainer]  Building GRPOTrainer ...")
    trainer = build_rlvr_trainer(
        cfg, model, tokenizer, train_ds,
        output_dir=output_dir, run_name=wandb_names["name"],
    )

    epoch_saves: list[dict] = []

    def _save_epoch(epoch_idx: int | None) -> None:
        epoch_label = f"{epoch_idx:02d}" if epoch_idx is not None else "final"
        epoch_tag = f"epoch_{epoch_label}"
        epoch_dir = output_dir / f"lora_{epoch_tag}"
        epoch_dir.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(str(epoch_dir))
        tokenizer.save_pretrained(str(epoch_dir))
        epoch_saves.append({"epoch": epoch_idx, "lora_dir": str(epoch_dir)})
        _append_jsonl(full_log_path, {
            "event": "rlvr_epoch_save",
            "epoch": epoch_idx,
            "lora_dir": str(epoch_dir),
        })

    trainer.add_callback(_SaveAfterEpochCallback(_save_epoch))

    print(f"[train]    max_steps={cfg.max_steps}  G={cfg.num_generations}  ")
    try:
        trainer.train()
    except Exception:
        if run_dir is not None:
            finalise_run(run_dir, status="failed", extra={"exception": "rlvr_failed"})
        raise

    print("[save]     Saving artefacts ...")
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

    del trainer
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

    rollouts_path = output_dir / cfg.rollouts_log
    rollouts_summary: dict = {}
    if rollouts_path.exists():
        rollouts_summary = rollup_rollouts_jsonl(
            rollouts_path,
            output_path=output_dir / "rollouts_summary.json",
        )
        print(f"  rollouts_summary.json -> {output_dir / 'rollouts_summary.json'}")
    else:
        print(f"  [warn] {rollouts_path} not found - skipping rollouts rollup")

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
                "beta": cfg.beta,
            },
            "Training": train_headlines,
            "Rollouts": {
                "mean_reward": rollouts_summary.get("mean_reward"),
                "format_ok_rate": rollouts_summary.get("format_ok_rate"),
                "parse_ok_rate": rollouts_summary.get("parse_ok_rate"),
                "q_neg_rate": rollouts_summary.get("q_neg_rate"),
                "group_std_pos_rate": rollouts_summary.get("group_std_pos_rate"),
            },
        },
    )

    if run_dir is not None:
        finalise_run(
            run_dir,
            status="completed",
            extra={
                **train_headlines,
                "final_reward_mean": rollouts_summary.get("mean_reward"),
            },
        )

    print("[done]    RLVR complete")
    return str(output_dir), epoch_saves


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run baseline eval -> SFT -> eval -> RLVR -> final eval.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--config", default=None, metavar="PATH",
                   help="YAML config file with [sft] and [rlvr] sections.")
    p.add_argument("--sft-args", default="", metavar="\"...\"",
                   help="Quoted args forwarded to training.sft.train (e.g. \"--max-steps 5\").")
    p.add_argument("--rlvr-args", default="", metavar="\"...\"",
                   help="Quoted args forwarded to training.rlvr.train (e.g. \"--max-steps 50\").")
    p.add_argument("--eval-args", default="", metavar="\"...\"",
                   help="Quoted args forwarded to training.eval.eval_runner.")
    p.add_argument("--test-file", default=None, metavar="PATH",
                   help="Override eval test file (default: data/test_set.jsonl if present).")
    p.add_argument("--base-model", default=None,
                   help="Override baseline eval model (default: sft.model_name).")
    p.add_argument("--eval-n-samples", type=int, default=5,
                   help="Default eval --n-samples if not set in --eval-args.")
    p.add_argument("--resume-from", choices=_RESUME_STEPS, default=None,
                   help="Resume from a specific step (requires --resume-run for later steps).")
    p.add_argument("--resume-run", default=None, metavar="PATH",
                   help="Path to a previous runs/full/<run_id> directory to resume from.")
    return p.parse_args()


def main() -> None:
    args = _parse_args()

    sft_cfg, sft_ns, sft_tokens = _parse_sft_cfg(args.config, args.sft_args)
    rlvr_cfg, rlvr_ns, rlvr_tokens = _parse_rlvr_cfg(args.config, args.rlvr_args)

    test_file = args.test_file or _default_test_file()
    eval_args, eval_tokens = _parse_eval_args(args.eval_args, args.eval_n_samples, test_file)

    test_path = _REPO_ROOT / eval_args.test_file
    if not test_path.exists():
        raise FileNotFoundError(f"Test file not found: {test_path}")

    records, eval_format, load_stats = eval_runner.load_test_records(
        test_path,
        limit=eval_args.limit,
        drop_v2_unusable=not eval_args.keep_v2_unusable,
    )

    base_model = args.base_model or sft_cfg.model_name

    resume_from = args.resume_from
    resume_state: dict | None = None
    resume_run_dir: Path | None = None
    if resume_from is not None:
        if resume_from in ("sft_eval", "rlvr", "rlvr_eval") and not args.resume_run:
            raise ValueError("--resume-run is required when resuming from sft_eval or later")
        if args.resume_run:
            resume_run_dir = Path(args.resume_run)
            resume_state = _load_resume_state(resume_run_dir)

    full_cfg = FullExperimentConfig(
        config_path=args.config,
        sft_args=sft_tokens,
        rlvr_args=rlvr_tokens,
        eval_args=eval_tokens,
        test_file=eval_args.test_file,
        base_model=base_model,
        eval_n_samples=eval_args.n_samples,
        resume_from=resume_from,
        resume_run=str(resume_run_dir) if resume_run_dir is not None else None,
    )

    full_run_dir = build_run_dir(
        phase="full",
        config_yaml=args.config,
        seed=sft_cfg.seed,
    )
    write_run_metadata(
        run_dir=full_run_dir,
        cfg=full_cfg,
        phase="full",
        cli_namespace=args,
        argv=sys.argv,
        config_yaml=args.config,
        dataset_paths=[eval_args.test_file],
    )

    state_path = full_run_dir / "full_experiment.json"
    timeline_path = full_run_dir / "timeline.jsonl"

    state = {
        "full_run_dir": str(full_run_dir),
        "config": {
            "config_yaml": args.config,
            "sft_args": sft_tokens,
            "rlvr_args": rlvr_tokens,
            "eval_args": eval_tokens,
            "test_file": eval_args.test_file,
            "base_model": base_model,
            "resume_from": resume_from,
            "resume_run": str(resume_run_dir) if resume_run_dir is not None else None,
        },
        "steps": {},
    }
    state_path.write_text(json.dumps(state, indent=2, default=str))

    def _carry_over(step_key: str) -> None:
        if not resume_state:
            return
        prior = resume_state.get("steps", {}).get(step_key)
        if prior:
            state["steps"][step_key] = prior

    def _require_prior_run(step_key: str) -> dict:
        if not resume_state:
            raise RuntimeError(f"resume_from requires prior run info for {step_key}")
        prior = resume_state.get("steps", {}).get(step_key)
        if not prior:
            raise RuntimeError(f"resume_from requires {step_key} in resume state")
        return prior

    try:
        # Baseline evaluation
        if _should_run("baseline_eval", resume_from):
            _append_jsonl(timeline_path, {"event": "baseline_eval_start"})
            base_eval_args = _clone_namespace(eval_args)
            base_eval_args.model = base_model
            base_eval_args.lora_adapter = None
            base_eval_args.model_type = "base"

            producer_run_id = eval_runner._derive_producer_run_id(base_eval_args.model, None)
            base_out_dir, base_summary, _ = _run_in_isolated_process(
                _run_standalone_eval,
                base_eval_args, test_path, records, eval_format, load_stats, "base", producer_run_id
            )
            state["steps"]["baseline_eval"] = {
                "run_dir": str(base_out_dir),
                "summary": base_summary,
            }
            state_path.write_text(json.dumps(state, indent=2, default=str))
            _append_jsonl(timeline_path, {"event": "baseline_eval_done", "run_dir": str(base_out_dir)})
        else:
            _carry_over("baseline_eval")

        # SFT
        if _should_run("sft", resume_from):
            _append_jsonl(timeline_path, {"event": "sft_start"})
            sft_out_dir, probe_summary = _run_in_isolated_process(_run_sft, sft_cfg, sft_ns)
            sft_out_dir = Path(sft_out_dir)
            state["steps"]["sft_train"] = {
                "run_dir": str(sft_out_dir),
                "probe_summary": probe_summary,
            }
            state_path.write_text(json.dumps(state, indent=2, default=str))
            _append_jsonl(timeline_path, {"event": "sft_done", "run_dir": str(sft_out_dir)})
        else:
            prior = _require_prior_run("sft_train")
            sft_out_dir = Path(prior["run_dir"])
            state["steps"]["sft_train"] = prior

        # SFT eval
        if _should_run("sft_eval", resume_from):
            _append_jsonl(timeline_path, {"event": "sft_eval_start"})
            sft_eval_args = _clone_namespace(eval_args)
            sft_eval_args.model = base_model
            sft_eval_args.lora_adapter = str(sft_out_dir / "lora")
            sft_eval_args.model_type = "sft"

            producer_run_id = eval_runner._derive_producer_run_id(
                sft_eval_args.model,
                sft_eval_args.lora_adapter,
            )
            sft_eval_out_dir, sft_eval_summary, _ = _run_in_isolated_process(
                _run_standalone_eval,
                sft_eval_args, test_path, records, eval_format, load_stats, "sft", producer_run_id
            )
            state["steps"]["sft_eval"] = {
                "run_dir": str(sft_eval_out_dir),
                "summary": sft_eval_summary,
            }
            state_path.write_text(json.dumps(state, indent=2, default=str))
            _append_jsonl(timeline_path, {"event": "sft_eval_done", "run_dir": str(sft_eval_out_dir)})
        else:
            _carry_over("sft_eval")


        # RLVR
        if _should_run("rlvr", resume_from):
            _append_jsonl(timeline_path, {"event": "rlvr_start"})
            rlvr_cfg.sft_checkpoint = str(sft_out_dir / "lora")
            rlvr_ns.sft_checkpoint = rlvr_cfg.sft_checkpoint
            rlvr_out_dir, rlvr_epoch_saves = _run_in_isolated_process(
                _run_rlvr,
                rlvr_cfg,
                rlvr_ns,
                eval_args,
                records,
                eval_format,
                load_stats,
                timeline_path,
                base_model
            )
            state["steps"]["rlvr_train"] = {
                "run_dir": str(rlvr_out_dir),
                "epoch_saves": rlvr_epoch_saves,
            }
            state_path.write_text(json.dumps(state, indent=2, default=str))
            _append_jsonl(timeline_path, {"event": "rlvr_done", "run_dir": str(rlvr_out_dir)})
        else:
            prior = _require_prior_run("rlvr_train")
            rlvr_out_dir = prior["run_dir"]
            state["steps"]["rlvr_train"] = prior

        # RLVR eval (final only)
        if _should_run("rlvr_eval", resume_from):
            _append_jsonl(timeline_path, {"event": "rlvr_eval_start"})
            rlvr_eval_args = _clone_namespace(eval_args)
            rlvr_eval_args.model = base_model
            rlvr_eval_args.lora_adapter = str(Path(rlvr_out_dir) / "lora")
            rlvr_eval_args.model_type = "rlvr"

            producer_run_id = eval_runner._derive_producer_run_id(
                rlvr_eval_args.model,
                rlvr_eval_args.lora_adapter,
            )
            rlvr_eval_out_dir, rlvr_eval_summary, _ = _run_in_isolated_process(
                _run_standalone_eval,
                rlvr_eval_args, test_path, records, eval_format, load_stats, "rlvr", producer_run_id
            )
            state["steps"]["rlvr_eval"] = {
                "run_dir": str(rlvr_eval_out_dir),
                "summary": rlvr_eval_summary,
            }
            state_path.write_text(json.dumps(state, indent=2, default=str))
            _append_jsonl(timeline_path, {"event": "rlvr_eval_done", "run_dir": str(rlvr_eval_out_dir)})
        else:
            _carry_over("rlvr_eval")

    except Exception as exc:
        finalise_run(full_run_dir, status="failed", extra={"exception": repr(exc)})
        raise

    final_pass = None
    rlvr_eval = state["steps"].get("rlvr_eval", {})
    if rlvr_eval:
        final_pass = rlvr_eval.get("summary", {}).get("pass_at_1")
    finalise_run(full_run_dir, status="completed", extra={"pass_at_1": final_pass})
    print(f"[done]    Full experiment -> {full_run_dir}")


if __name__ == "__main__":
    main()
