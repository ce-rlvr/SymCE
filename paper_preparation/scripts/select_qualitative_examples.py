"""Surface candidate qualitative examples for the paper.

The paper's Section 6.6 has two boxed examples:

    Example 1 - a TRUE theorem on which SFT confidently fabricates a
                counterexample, RLVR-sparse correctly abstains.
    Example 2 - a FALSE conjecture on which RLVR-dense produces a clean
                witness but RLVR-sparse incorrectly abstains.

This script trawls the per_cell JSONs to surface candidates for each.

It does NOT pick the final examples - the writer should read the top 5-10
candidates and choose. The script writes a markdown report to
`paper_preparation/results/qualitative_candidates.md`.

Inputs (auto-discovered):
- runs/eval/*__suite/per_cell/qwen-*__theorem_truth__v2_counterexample__greedy.json
- runs/eval/*__suite/per_cell/qwen-*__counterexample__v2_counterexample__greedy.json

Usage:
    python -m paper_preparation.scripts.select_qualitative_examples
    python -m paper_preparation.scripts.select_qualitative_examples --top-k 10
"""

from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "paper_preparation" / "results" / "qualitative_candidates.md"

MODELS = ["qwen3-base", "qwen-sft", "qwen-rlvr", "qwen-rlvr-sparse"]


def _load_per_cell(pattern: str) -> dict[str, dict]:
    """Latest per_cell JSON per model name matching pattern."""
    out: dict[str, dict] = {}
    for path in sorted(glob.glob(str(REPO_ROOT / "runs" / "eval" / pattern))):
        with open(path) as fh:
            d = json.load(fh)
        s = d.get("summary", {})
        model = s.get("model")
        if model:
            out[model] = d
    return out


def _record_by_id(per_cell: dict) -> dict[str, dict]:
    """Build {problem_id: record} from a per_cell JSON."""
    return {r["problem_id"]: r for r in per_cell.get("per_record", [])}


def _truncate(text: Optional[str], n: int = 600) -> str:
    if not text:
        return ""
    text = text.replace("\n", " ⏎ ")
    return text[:n] + ("..." if len(text) > n else "")


def find_example_1(top_k: int = 10) -> list[dict]:
    """TRUE theorem (theorem_truth/v2_counterexample/greedy) where:
      - SFT predicts wrong (correct=False, parse_ok=True, NOT is_none/empty)
      - sparse predicts correct (correct=True, is_none or is_empty)
    Sort candidates by SFT confidence proxy (length of payload) descending.
    """
    cells = _load_per_cell(
        "*__suite/per_cell/qwen*__theorem_truth__v2_counterexample__greedy.json"
    )
    required = ["qwen-sft", "qwen-rlvr-sparse"]  # the two we MUST have
    optional = ["qwen-rlvr", "qwen3-base"]
    if not all(m in cells for m in required):
        print(f"[example 1] missing required model cells; have {list(cells)}; need {required}")
        return []
    needed = required + [m for m in optional if m in cells]
    by_model = {m: _record_by_id(cells[m]) for m in needed}
    common = sorted(set.intersection(*[set(d) for d in by_model.values()]))

    rows = []
    for pid in common:
        sft = by_model["qwen-sft"][pid]["samples"][0]
        spa = by_model["qwen-rlvr-sparse"][pid]["samples"][0]
        den_sample = by_model["qwen-rlvr"][pid]["samples"][0] if "qwen-rlvr" in by_model else {}
        bas_sample = by_model["qwen3-base"][pid]["samples"][0] if "qwen3-base" in by_model else {}
        sft_wrong_emit = (
            not sft.get("correct")
            and sft.get("parse_ok")
            and not sft.get("is_none")
            and not sft.get("is_empty")
            and sft.get("payload")
        )
        sparse_correct = bool(spa.get("correct"))
        if sft_wrong_emit and sparse_correct:
            rows.append({
                "problem_id": pid,
                "domain": by_model["qwen-sft"][pid].get("domain"),
                "sft_payload": sft.get("payload"),
                "sft_completion": sft.get("completion"),
                "sparse_payload": spa.get("payload"),
                "sparse_completion": spa.get("completion"),
                "dense_correct": bool(den_sample.get("correct")) if den_sample else None,
                "dense_payload": den_sample.get("payload") if den_sample else None,
                "base_correct": bool(bas_sample.get("correct")) if bas_sample else None,
                "sft_payload_len": len(sft.get("payload") or ""),
            })
    rows.sort(key=lambda r: -r["sft_payload_len"])
    return rows[:top_k]


def find_example_2(top_k: int = 10) -> list[dict]:
    """FALSE conjecture (counterexample/v2_counterexample/greedy) where:
      - dense succeeds (reason=='success', correct=True)
      - sparse abstains (reason in {'none_on_false', 'no_tag'} OR is_none/is_empty/correct=False with parse_ok)
    Sort by dense score descending.
    """
    cells = _load_per_cell(
        "*__suite/per_cell/qwen*__counterexample__v2_counterexample__greedy.json"
    )
    required = ["qwen-rlvr", "qwen-rlvr-sparse"]
    optional = ["qwen-sft", "qwen3-base"]
    if not all(m in cells for m in required):
        print(f"[example 2] missing required model cells; have {list(cells)}; need {required}")
        return []
    needed = required + [m for m in optional if m in cells]
    by_model = {m: _record_by_id(cells[m]) for m in needed}
    common = sorted(set.intersection(*[set(d) for d in by_model.values()]))

    rows = []
    for pid in common:
        den = by_model["qwen-rlvr"][pid]["samples"][0]
        spa = by_model["qwen-rlvr-sparse"][pid]["samples"][0]
        sft_sample = by_model["qwen-sft"][pid]["samples"][0] if "qwen-sft" in by_model else {}
        bas_sample = by_model["qwen3-base"][pid]["samples"][0] if "qwen3-base" in by_model else {}
        dense_success = (den.get("reason") == "success" and den.get("correct"))
        sparse_abstain = (
            spa.get("reason") in ("none_on_false", "no_tag")
            or (spa.get("is_none") or spa.get("is_empty"))
        ) and not spa.get("correct")
        if dense_success and sparse_abstain:
            rows.append({
                "problem_id": pid,
                "domain": by_model["qwen-rlvr"][pid].get("domain"),
                "dense_payload": den.get("extracted") or den.get("payload"),
                "dense_completion": den.get("completion"),
                "dense_score": den.get("score"),
                "sparse_reason": spa.get("reason"),
                "sparse_payload": spa.get("extracted") or spa.get("payload"),
                "sparse_completion": spa.get("completion"),
                "sft_correct": bool(sft_sample.get("correct")) if sft_sample else None,
                "base_correct": bool(bas_sample.get("correct")) if bas_sample else None,
            })
    rows.sort(key=lambda r: -(r["dense_score"] or 0))
    return rows[:top_k]


def render(ex1: list[dict], ex2: list[dict]) -> str:
    md = ["# Qualitative example candidates",
          "",
          "Selection criteria are documented at the top of "
          "`paper_preparation/scripts/select_qualitative_examples.py`.",
          "",
          "Pick **one** from each list. Re-run the script if no candidate looks good.",
          ""]

    md.append("## Example 1 - TRUE-theorem candidates")
    md.append("**Criterion:** SFT confidently emits a wrong counterexample (parse-OK, non-NONE payload); RLVR-sparse correctly identifies the theorem as TRUE.")
    md.append("")
    if not ex1:
        md.append("_No candidates found._")
    else:
        md.append(f"_{len(ex1)} candidates, sorted by SFT payload length (a rough confidence proxy):_")
        md.append("")
        for i, r in enumerate(ex1, 1):
            md.append(f"### Candidate 1.{i} - `{r['problem_id']}` ({r['domain']})")
            md.append(f"- **SFT payload:** `{_truncate(r['sft_payload'], 200)}`")
            md.append(f"- **SFT completion (truncated):** {_truncate(r['sft_completion'], 600)}")
            md.append(f"- **RLVR-sparse payload:** `{_truncate(r['sparse_payload'], 200)}`")
            md.append(f"- **RLVR-dense correct:** {r['dense_correct']} (payload: `{_truncate(r['dense_payload'], 80)}`)")
            md.append(f"- **Base correct:** {r['base_correct']}")
            md.append("")
    md.append("")

    md.append("## Example 2 - FALSE-conjecture candidates")
    md.append("**Criterion:** RLVR-dense produces a correct witness; RLVR-sparse incorrectly abstains.")
    md.append("")
    if not ex2:
        md.append("_No candidates found._")
    else:
        md.append(f"_{len(ex2)} candidates, sorted by dense score descending:_")
        md.append("")
        for i, r in enumerate(ex2, 1):
            md.append(f"### Candidate 2.{i} - `{r['problem_id']}` ({r['domain']})")
            md.append(f"- **Dense payload:** `{_truncate(r['dense_payload'], 200)}` (score {r['dense_score']:.3f})")
            md.append(f"- **Dense completion (truncated):** {_truncate(r['dense_completion'], 600)}")
            md.append(f"- **Sparse reason:** {r['sparse_reason']}")
            md.append(f"- **Sparse payload:** `{_truncate(r['sparse_payload'], 200)}`")
            md.append(f"- **SFT / base correct:** SFT={r['sft_correct']}, base={r['base_correct']}")
            md.append("")
    return "\n".join(md)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--top-k", type=int, default=8)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    ex1 = find_example_1(args.top_k)
    ex2 = find_example_2(args.top_k)
    md = render(ex1, ex2)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(md)
    print(f"Wrote {args.out}")
    print(f"  Example 1 candidates: {len(ex1)}")
    print(f"  Example 2 candidates: {len(ex2)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
