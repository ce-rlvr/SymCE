"""
One-shot migration: move legacy checkpoint and eval-result directories into
the new ``runs/`` layout introduced alongside ``training/common/run_dir.py``.

Source dirs:
  - checkpoints/sft/<name>/        → runs/sft/<ts>__legacy_<name>__seed?__nogit/
  - checkpoints/rlvr/<name>/       → runs/rlvr/<ts>__legacy_<name>__seed?__nogit/
  - training/eval/results/*.json   → runs/eval/<ts>__legacy_<basename>/ ...

Idempotent: if the source dir is gone or the destination already exists, the
entry is skipped. Each migrated run is registered in runs/index.jsonl with
``event=migrated`` so post-hoc audits know where it came from.

Usage:
    python -m tools.migrate_legacy_checkpoints           # dry run (default)
    python -m tools.migrate_legacy_checkpoints --apply   # actually move
    python -m tools.migrate_legacy_checkpoints --apply --no-eval-results

The synthetic timestamp is derived from the source dir's mtime so the
ordering in ``runs/`` reflects when the run actually happened.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from training.common.paths import REPO_ROOT  # noqa: E402
from training.common.run_dir import RUNS_ROOT, _append_index  # noqa: E402


def _ts_from_mtime(p: Path) -> str:
    return datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).strftime("%Y%m%d-%H%M%S")


def _slug(s: str) -> str:
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in s)[:80]


def _read_existing_config(src: Path) -> dict | None:
    """Look for an existing config.json in the source dir (HF Trainer writes one)."""
    candidates = [src / "config.json"]
    for c in candidates:
        if c.exists():
            try:
                return json.loads(c.read_text())
            except Exception:
                pass
    return None


def _migrate_checkpoint_dir(src: Path, phase: str, dry_run: bool) -> tuple[Path | None, str]:
    """Move a single legacy checkpoint dir into runs/{phase}/. Returns (dst, status)."""
    if not src.is_dir():
        return None, "skipped: not a directory"
    ts = _ts_from_mtime(src)
    cfg_name = _slug(src.name)
    leaf = f"{ts}__legacy_{cfg_name}__seed_unknown__nogit"
    dst = RUNS_ROOT / phase / leaf
    if dst.exists():
        return dst, "skipped: destination exists"
    if dry_run:
        return dst, "would move"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))

    # Stamp a minimal status.json + invocation breadcrumb so the run is
    # legible alongside fresh runs/.
    existing_cfg = _read_existing_config(dst)
    status = {
        "run_id": leaf,
        "phase": phase,
        "run_dir": str(dst.relative_to(REPO_ROOT)),
        "config_yaml": None,
        "seed": (existing_cfg or {}).get("seed"),
        "git": {"sha": None, "sha7": "nogit", "branch": None, "remote": None, "dirty": None},
        "datasets": {},
        "status": "migrated_from_legacy",
        "started_at": None,
        "ended_at": datetime.fromtimestamp(dst.stat().st_mtime, tz=timezone.utc).isoformat(),
        "extra": {"legacy_source": f"checkpoints/{phase}/{src.name}"},
    }
    (dst / "status.json").write_text(json.dumps(status, indent=2, default=str))
    if not (dst / "config.json").exists() and existing_cfg:
        (dst / "config.json").write_text(json.dumps(existing_cfg, indent=2, default=str))

    _append_index({
        "event": "migrated",
        "run_id": leaf,
        "phase": phase,
        "run_dir": str(dst.relative_to(REPO_ROOT)),
        "legacy_source": f"checkpoints/{phase}/{src.name}",
    })
    return dst, "moved"


def migrate_checkpoints(dry_run: bool) -> int:
    count = 0
    for phase in ("sft", "rlvr"):
        legacy_root = REPO_ROOT / "checkpoints" / phase
        if not legacy_root.exists():
            continue
        for src in sorted(legacy_root.iterdir()):
            dst, status = _migrate_checkpoint_dir(src, phase, dry_run)
            print(f"  [{phase}] {src.name:55s}  {status:25s}  → {dst.relative_to(REPO_ROOT) if dst else '(n/a)'}")
            if status == "moved":
                count += 1
    return count


def _migrate_eval_result_pair(full_path: Path, dry_run: bool) -> tuple[Path | None, str]:
    """Pair a ``<run_id>_<model_type>.json`` with its ``_summary.json`` and move both."""
    if full_path.name.endswith("_summary.json"):
        return None, "skipped: summary handled with parent"
    name = full_path.stem  # e.g. 20260507_140224_base
    summary_path = full_path.with_name(f"{name}_summary.json")
    ts = _ts_from_mtime(full_path)
    leaf = f"{ts}__legacy__{_slug(name)}"
    dst = RUNS_ROOT / "eval" / leaf
    if dst.exists():
        return dst, "skipped: destination exists"
    if dry_run:
        return dst, "would move"
    dst.mkdir(parents=True, exist_ok=False)
    shutil.move(str(full_path), str(dst / "eval_result.json"))
    if summary_path.exists():
        shutil.move(str(summary_path), str(dst / "eval_summary.json"))

    # Best-effort: pull meta from the moved result
    meta: dict = {}
    try:
        with open(dst / "eval_result.json") as fh:
            meta = (json.load(fh) or {}).get("meta", {})
    except Exception:
        pass

    status = {
        "run_id": leaf,
        "phase": "eval",
        "run_dir": str(dst.relative_to(REPO_ROOT)),
        "config_yaml": None,
        "seed": meta.get("seed"),
        "git": {"sha": None, "sha7": "nogit", "branch": None, "remote": None, "dirty": None},
        "datasets": {},
        "status": "migrated_from_legacy",
        "started_at": meta.get("timestamp"),
        "ended_at": datetime.fromtimestamp(dst.stat().st_mtime, tz=timezone.utc).isoformat(),
        "extra": {"legacy_source": f"training/eval/results/{full_path.name}", **meta},
    }
    (dst / "status.json").write_text(json.dumps(status, indent=2, default=str))
    _append_index({
        "event": "migrated",
        "run_id": leaf,
        "phase": "eval",
        "run_dir": str(dst.relative_to(REPO_ROOT)),
        "legacy_source": f"training/eval/results/{full_path.name}",
    })
    return dst, "moved"


def migrate_eval_results(dry_run: bool) -> int:
    src_dir = REPO_ROOT / "training" / "eval" / "results"
    if not src_dir.exists():
        return 0
    count = 0
    for path in sorted(src_dir.glob("*.json")):
        # Skip already-grouped summary files; they're handled with their parent
        if path.name.endswith("_summary.json"):
            continue
        dst, status = _migrate_eval_result_pair(path, dry_run)
        print(f"  [eval] {path.name:55s}  {status:25s}  → "
              f"{dst.relative_to(REPO_ROOT) if dst else '(n/a)'}")
        if status == "moved":
            count += 1
    # If we moved everything, the leftover directory + any orphan summaries can
    # be inspected manually. We do not delete the directory itself.
    return count


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Move legacy checkpoint + eval-result dirs into runs/",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    ap.add_argument("--apply", action="store_true",
                    help="Actually move files. Default is dry-run.")
    ap.add_argument("--no-checkpoints", action="store_true",
                    help="Skip checkpoints/sft and checkpoints/rlvr migration.")
    ap.add_argument("--no-eval-results", action="store_true",
                    help="Skip training/eval/results migration.")
    args = ap.parse_args()
    dry = not args.apply

    print(f"Mode: {'DRY-RUN' if dry else 'APPLY'}")
    print(f"Runs root: {RUNS_ROOT.relative_to(REPO_ROOT)}")
    print()

    moved_ckpt = 0
    moved_eval = 0
    if not args.no_checkpoints:
        print("=== checkpoints/{sft,rlvr}/ ===")
        moved_ckpt = migrate_checkpoints(dry)
        print()
    if not args.no_eval_results:
        print("=== training/eval/results/ ===")
        moved_eval = migrate_eval_results(dry)
        print()

    print(f"{'Would move' if dry else 'Moved'} {moved_ckpt} checkpoint dirs, "
          f"{moved_eval} eval result pairs.")
    if dry:
        print("Re-run with --apply to perform the migration.")


if __name__ == "__main__":
    main()
