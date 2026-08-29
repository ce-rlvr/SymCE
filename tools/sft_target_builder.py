"""
Build the SFT assistant target for one v2.0 record.

Per ``docs/PLAN.md`` §P3, the SFT target has the form

    <reasoning>{justification}</reasoning>
    [COUNTEREXAMPLE: {canonical_witness}]

This module produces it deterministically, without an LLM call, from fields
already present in the record:

- ``canonical_witness``        – the SymPy expression the verifier accepts.
- ``verifier.condition_labels`` – the structured per-condition labels.
- ``counterexample_code``     – the legacy v1 script. Its leading ``#`` comments
                                  are the model-authored prose explaining why
                                  this witness works; we extract them as
                                  free-form reasoning text after filtering
                                  any line that could leak the dropped
                                  hypothesis (the v1 generator was told the
                                  dropped hypothesis explicitly; the v2 policy
                                  is not, so leakage would be a training
                                  signal we must not give).

The output is a pure string. Token-length truncation is a separate function so
the caller (``tools/build_v2_splits.py``) can apply a budget under its chosen
tokenizer without this module having to depend on transformers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, Iterable, Optional


# ─────────────────────────────────────────────────────────────────────────────
# Leakage filter
# ─────────────────────────────────────────────────────────────────────────────

# Tokens that strongly indicate a comment is leaking the v1-pipeline knowledge
# of which hypothesis was dropped. Matched case-insensitively as whole words
# (where applicable) on the comment body (after the leading ``#``).
_LEAKAGE_PATTERNS: tuple[re.Pattern, ...] = (
    re.compile(r"\bFALSE\s+CONJECTURE\b", re.IGNORECASE),
    re.compile(r"\bdropped\s+hypothesis\b", re.IGNORECASE),
    re.compile(r"\bdrop(?:s|ped|ping)?\b", re.IGNORECASE),
    re.compile(r"\bremov(?:e|es|ed|ing)\b", re.IGNORECASE),
    re.compile(r"\bomit(?:s|ted|ting)?\b", re.IGNORECASE),
    re.compile(r"\bmissing\s+hypothesis\b", re.IGNORECASE),
    re.compile(r"\bwithout\s+the\s+", re.IGNORECASE),
)


def _record_specific_leakage_patterns(record: dict) -> list[re.Pattern]:
    """Build leakage patterns from record-specific fields.

    The v1 prompt exposed the dropped hypothesis ``text`` and ``name`` (e.g.
    ``"h1"``); the model-authored comments may quote them verbatim. We block
    any comment containing the name as a word, or a long substring of the
    dropped text.
    """
    pats: list[re.Pattern] = []
    name = (record.get("dropped_hypothesis_name") or "").strip()
    if name:
        pats.append(re.compile(rf"\b{re.escape(name)}\b", re.IGNORECASE))
    text = (record.get("dropped_hypothesis") or "").strip()
    # Match meaningful chunks of the dropped-hypothesis text (≥ 12 chars). We
    # split on whitespace and stitch back without punctuation so a sentence
    # like "G is a finite group" matches "finite group" even if punctuation
    # differs in the comment.
    if len(text) >= 12:
        pats.append(re.compile(re.escape(text[:80]), re.IGNORECASE))
        # also any 3-word slice ≥ 12 chars to catch paraphrase
        words = re.findall(r"\w+", text)
        for i in range(len(words) - 2):
            chunk = " ".join(words[i : i + 3])
            if len(chunk) >= 12:
                pats.append(
                    re.compile(rf"\b{re.escape(chunk)}\b", re.IGNORECASE)
                )
    return pats


def _comment_is_safe(comment: str, record_pats: list[re.Pattern]) -> bool:
    """True iff none of the global or record-specific leakage patterns match."""
    for pat in _LEAKAGE_PATTERNS:
        if pat.search(comment):
            return False
    for pat in record_pats:
        if pat.search(comment):
            return False
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Comment extraction
# ─────────────────────────────────────────────────────────────────────────────

# Skip boilerplate that conveys no reasoning content.
_BOILERPLATE_PREFIXES: tuple[str, ...] = (
    "remaining hypotheses",   # "# Remaining hypotheses: G is a group ..."
    "conclusion:",            # "# Conclusion: G is a solvable group."
    "we must assert",
    "we must show",
    "counterexample found",
    "verify",
    "verifying",
    "check:",
    "checks:",
    "import",
    "imports",
    "from",
)


def _is_boilerplate(comment: str) -> bool:
    low = comment.strip().lower()
    return any(low.startswith(p) for p in _BOILERPLATE_PREFIXES)


_COMMENT_LINE = re.compile(r"^\s*#\s?(.*?)\s*$")


def extract_safe_comments(code: str, record: dict) -> list[str]:
    """Pull standalone ``# ...`` comment lines from a v1 counterexample script.

    Strips inline trailing comments (``x = 1  # this``); we only collect
    full-line comments to keep the reasoning prose self-contained. Filters
    leakage and boilerplate.
    """
    if not isinstance(code, str) or not code.strip():
        return []
    record_pats = _record_specific_leakage_patterns(record)
    out: list[str] = []
    for raw_line in code.splitlines():
        m = _COMMENT_LINE.match(raw_line)
        if not m:
            continue
        body = m.group(1).strip()
        if not body or body.startswith("-") or body in ("#", "--"):
            continue
        if _is_boilerplate(body):
            continue
        if not _comment_is_safe(body, record_pats):
            continue
        # Capitalise first letter and normalise trailing punctuation: replace
        # a trailing comma/semicolon/colon with a period; otherwise append a
        # period if none present. Avoids the "…addition,." artefact when the
        # source comment was a clause fragment.
        if body[0].islower():
            body = body[0].upper() + body[1:]
        if body[-1] in ",;:":
            body = body[:-1] + "."
        elif not body.endswith((".", "!", "?")):
            body = body + "."
        out.append(body)
    # De-dup while preserving order.
    seen: set[str] = set()
    deduped: list[str] = []
    for c in out:
        if c not in seen:
            seen.add(c)
            deduped.append(c)
    return deduped


# ─────────────────────────────────────────────────────────────────────────────
# Reasoning block assembly
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class BuildResult:
    """Outcome of one SFT-target build attempt."""
    target: Optional[str]
    skip_reason: Optional[str]
    n_comment_lines: int
    n_condition_lines: int


def _verifier_meta(record: dict) -> Optional[dict]:
    v = record.get("verifier")
    if not isinstance(v, dict):
        return None
    return v


def _format_witness_line(witness: str) -> str:
    return f"We propose the counterexample x = {witness}."


def _format_condition_lines(condition_labels: Iterable[str]) -> list[str]:
    return [f"  - {label} ✓" for label in condition_labels]


_CLOSING_LINE = (
    "All required conditions are met and the negated conclusion holds at x, "
    "so the conjecture is false."
)


def build_reasoning(record: dict, comments: list[str]) -> str:
    """Assemble the inside of the ``<reasoning>...</reasoning>`` block.

    Structure:
        <free-form prose, leakage-filtered>     (may be empty)
        We propose the counterexample x = <witness>.
        This satisfies the required conditions:
          - <label_1> ✓
          - <label_2> ✓
          ...
        <closing line>
    """
    meta = _verifier_meta(record) or {}
    labels: list[str] = list(meta.get("condition_labels", []) or [])
    witness: str = str(record.get("canonical_witness", "")).strip()

    lines: list[str] = []
    if comments:
        lines.extend(comments)
    lines.append(_format_witness_line(witness))
    if labels:
        lines.append("This satisfies the required conditions:")
        lines.extend(_format_condition_lines(labels))
    lines.append(_CLOSING_LINE)
    return "\n".join(lines)


def assemble_target(reasoning_body: str, witness: str) -> str:
    """Compose the full SFT target string from a reasoning body + witness."""
    return (
        f"<reasoning>\n{reasoning_body}\n</reasoning>\n"
        f"[COUNTEREXAMPLE: {witness}]"
    )


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def build_sft_target(record: dict) -> BuildResult:
    """Produce the canonical SFT assistant target for a v2 record.

    Returns BuildResult.target == None with a ``skip_reason`` if the record
    is not SFT-eligible. The caller is responsible for token-length
    truncation (see ``truncate_target_to_fit``).
    """
    witness = (record.get("canonical_witness") or "").strip()
    if not witness:
        return BuildResult(None, "no_canonical_witness", 0, 0)
    if witness == "NONE":
        # A NONE witness is a Stage-2/3 sentinel, not a Stage-1 SFT target.
        return BuildResult(None, "witness_is_none_sentinel", 0, 0)
    if not record.get("witness_passes_verifier"):
        return BuildResult(None, "witness_does_not_pass_verifier", 0, 0)
    meta = _verifier_meta(record)
    if meta is None:
        return BuildResult(None, "no_verifier_metadata", 0, 0)

    comments = extract_safe_comments(record.get("counterexample_code", ""), record)
    reasoning = build_reasoning(record, comments)
    target = assemble_target(reasoning, witness)
    n_condition_lines = len(meta.get("condition_labels") or [])
    return BuildResult(target, None, len(comments), n_condition_lines)


# ─────────────────────────────────────────────────────────────────────────────
# Truncation (token-budget aware)
# ─────────────────────────────────────────────────────────────────────────────

def _split_target(target: str) -> tuple[list[str], str]:
    """Split a built target into (reasoning_lines, tag_line).

    The tag line is the trailing ``[COUNTEREXAMPLE: ...]`` plus its preceding
    ``</reasoning>`` close tag (we keep them adjacent to preserve structure).
    """
    # Find the closing </reasoning> tag — everything after it is tag/closer.
    close = target.rfind("</reasoning>")
    if close == -1:
        # No reasoning to truncate; return target as a single-line block.
        return [], target
    head = target[:close]  # includes "<reasoning>\n...\n"
    tail = target[close:]   # "</reasoning>\n[COUNTEREXAMPLE: ...]"
    # head looks like "<reasoning>\n{lines...}\n"
    if head.startswith("<reasoning>\n"):
        body = head[len("<reasoning>\n"):]
    else:
        body = head
    body = body.rstrip("\n")
    lines = body.splitlines()
    return lines, tail


def truncate_target_to_fit(
    target: str,
    witness: str,
    token_counter: Callable[[str], int],
    max_tokens: int,
    *,
    min_keep_lines: int = 1,
) -> tuple[str, bool]:
    """Walk back ``<reasoning>`` lines from the END until the target fits.

    Returns (truncated_target, was_truncated). The ``[COUNTEREXAMPLE: …]`` tag
    and the witness-proposing line + closing line are preserved as a structural
    minimum (``min_keep_lines`` controls the bottom guard).

    If even the structural minimum does not fit, returns the structural
    minimum and ``was_truncated=True`` so the caller can decide whether to
    skip the record.
    """
    if token_counter(target) <= max_tokens:
        return target, False

    reasoning_lines, tail = _split_target(target)
    if not reasoning_lines:
        return target, True

    # Identify the "must keep" suffix of reasoning_lines: the witness-proposing
    # line ("We propose the counterexample x = ...") through the closing line.
    # We protect everything from the first occurrence of "We propose the
    # counterexample" onwards.
    pivot = 0
    for i, line in enumerate(reasoning_lines):
        if line.startswith("We propose the counterexample"):
            pivot = i
            break
    head_lines = reasoning_lines[:pivot]
    keep_lines = reasoning_lines[pivot:]

    # Drop head_lines one at a time (from the end of head_lines) until fit.
    while head_lines:
        head_lines.pop()
        candidate_body = "\n".join(head_lines + keep_lines).rstrip("\n")
        candidate = f"<reasoning>\n{candidate_body}\n{tail}" if candidate_body else \
                    f"<reasoning>\n{tail}"
        # Strip the duplicate <reasoning>\n if tail already starts with </reasoning>
        # (it does by construction).
        if token_counter(candidate) <= max_tokens:
            return candidate, True

    # head exhausted — also start trimming keep_lines from the top (after the
    # witness line) but always keep at least the witness line.
    while len(keep_lines) > max(1, min_keep_lines):
        # Remove the second-to-last reasoning line (just above the closing).
        # We keep keep_lines[0] (the witness proposal) at all costs.
        if len(keep_lines) <= 2:
            break
        del keep_lines[1]
        candidate_body = "\n".join(keep_lines).rstrip("\n")
        candidate = f"<reasoning>\n{candidate_body}\n{tail}"
        if token_counter(candidate) <= max_tokens:
            return candidate, True

    # Structural minimum reached. Return it even if still over budget; the
    # caller logs/drops as it sees fit.
    candidate_body = "\n".join(keep_lines).rstrip("\n")
    candidate = f"<reasoning>\n{candidate_body}\n{tail}"
    return candidate, True


__all__ = [
    "BuildResult",
    "assemble_target",
    "build_reasoning",
    "build_sft_target",
    "extract_safe_comments",
    "truncate_target_to_fit",
]
