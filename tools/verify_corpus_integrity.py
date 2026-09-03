#!/usr/bin/env python3
"""Check the released splits against their recorded hashes.

Two independent checks:

1. ``--sums`` compares every file listed in ``data/SHA256SUMS`` against its
   current contents. This is the check to run after cloning.

2. ``--against-rev REV`` compares each split with the same file at a git
   revision, ignoring the verifier-path fields. The corpus was published with
   absolute paths from the build machine and later rewritten to repo-relative
   ones; this proves that rewrite touched nothing else.

    python tools/verify_corpus_integrity.py --sums
    python tools/verify_corpus_integrity.py --against-rev 3ce826c

Exit status is non-zero if any check fails.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SUMS = REPO_ROOT / "data" / "SHA256SUMS"

# Fields holding a verifier module location, which the path rewrite touched.
PATH_FIELDS = {
    "data/symce_corpus.jsonl": [("verifier", "module_path")],
    "data/test_set.jsonl": [("verifier", "module_path")],
    "data/rlvr_prompts.jsonl": [("verifier_module_path",)],
    "data/witness_schemas.jsonl": [("file",), ("module_path",)],
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_sums() -> int:
    if not SUMS.is_file():
        print(f"missing {SUMS}", file=sys.stderr)
        return 1
    bad = 0
    for line in SUMS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        recorded, rel = line.split(None, 1)
        path = REPO_ROOT / rel.strip()
        if not path.is_file():
            print(f"  MISSING  {rel.strip()}")
            bad += 1
            continue
        actual = sha256(path)
        ok = actual == recorded
        print(f"  {'ok      ' if ok else 'MISMATCH'} {rel.strip()}")
        bad += 0 if ok else 1
    return bad


def strip_paths(record: dict, keys_list) -> dict:
    for keys in keys_list:
        node = record
        for k in keys[:-1]:
            node = node.get(k) if isinstance(node, dict) else None
            if node is None:
                break
        if isinstance(node, dict):
            node.pop(keys[-1], None)
    return record


def check_against_rev(rev: str) -> int:
    """Compare each split with an older revision, ignoring path fields."""
    renamed = {
        "data/symce_corpus.jsonl": "data/algebra_counterexamples_v2_reconstructed.jsonl",
        "data/test_set.jsonl": "data/test_set_v2.jsonl",
        "data/rlvr_prompts.jsonl": "data/rlvr_prompts_v2.jsonl",
        "data/witness_schemas.jsonl": "data/witness_schemas.jsonl",
    }
    bad = 0
    for rel, keys_list in PATH_FIELDS.items():
        old_name = renamed.get(rel, rel)
        blob = subprocess.run(["git", "-C", str(REPO_ROOT), "show", f"{rev}:{old_name}"],
                              capture_output=True, text=True)
        if blob.returncode != 0:
            print(f"  SKIP     {rel} (not present at {rev} as {old_name})")
            continue
        old = [json.loads(l) for l in blob.stdout.splitlines() if l.strip()]
        new = [json.loads(l) for l in (REPO_ROOT / rel).read_text(encoding="utf-8").splitlines() if l.strip()]
        if len(old) != len(new):
            print(f"  MISMATCH {rel}: {len(old)} records at {rev}, {len(new)} now")
            bad += 1
            continue
        diffs = sum(
            1 for a, b in zip(old, new)
            if json.dumps(strip_paths(a, keys_list), sort_keys=True)
            != json.dumps(strip_paths(b, keys_list), sort_keys=True)
        )
        print(f"  {'ok      ' if diffs == 0 else 'MISMATCH'} {rel}: "
              f"{len(new)} records, {diffs} difference(s) outside the path fields")
        bad += 0 if diffs == 0 else 1
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sums", action="store_true", help="check data/SHA256SUMS")
    ap.add_argument("--against-rev", metavar="REV",
                    help="compare with REV, ignoring the verifier-path fields")
    args = ap.parse_args()
    if not args.sums and not args.against_rev:
        args.sums = True

    bad = 0
    if args.sums:
        print("Checking data/SHA256SUMS:")
        bad += check_sums()
    if args.against_rev:
        print(f"\nComparing with {args.against_rev}, ignoring verifier-path fields:")
        bad += check_against_rev(args.against_rev)

    print("\nAll checks passed." if bad == 0 else f"\n{bad} check(s) failed.")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
