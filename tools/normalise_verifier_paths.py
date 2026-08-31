#!/usr/bin/env python3
"""Rewrite absolute verifier paths in the released JSONLs to repo-relative ones.

The corpus was built on one machine, and the verifier locations were recorded as
absolute paths under that machine's home directory. Anything that loads a record
and hands the path to ``src.oracle.sandbox.run_oracle`` therefore fails for every
other user, because ``run_oracle`` resolves the path as given.

This script rewrites every such value to ``data/verifiers/<Domain>/<file>.py``,
which ``run_oracle`` resolves against the working directory. It is idempotent:
running it twice is a no-op, and ``--check`` reports without writing.

    python tools/normalise_verifier_paths.py --check
    python tools/normalise_verifier_paths.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# (file, dotted key path) pairs that hold a verifier module location.
TARGETS: list[tuple[str, tuple[str, ...]]] = [
    ("data/algebra_counterexamples_v2_reconstructed.jsonl", ("verifier", "module_path")),
    ("data/test_set_v2.jsonl", ("verifier", "module_path")),
    ("data/rlvr_prompts_v2.jsonl", ("verifier_module_path",)),
    ("data/witness_schemas.jsonl", ("file",)),
    ("data/witness_schemas.jsonl", ("module_path",)),
]

VERIFIERS_PREFIX = "data/verifiers/"


def to_relative(value: str) -> str:
    """Map any absolute or relative verifier path onto data/verifiers/<Domain>/<f>.

    Raises ValueError if the path does not look like a verifier module, so that a
    silent mangling of some unrelated field can never happen.
    """
    posix = value.replace("\\", "/")
    marker = "/verifiers/"
    if posix.startswith(VERIFIERS_PREFIX):
        tail = posix[len(VERIFIERS_PREFIX):]
    elif marker in posix:
        tail = posix.split(marker, 1)[1]
    else:
        raise ValueError(f"not a verifier module path: {value!r}")

    parts = [p for p in tail.split("/") if p]
    if len(parts) != 2 or not parts[1].endswith(".py"):
        raise ValueError(f"unexpected verifier path shape: {value!r}")
    return VERIFIERS_PREFIX + "/".join(parts)


def get_in(rec: dict, keys: tuple[str, ...]):
    node = rec
    for k in keys[:-1]:
        node = node.get(k) if isinstance(node, dict) else None
        if node is None:
            return None, None
    if not isinstance(node, dict):
        return None, None
    return node, node.get(keys[-1])


def process(path: Path, keys: tuple[str, ...], *, write: bool) -> tuple[int, int, int]:
    """Return (records, rewritten, missing_on_disk)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    rewritten = 0
    missing = 0
    for line in lines:
        if not line.strip():
            out.append(line)
            continue
        rec = json.loads(line)
        node, value = get_in(rec, keys)
        if node is not None and isinstance(value, str) and value:
            new = to_relative(value)
            if new != value:
                node[keys[-1]] = new
                rewritten += 1
            if not (REPO_ROOT / new).is_file():
                missing += 1
        out.append(json.dumps(rec, ensure_ascii=False))
    if write and rewritten:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return len(lines), rewritten, missing


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="report what would change; exit 1 if anything would.")
    args = ap.parse_args()

    total_rewritten = 0
    total_missing = 0
    for rel, keys in TARGETS:
        path = REPO_ROOT / rel
        if not path.is_file():
            print(f"skip   {rel}  (not found)")
            continue
        n, rewritten, missing = process(path, keys, write=not args.check)
        total_rewritten += rewritten
        total_missing += missing
        verb = "would rewrite" if args.check else "rewrote"
        note = f"  [{missing} target file(s) missing on disk]" if missing else ""
        print(f"{rel}  ({'.'.join(keys)}): {n} records, {verb} {rewritten}{note}")

    if total_missing:
        print(f"\nWARNING: {total_missing} path(s) do not resolve under "
              f"{REPO_ROOT / VERIFIERS_PREFIX}.", file=sys.stderr)
    if args.check and total_rewritten:
        print(f"\n{total_rewritten} value(s) still absolute. Run without --check to fix.")
        return 1
    print("\nAll verifier paths are repo-relative." if not total_rewritten
          else f"\nDone: {total_rewritten} value(s) rewritten.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
