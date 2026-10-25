#!/usr/bin/env python3
"""Assemble the Hugging Face dataset repository for SymCE.

Produces a directory that can be uploaded verbatim:

    python hf_release/build_dataset.py --out hf_release/build/SymCE
    hf upload ce-rlvr/SymCE hf_release/build/SymCE . --repo-type dataset

Every count written into the dataset card is measured from the files being
shipped, so the card cannot drift from the data.

The 12,376 verifier modules are shipped two ways: as `verifiers.jsonl`, which the
Hub's dataset viewer can browse and `load_dataset` can read, and as a
deterministic `verifiers.tar.gz` for anyone who wants the tree on disk. They are
not uploaded as 12,376 loose files, which the Hub handles poorly.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

# local file -> name in the dataset repo
JSONL_FILES = {
    "data/symce_corpus.jsonl": "corpus.jsonl",
    "data/test_set.jsonl": "test.jsonl",
    "data/sft_data.jsonl": "sft.jsonl",
    "data/rlvr_prompts.jsonl": "rlvr_prompts.jsonl",
    "data/theorem_truth_eval.jsonl": "theorem_truth.jsonl",
    "data/witness_schemas.jsonl": "witness_schemas.jsonl",
}

AUDIT_FILES = {
    "human_eval/accepted_counterexamples_review.csv": "human_audit/accepted.csv",
    "human_eval/rejected_counterexamples_review.csv": "human_audit/rejected.csv",
    "human_eval/README.md": "human_audit/README.md",
}

DOMAINS = ["GroupTheory", "RingTheory", "NumberTheory",
           "LinearAlgebra", "FieldTheory", "RealAnalysis"]


def count_lines(path: Path) -> int:
    with path.open(encoding="utf-8") as fh:
        return sum(1 for line in fh if line.strip())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def guard_paths_are_relative() -> None:
    """Refuse to ship a corpus whose verifier paths point at one machine."""
    script = REPO_ROOT / "tools" / "normalise_verifier_paths.py"
    result = subprocess.run([sys.executable, str(script), "--check"],
                            cwd=REPO_ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit(
            "\nRefusing to build: verifier paths are still absolute.\n"
            "Run  python tools/normalise_verifier_paths.py  first."
        )


def build_verifiers(out: Path) -> tuple[int, dict[str, int]]:
    """Write verifiers.jsonl and a deterministic verifiers.tar.gz."""
    src = REPO_ROOT / "data" / "verifiers"
    modules = sorted(src.rglob("*.py"), key=lambda p: str(p.relative_to(src)))
    per_domain: dict[str, int] = {}

    with (out / "verifiers.jsonl").open("w", encoding="utf-8") as fh:
        for m in modules:
            rel = m.relative_to(src)
            domain = rel.parts[0]
            per_domain[domain] = per_domain.get(domain, 0) + 1
            stem = m.stem
            theorem_id, _, hyp = stem.rpartition("__")
            fh.write(json.dumps({
                "module_path": f"data/verifiers/{rel.as_posix()}",
                "domain": domain,
                "theorem_id": theorem_id or stem,
                "dropped_hypothesis": hyp,
                "source": m.read_text(encoding="utf-8"),
            }, ensure_ascii=False) + "\n")

    # Fixed mtime/uid/gid so the archive is byte-identical across rebuilds.
    def scrub(ti: tarfile.TarInfo) -> tarfile.TarInfo:
        ti.mtime, ti.uid, ti.gid = 0, 0, 0
        ti.uname = ti.gname = ""
        return ti

    with tarfile.open(out / "verifiers.tar.gz", "w:gz", compresslevel=9) as tf:
        for m in modules:
            tf.add(m, arcname=f"verifiers/{m.relative_to(src).as_posix()}", filter=scrub)

    return len(modules), per_domain


CARD = """---
license: cc-by-4.0
language:
- en
pretty_name: SymCE
size_categories:
- 1K<n<10K
task_categories:
- text-generation
tags:
- mathematics
- counterexample-generation
- theorem-proving
- symbolic-verification
- rlvr
- reinforcement-learning
- arxiv:2610.02444
configs:
- config_name: corpus
  data_files:
  - split: train
    path: corpus.jsonl
- config_name: test
  data_files:
  - split: test
    path: test.jsonl
- config_name: sft
  data_files:
  - split: train
    path: sft.jsonl
- config_name: rlvr
  data_files:
  - split: train
    path: rlvr_prompts.jsonl
- config_name: theorem_truth
  data_files:
  - split: test
    path: theorem_truth.jsonl
- config_name: witness_schemas
  data_files:
  - split: train
    path: witness_schemas.jsonl
- config_name: verifiers
  data_files:
  - split: train
    path: verifiers.jsonl
---

# SymCE

**{n_corpus:,} false undergraduate algebra and real-analysis conjectures, each with an
executable Python verifier.**

Every record is a true theorem with one hypothesis removed. A verifier module
decides, for a candidate witness, whether each remaining hypothesis holds and
whether the conclusion fails. Verification takes about 130 ms, so the same
substrate serves as the reward function during reinforcement learning: SymCE is a
training environment, not only a benchmark.

Companion to *Counterexample Generation via Per-Theorem Symbolic Verifiers: When
Imitation Hurts and Reinforcement Repairs* (Findings of EMNLP 2026).

- Paper: https://aclanthology.org/2026.findings-emnlp.2112/
- arXiv: https://arxiv.org/abs/2610.02444
- Project page: https://ce-rlvr.github.io/SymCE/
- Code: https://github.com/ce-rlvr/SymCE

## Configurations

| Config | Rows | Contents |
|---|---:|---|
| `corpus` | {n_corpus:,} | Every retained record: statement, hypotheses, conclusion, dropped hypothesis, canonical witness, verifier pointer |
| `test` | {n_test:,} | Held-out counterexample benchmark, stratified by domain |
| `sft` | {n_sft:,} | Supervised fine-tuning split, chat-formatted |
| `rlvr` | {n_rlvr:,} | RLVR prompt set with the oracle metadata GRPO needs |
| `theorem_truth` | {n_truth:,} | Calibration probe. These theorems are **true**; the correct answer is `NONE` |
| `witness_schemas` | {n_schemas:,} | One-line Python-shape description of an acceptable witness per module |
| `verifiers` | {n_verifiers:,} | Every generated verifier module, with its source |

```python
from datasets import load_dataset

test = load_dataset("ce-rlvr/SymCE", "test")["test"]
print(test[0]["false_conjecture"])
```

The verifier tree is also shipped as `verifiers.tar.gz` for local execution:

```bash
hf download ce-rlvr/SymCE verifiers.tar.gz --repo-type dataset --local-dir .
tar xzf verifiers.tar.gz          # -> verifiers/<Domain>/<theorem_id>__<hyp>.py
```

Paths inside the records are written as `data/verifiers/<Domain>/<file>.py`, which
matches the layout of the code repository.

## Running a verifier

```python
from src.oracle.sandbox import run_oracle          # from the code repository

run_oracle("data/verifiers/GroupTheory/abelian_direct_product__h1.py",
           "(SymmetricGroup(3), CyclicGroup(2))", n_conditions=2).conditions
# [True, True]   -> the remaining hypothesis holds and the conclusion fails
```

The module returns one boolean per remaining hypothesis followed by one for the
negated conclusion. A witness counts as a counterexample only when all of them
are true. No language model judges the answer.

## Domains

{domain_table}

## Splits

Stratified per domain with a fixed seed (42). The strict pool is the
{n_strict:,} records whose teacher-generated canonical witness passes its own
verifier; the remaining {n_loose:,} records have a working verifier but no
oracle-confirmed witness, and are used only as RLVR prompts.

## Verifier reliability

Verifiers are written by a teacher model, so their reliability was measured
rather than assumed. Judging verifier *source* proved unworkable: the code leans
on heuristics that are incomplete in theory but correct on the cases that arise.
The accept/reject *decision* on real model outputs was audited instead:

- 177 decisions checked by hand, **97.7 % correct**
- 99/101 accepted witnesses genuinely valid (2.0 % false-accept rate)
- 74/76 rejections genuinely correct
- no case traced to a faulty verifier module

The annotations, including all four disputed decisions, are in `human_audit/`.

## Known limitations

Mutations are single-hypothesis drops only, so the corpus does not span the range
of mathematical fallacies. Verifiers are bounded by what SymPy and Z3 decide,
which excludes topology and higher-order logic. All verifiers come from a single
teacher model (Gemini 3.1 Pro); the witness schemas come from a second
(DeepSeek). The audit had one annotator, so there is no inter-annotator
agreement figure.

## Licence

CC BY 4.0. The corpus consists of formal mathematical statements and their
hypothesis-dropped mutations. It contains no human-derived text and no personal
information.

## Citation

```bibtex
@inproceedings{{zouak-etal-2026-counterexample,
    title = "Counterexample Generation via Per-Theorem Symbolic Verifiers: When Imitation Hurts and Reinforcement Repairs",
    author = "Zouak, Omar Farouk  and
      Boukhalfa, Houssam Eddine  and
      Lakehal, Soumaya  and
      Katiyar, Shiv  and
      Nefti-Meziani, Samia",
    editor = "Lee, Hung-Yi  and
      Dev, Sunipa  and
      Li, Jessy  and
      Elliott, Desmond",
    booktitle = "Findings of the {{A}}ssociation for {{C}}omputational {{L}}inguistics: {{EMNLP}} 2026",
    month = oct,
    year = "2026",
    address = "Budapest, Hungary",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.findings-emnlp.2112/",
    pages = "45032--45047",
    ISBN = "979-8-89176-462-0",
}}
```
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="hf_release/build/SymCE",
                    help="output directory (will be replaced)")
    args = ap.parse_args()

    guard_paths_are_relative()

    out = (REPO_ROOT / args.out) if not Path(args.out).is_absolute() else Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    (out / "human_audit").mkdir(parents=True)

    counts: dict[str, int] = {}
    for src_rel, dst_rel in JSONL_FILES.items():
        src = REPO_ROOT / src_rel
        dst = out / dst_rel
        shutil.copy2(src, dst)
        counts[dst_rel] = count_lines(dst)
        print(f"  {dst_rel:24s} {counts[dst_rel]:6,d} rows")

    for src_rel, dst_rel in AUDIT_FILES.items():
        src = REPO_ROOT / src_rel
        if src.is_file():
            shutil.copy2(src, out / dst_rel)

    shutil.copy2(REPO_ROOT / "LICENSE-DATA", out / "LICENSE")
    shutil.copy2(REPO_ROOT / "data" / "dataset_stats.json", out / "dataset_stats.json")

    n_verifiers, per_domain = build_verifiers(out)
    print(f"  verifiers.jsonl          {n_verifiers:6,d} modules")
    print(f"  verifiers.tar.gz         {(out / 'verifiers.tar.gz').stat().st_size / 1e6:.1f} MB")

    stats = json.loads((REPO_ROOT / "data" / "dataset_stats.json").read_text())
    pools = stats["pools"]
    dom = stats["domain_breakdown_strict_pool"]

    rows = ["| Domain | Strict pool | SFT | RLVR | Test | Verifier modules |",
            "|---|---:|---:|---:|---:|---:|"]
    for d in DOMAINS:
        b = dom[d]
        rows.append(f"| {d} | {b['strict_total']:,} | {b['sft']:,} | "
                    f"{b['rlvr_strict']:,} | {b['test']:,} | {per_domain.get(d, 0):,} |")

    card = CARD.format(
        n_corpus=counts["corpus.jsonl"],
        n_test=counts["test.jsonl"],
        n_sft=counts["sft.jsonl"],
        n_rlvr=counts["rlvr_prompts.jsonl"],
        n_truth=counts["theorem_truth.jsonl"],
        n_schemas=counts["witness_schemas.jsonl"],
        n_verifiers=n_verifiers,
        n_strict=pools["strict"],
        n_loose=pools["loose_only"],
        domain_table="\n".join(rows),
    )
    (out / "README.md").write_text(card, encoding="utf-8")

    manifest = {p.relative_to(out).as_posix(): {"bytes": p.stat().st_size,
                                                "sha256": sha256(p)}
                for p in sorted(out.rglob("*")) if p.is_file()}
    (out / "MANIFEST.sha256.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")

    total = sum(v["bytes"] for v in manifest.values())
    print(f"\nBuilt {out}  ({total / 1e6:.1f} MB, {len(manifest)} files)")
    print("\nUpload with:")
    print(f"  hf upload ce-rlvr/SymCE {out.relative_to(REPO_ROOT)} . --repo-type dataset")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
