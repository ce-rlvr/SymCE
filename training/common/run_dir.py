"""
Run-directory builder + metadata stamping.

Every training / eval launch goes through here:

    rdir = build_run_dir(phase="sft", config_yaml=args.config,
                         seed=cfg.seed)
    write_run_metadata(
        run_dir=rdir, cfg=cfg,
        cli_namespace=parsed_args, argv=sys.argv,
        config_yaml=args.config,
        dataset_paths=[cfg.train_jsonl],
    )
    ...
    finalise_run(run_dir=rdir, status="completed", extra={...})

The on-disk layout is:

    runs/
      {phase}/
        {YYYYMMDD-HHMMSS}__{config_basename}__seed{N}__{sha7}/
          config.json                  (resolved dataclass dump)
          invocation.json              (argv, cli namespace, config yaml path, env)
          git_info.json                (sha, branch, dirty flag, remote)
          dataset_fingerprint.json     (sha256 + line count + mtime per dataset)
          status.json                  (started_at, ended_at, status, extra)
          ... whatever the trainer writes alongside (lora/, merged/, train_log.csv,
              rollouts.jsonl, rollouts_summary.json, sft_diagnostics.json,
              run_summary.md, ...)
      index.jsonl                      (one line per status change; append-only)

The runs/ directory is intentionally separate from checkpoints/ so the
legacy paths (checkpoints/sft/qwen25-math-1_5b-r16-bf16/, ...) remain readable
without us having to rewrite them in-place. `tools/migrate_legacy_checkpoints.py`
moves the legacy dirs into runs/ with a synthetic timestamp from mtime.
"""

from __future__ import annotations

import hashlib
import json
import os
import socket
import subprocess
import sys
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

from training.common.paths import REPO_ROOT


RUNS_ROOT: Path = REPO_ROOT / "runs"
INDEX_PATH: Path = RUNS_ROOT / "index.jsonl"


# ---------------------------------------------------------------------------
# Git
# ---------------------------------------------------------------------------

def _run_git(*args: str) -> Optional[str]:
    try:
        out = subprocess.check_output(
            ["git", *args], cwd=str(REPO_ROOT), stderr=subprocess.DEVNULL,
        )
        return out.decode().strip() or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def git_info() -> dict[str, Any]:
    sha = _run_git("rev-parse", "HEAD")
    branch = _run_git("rev-parse", "--abbrev-ref", "HEAD")
    remote = _run_git("config", "--get", "remote.origin.url")
    dirty = bool(_run_git("status", "--porcelain"))
    return {
        "sha": sha,
        "sha7": (sha or "nogit")[:7],
        "branch": branch,
        "remote": remote,
        "dirty": dirty,
    }


# ---------------------------------------------------------------------------
# Dataset fingerprint
# ---------------------------------------------------------------------------

def _sha256_of_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for buf in iter(lambda: fh.read(chunk), b""):
            h.update(buf)
    return h.hexdigest()


def _count_lines(path: Path) -> int:
    n = 0
    with open(path, "rb") as fh:
        for _ in fh:
            n += 1
    return n


def dataset_fingerprint(dataset_paths: Iterable[str | Path]) -> dict[str, dict[str, Any]]:
    """Returns {relative_path: {sha256, sha8, line_count, mtime, bytes}}.

    Silently skips paths that don't exist (with a sentinel entry) - we still
    record the attempt so post-hoc audits can see the trainer was *asked* to
    train on a missing file.
    """
    out: dict[str, dict[str, Any]] = {}
    for p in dataset_paths:
        path = Path(p)
        if not path.is_absolute():
            path = REPO_ROOT / path
        key = str(path.relative_to(REPO_ROOT)) if path.is_relative_to(REPO_ROOT) else str(path)
        if not path.exists():
            out[key] = {"missing": True}
            continue
        sha = _sha256_of_file(path)
        out[key] = {
            "sha256": sha,
            "sha8": sha[:8],
            "line_count": _count_lines(path) if path.suffix == ".jsonl" else None,
            "mtime": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(),
            "bytes": path.stat().st_size,
        }
    return out


# ---------------------------------------------------------------------------
# Run-directory construction
# ---------------------------------------------------------------------------

def _config_basename(config_yaml: Optional[str | Path]) -> str:
    if not config_yaml:
        return "noconfig"
    return Path(config_yaml).stem


def _slugify(s: str) -> str:
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in s)[:64]


def build_run_dir(
    phase: str,
    config_yaml: Optional[str | Path],
    seed: int,
    *,
    now: Optional[datetime] = None,
    extra_tag: Optional[str] = None,
) -> Path:
    """Allocate a unique run directory under ``runs/{phase}/``.

    Collisions (same minute, same config, same seed, same SHA - rare) get an
    ``__r2``, ``__r3``, ... suffix appended so we never silently overwrite.
    """
    ts = (now or datetime.now(tz=timezone.utc)).strftime("%Y%m%d-%H%M%S")
    cfg_name = _slugify(_config_basename(config_yaml))
    sha7 = git_info()["sha7"]
    base_name = f"{ts}__{cfg_name}__seed{seed}__{sha7}"
    if extra_tag:
        base_name = f"{base_name}__{_slugify(extra_tag)}"

    parent = RUNS_ROOT / phase
    parent.mkdir(parents=True, exist_ok=True)
    candidate = parent / base_name
    suffix = 2
    while candidate.exists():
        candidate = parent / f"{base_name}__r{suffix}"
        suffix += 1
    candidate.mkdir(parents=True, exist_ok=False)
    return candidate


# ---------------------------------------------------------------------------
# Metadata stamping
# ---------------------------------------------------------------------------

def _config_to_dict(cfg: Any) -> dict[str, Any]:
    if is_dataclass(cfg):
        return asdict(cfg)
    if hasattr(cfg, "to_dict"):
        try:
            return cfg.to_dict()
        except Exception:
            pass
    if isinstance(cfg, dict):
        return cfg
    return {"_repr": repr(cfg)}


def _wandb_env() -> dict[str, str]:
    keys = (
        "WANDB_PROJECT", "WANDB_ENTITY", "WANDB_RUN_GROUP", "WANDB_NAME",
        "WANDB_MODE", "WANDB_DIR", "WANDB_DISABLED",
        "CUDA_VISIBLE_DEVICES", "ACCELERATE_MIXED_PRECISION",
        "HF_HOME", "TRANSFORMERS_CACHE", "TORCH_DTYPE",
    )
    return {k: os.environ[k] for k in keys if k in os.environ}


def write_run_metadata(
    run_dir: Path,
    cfg: Any,
    *,
    phase: str,
    cli_namespace: Any = None,
    argv: Optional[list[str]] = None,
    config_yaml: Optional[str | Path] = None,
    dataset_paths: Iterable[str | Path] = (),
    extra: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Write config.json + invocation.json + git_info.json + dataset_fingerprint.json
    inside ``run_dir`` and append one start-event line to ``runs/index.jsonl``.

    Returns the run-record dict (also persisted as ``run_dir/status.json``).
    """
    run_dir.mkdir(parents=True, exist_ok=True)
    run_id = run_dir.name

    cfg_dict = _config_to_dict(cfg)
    (run_dir / "config.json").write_text(json.dumps(cfg_dict, indent=2, default=str))

    invocation = {
        "argv": list(argv) if argv is not None else list(sys.argv),
        "cli_namespace": (
            {k: v for k, v in vars(cli_namespace).items() if v is not None}
            if cli_namespace is not None else None
        ),
        "config_yaml": str(config_yaml) if config_yaml else None,
        "cwd": os.getcwd(),
        "host": socket.gethostname(),
        "user": os.environ.get("USER") or os.environ.get("LOGNAME"),
        "python": sys.version.split()[0],
        "env": _wandb_env(),
    }
    (run_dir / "invocation.json").write_text(json.dumps(invocation, indent=2, default=str))

    gi = git_info()
    (run_dir / "git_info.json").write_text(json.dumps(gi, indent=2))

    fp = dataset_fingerprint(dataset_paths)
    (run_dir / "dataset_fingerprint.json").write_text(json.dumps(fp, indent=2))

    started_at = datetime.now(tz=timezone.utc).isoformat()
    record = {
        "run_id": run_id,
        "phase": phase,
        "run_dir": str(run_dir.relative_to(REPO_ROOT)) if run_dir.is_relative_to(REPO_ROOT) else str(run_dir),
        "config_yaml": str(config_yaml) if config_yaml else None,
        "seed": getattr(cfg, "seed", None),
        "git": gi,
        "datasets": fp,
        "status": "started",
        "started_at": started_at,
        "ended_at": None,
        "extra": extra or {},
    }
    (run_dir / "status.json").write_text(json.dumps(record, indent=2, default=str))
    _append_index({"event": "started", **{k: record[k] for k in (
        "run_id", "phase", "run_dir", "config_yaml", "seed", "started_at"
    )}, "git_sha7": gi["sha7"], "git_dirty": gi["dirty"]})
    return record


def finalise_run(
    run_dir: Path,
    *,
    status: str = "completed",
    extra: Optional[dict[str, Any]] = None,
) -> None:
    """Update ``run_dir/status.json`` and append a finish line to index.jsonl."""
    record_path = run_dir / "status.json"
    record: dict[str, Any] = {}
    if record_path.exists():
        try:
            record = json.loads(record_path.read_text())
        except Exception:
            record = {}
    ended_at = datetime.now(tz=timezone.utc).isoformat()
    record["status"] = status
    record["ended_at"] = ended_at
    record["extra"] = {**(record.get("extra") or {}), **(extra or {})}
    record_path.write_text(json.dumps(record, indent=2, default=str))
    _append_index({
        "event": "finished",
        "run_id": record.get("run_id", run_dir.name),
        "phase": record.get("phase"),
        "run_dir": record.get("run_dir", str(run_dir)),
        "status": status,
        "ended_at": ended_at,
        "extra_summary": _summarise_extra(record.get("extra") or {}),
    })


def _summarise_extra(extra: dict[str, Any]) -> dict[str, Any]:
    """Keep the index.jsonl compact: lift only headline-friendly fields."""
    keys = (
        "final_loss", "final_eval_loss", "final_reward_mean",
        "pass_at_1", "tag_parse_rate", "oracle_pass_at_1",
        "max_steps_completed", "elapsed_seconds",
    )
    return {k: extra[k] for k in keys if k in extra}


def _append_index(record: dict[str, Any]) -> None:
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    record["ts"] = datetime.now(tz=timezone.utc).isoformat()
    with open(INDEX_PATH, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, default=str) + "\n")


# ---------------------------------------------------------------------------
# Convenience: derive a W&B run_name from a run_dir
# ---------------------------------------------------------------------------

def derive_wandb_names(
    run_dir: Path,
    phase: str,
    *,
    project_override: Optional[str] = None,
    group_override: Optional[str] = None,
) -> dict[str, str]:
    """Return ({project, group, run_name}) suitable for stamping into env or TRL config.

    Conventions (overridable):
      - project: ``pfe-rlvr-{phase}`` (e.g. ``pfe-rlvr-sft``, ``pfe-rlvr-rlvr``).
      - group:   the config_basename portion of the run_dir leaf.
      - name:    the run_dir leaf (timestamped + seed + sha -> globally unique).
    """
    leaf = run_dir.name
    # leaf is "<ts>__<cfg>__seed<N>__<sha>[__extra]" - group = <cfg>
    parts = leaf.split("__")
    group = parts[1] if len(parts) >= 2 else "default"
    return {
        "project": project_override or f"pfe-rlvr-{phase}",
        "group": group_override or group,
        "name": leaf,
    }
