"""
Extract algebraic theorems from Lean 4 Mathlib via LeanDojo.

Falls back to a curated set of hardcoded theorems when LeanDojo is not
available or has not completed its trace, so the rest of the pipeline
can be tested immediately.

Each theorem dict has the shape:
    {
        "id": str,
        "name": str,
        "lean_name": str | None,
        "domain": str,           # e.g. "GroupTheory", "RingTheory"
        "subdomain": str | None,
        "full_statement": str,   # human-readable English statement
        "hypotheses": [
            {
                "id": str,
                "name": str,
                "text": str,
                "droppable": bool,   # True = this hypothesis can be dropped
            },
            ...
        ],
        "conclusion": str,
        "notes": str | None,     # proof sketch / known counterexample hint
        "source": str,           # "hardcoded_fallback" | "leandojo"
        "lean_file": str | None,
    }
"""

import logging
import json
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def _load_fallback_theorems() -> list[dict]:
    """Load fallback theorems from data/fallback_theorems.json next to project root."""
    try:
        root = Path(__file__).resolve().parent.parent
        fallback_path = root / "data" / "fallback_theorems.json"
        if not fallback_path.exists():
            logger.error("Fallback theorems file not found: %s", fallback_path)
            return []
        with open(fallback_path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:
        logger.error("Failed to load fallback theorems: %s", exc)
        return []


def _normalize_hypothesis(hypothesis: object, theorem_id: str, index: int) -> dict:
    """Convert hypothesis data into the internal dict shape used by the pipeline."""
    if isinstance(hypothesis, dict):
        normalized = dict(hypothesis)
        normalized.setdefault("id", f"h{index + 1}")
        normalized.setdefault("name", normalized["id"])
        normalized.setdefault("text", "")
        normalized.setdefault("droppable", bool(normalized.get("droppable", False)))
        return normalized

    text = str(hypothesis)
    return {
        "id": f"{theorem_id}_h{index + 1}",
        "name": f"h{index + 1}",
        "text": text,
        "droppable": True,
    }


def _normalize_theorem(theorem: object, index: int) -> dict:
    """Normalize theorem records from fallback or user-provided JSON input."""
    if not isinstance(theorem, dict):
        raise TypeError(f"Expected theorem dict at index {index}, got {type(theorem).__name__}")

    theorem_id = str(theorem.get("id") or f"thm_{index + 1:03d}")
    name = str(theorem.get("name") or theorem_id)
    full_statement = theorem.get("full_statement") or theorem.get("original_full_statement") or ""
    conclusion = theorem.get("conclusion") or ""
    domain = theorem.get("domain") or "Algebra"
    subdomain = theorem.get("subdomain") or theorem.get("topic")
    hypotheses = theorem.get("hypotheses") or []

    normalized_hypotheses = [
        _normalize_hypothesis(hypothesis, theorem_id, hyp_index)
        for hyp_index, hypothesis in enumerate(hypotheses)
    ]

    return {
        "id": theorem_id,
        "name": name,
        "lean_name": theorem.get("lean_name"),
        "domain": domain,
        "subdomain": subdomain,
        "full_statement": full_statement,
        "hypotheses": normalized_hypotheses,
        "conclusion": conclusion,
        "notes": theorem.get("notes"),
        "source": theorem.get("source") or "input_file",
        "lean_file": theorem.get("lean_file"),
        # P1c will populate this via bounded-search validation; null = not yet checked.
        "original_theorem_validated": theorem.get("original_theorem_validated"),
    }


def _load_theorems_from_file(path: Path) -> list[dict]:
    """Load and normalize theorem records from a JSON file."""
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON array in {path}")

    return [_normalize_theorem(theorem, index) for index, theorem in enumerate(data)]


# ---------------------------------------------------------------------------
# LeanDojo extraction (requires Lean 4 + elan installed)
# ---------------------------------------------------------------------------

_ALGEBRA_MODULES = (
    "Mathlib/Algebra",
    "Mathlib/GroupTheory",
    "Mathlib/RingTheory",
    "Mathlib/LinearAlgebra",
)


def _infer_domain(file_path: str) -> str:
    if "GroupTheory" in file_path:
        return "GroupTheory"
    if "RingTheory" in file_path:
        return "RingTheory"
    if "LinearAlgebra" in file_path:
        return "LinearAlgebra"
    return "Algebra"


def get_lean_theorems(
    repo_url: str = "https://github.com/leanprover-community/mathlib4",
    commit: str = "v4.14.0",
    max_theorems: int = 40,
) -> list[dict]:
    """
    Extract algebraic theorems from Lean 4 Mathlib using LeanDojo.

    First run traces Mathlib (20-40 min); subsequent runs use the cached trace.
    Returns an empty list if LeanDojo is unavailable or tracing fails.

    NOTE: The returned dicts have empty `hypotheses` and `conclusion` fields
    because mapping Lean4 AST hypothesis nodes to English requires a dedicated
    parsing step (TODO for a later milestone). The raw Lean4 statement is
    stored in `full_statement` for reference.
    """
    try:
        from lean_dojo import LeanGitRepo, trace  # type: ignore
    except ImportError:
        logger.warning("lean-dojo not installed or Lean 4 unavailable.")
        return []

    try:
        repo = LeanGitRepo(repo_url, commit)
        logger.info("Tracing Mathlib — first run takes 20-40 minutes...")
        traced = trace(repo)
    except Exception as exc:
        logger.error(f"LeanDojo trace failed: {exc}")
        return []

    results: list[dict] = []
    for thm in traced.theorems:
        if not any(mod in thm.file_path for mod in _ALGEBRA_MODULES):
            continue
        results.append(
            {
                "id": thm.full_name.replace(".", "_"),
                "name": thm.full_name,
                "lean_name": thm.full_name,
                "domain": _infer_domain(thm.file_path),
                "subdomain": None,
                "full_statement": thm.statement,  # raw Lean4 syntax
                "hypotheses": [],  # requires AST parsing — future milestone
                "conclusion": None,
                "notes": None,
                "source": "leandojo",
                "lean_file": thm.file_path,
            }
        )
        if len(results) >= max_theorems:
            break

    logger.info(f"Extracted {len(results)} theorems from Mathlib via LeanDojo")
    return results


def get_theorems(use_lean: bool = False, input_file: Optional[str] = None) -> list[dict]:
    """
    Return a list of theorem dicts ready for mutation and prompting.

    Args:
        use_lean: If True, attempt LeanDojo extraction first and fall back
                  to fallback theorems on failure.
        input_file: Optional path to a JSON file containing an array of theorems.
    """
    # Lean extraction has priority when requested
    if use_lean:
        lean_theorems = get_lean_theorems()
        if lean_theorems:
            return lean_theorems
        logger.warning("LeanDojo extraction failed — using fallback theorems.")

    # If an input file is provided, load and return it
    if input_file:
        try:
            p = Path(input_file)
            data = _load_theorems_from_file(p)
            logger.info(f"Loaded {len(data)} theorems from {p}")
            return data
        except Exception as exc:
            logger.error("Failed to load input theorems file %s: %s", input_file, exc)

    # Otherwise, load the fallback JSON file
    fallbacks = [_normalize_theorem(theorem, index) for index, theorem in enumerate(_load_fallback_theorems())]
    logger.info(f"Using {len(fallbacks)} fallback theorems.")
    return fallbacks
