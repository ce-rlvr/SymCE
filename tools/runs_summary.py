"""
Summarise the runs/index.jsonl registry.

The index is append-only: each event (started / finished / migrated) is one
line. This tool collapses events per run_id, surfaces the latest status and
headline metrics, and prints a markdown table you can paste into advisor
check-ins.

Usage:
    python -m tools.runs_summary
    python -m tools.runs_summary --phase rlvr
    python -m tools.runs_summary --since 2026-05-01
    python -m tools.runs_summary --markdown        # markdown only, no header
    python -m tools.runs_summary --json            # one JSON object per run on stdout
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from training.common.paths import REPO_ROOT  # noqa: E402
from training.common.run_dir import INDEX_PATH  # noqa: E402


def _load_runs(index_path: Path) -> dict[str, dict]:
    """Collapse the JSONL event log into one record per run_id (last-write-wins)."""
    runs: dict[str, dict] = {}
    if not index_path.exists():
        return runs
    with open(index_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                evt = json.loads(line)
            except json.JSONDecodeError:
                continue
            run_id = evt.get("run_id")
            if not run_id:
                continue
            runs.setdefault(run_id, {})
            # Merge — later events overwrite earlier fields they touch.
            for k, v in evt.items():
                runs[run_id][k] = v
    return runs


def _read_status(run_dir: Path) -> dict | None:
    """Best-effort: pull richer headline metrics from status.json inside the run dir."""
    if not run_dir.exists():
        return None
    p = run_dir / "status.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def _parse_since(since: str | None) -> datetime | None:
    if not since:
        return None
    try:
        return datetime.fromisoformat(since).replace(tzinfo=timezone.utc)
    except ValueError:
        # Accept YYYY-MM-DD
        return datetime.strptime(since, "%Y-%m-%d").replace(tzinfo=timezone.utc)


def _row_ts(run: dict) -> str:
    return run.get("ended_at") or run.get("started_at") or run.get("ts") or ""


def _filter_runs(
    runs: dict[str, dict], *,
    phase: str | None, since: datetime | None,
) -> list[dict]:
    out: list[dict] = []
    for run_id, r in runs.items():
        if phase and r.get("phase") != phase:
            continue
        if since:
            ts = r.get("started_at") or r.get("ts")
            if ts:
                try:
                    parsed = datetime.fromisoformat(ts)
                    if parsed.tzinfo is None:
                        parsed = parsed.replace(tzinfo=timezone.utc)
                    if parsed < since:
                        continue
                except ValueError:
                    pass
        out.append({"run_id": run_id, **r})
    return sorted(out, key=_row_ts, reverse=True)


def _format_markdown(rows: list[dict]) -> str:
    if not rows:
        return "_(no runs)_\n"
    lines = [
        "| When | Phase | Run | Status | Seed | Headline metrics |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        when = (r.get("ended_at") or r.get("started_at") or r.get("ts") or "")[:19]
        phase = r.get("phase", "?")
        run_id = r.get("run_id", "?")
        status = r.get("status") or ""
        seed = r.get("seed", "")

        # Enrich from on-disk status.json: pulls richer metrics and a proper
        # status field for runs whose only index event was "migrated".
        run_dir = r.get("run_dir")
        extra = {}
        if run_dir:
            sj = _read_status(REPO_ROOT / run_dir)
            if sj:
                extra = sj.get("extra") or {}
                if not status and sj.get("status"):
                    status = sj["status"]
                if not seed and sj.get("seed") is not None:
                    seed = sj["seed"]
        status = status or "?"
        merged_extra = {**(r.get("extra_summary") or {}), **extra}

        headline_bits = []
        if "final_loss" in merged_extra and merged_extra["final_loss"] is not None:
            headline_bits.append(f"loss={merged_extra['final_loss']:.4f}")
        if "tag_parse_rate" in merged_extra and merged_extra["tag_parse_rate"] is not None:
            headline_bits.append(f"tag={merged_extra['tag_parse_rate']:.3f}")
        if "oracle_pass_at_1" in merged_extra and merged_extra["oracle_pass_at_1"] is not None:
            headline_bits.append(f"probe@1={merged_extra['oracle_pass_at_1']:.3f}")
        if "rollouts_mean_reward" in merged_extra and merged_extra["rollouts_mean_reward"] is not None:
            headline_bits.append(f"mean_r={merged_extra['rollouts_mean_reward']:+.3f}")
        if "rollouts_group_std_pos_rate" in merged_extra and merged_extra["rollouts_group_std_pos_rate"] is not None:
            headline_bits.append(f"σ+={merged_extra['rollouts_group_std_pos_rate']:.2f}")
        if "pass_at_1" in merged_extra and merged_extra["pass_at_1"] is not None:
            headline_bits.append(f"P@1={merged_extra['pass_at_1']:.3f}")
        headline = ", ".join(headline_bits) or "_(none)_"

        lines.append(
            f"| {when} | {phase} | `{run_id}` | {status} | {seed} | {headline} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(
        description="List runs from runs/index.jsonl as a markdown table.",
    )
    ap.add_argument("--phase", choices=["sft", "rlvr", "eval"], default=None,
                    help="Filter to one phase.")
    ap.add_argument("--since", default=None, metavar="DATE",
                    help="Only show runs whose started_at >= this ISO date (e.g. 2026-05-01).")
    ap.add_argument("--markdown", action="store_true",
                    help="Print only the markdown table (no header).")
    ap.add_argument("--json", action="store_true",
                    help="One JSON object per run, suitable for jq.")
    ap.add_argument("--index", default=str(INDEX_PATH),
                    help="Override the path to runs/index.jsonl.")
    args = ap.parse_args()

    runs = _load_runs(Path(args.index))
    since = _parse_since(args.since)
    rows = _filter_runs(runs, phase=args.phase, since=since)

    if args.json:
        for r in rows:
            print(json.dumps(r, default=str))
        return

    if not args.markdown:
        print(f"# Runs summary — {datetime.now(tz=timezone.utc).isoformat(timespec='seconds')}")
        print()
        print(f"_{len(rows)} runs"
              + (f", phase={args.phase}" if args.phase else "")
              + (f", since={args.since}" if args.since else "")
              + "_")
        print()
    print(_format_markdown(rows))


if __name__ == "__main__":
    main()
