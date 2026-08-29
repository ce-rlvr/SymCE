"""
Per-theorem verifier generator for the v2.0 independent-verifier pipeline.

Calls Gemini to generate (setup_namespace + conditions_fn) as a single Python
module, then extracts a canonical witness expression from the legacy counterexample
script. Validates both artefacts via the sandbox before returning.

The generated module is written to:
    data/verifiers/<domain>/<theorem_id>__<hyp_name>.py

The module path is then stored in the JSONL record under `verifier.module_path`.
"""

from __future__ import annotations

import logging
import os
import re
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from time import sleep

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Prompt loading
# ---------------------------------------------------------------------------

_PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts"


def _load_prompt(filename: str) -> str:
    path = _PROMPTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def _extract_section(prompt_md: str, heading: str) -> str:
    """Extract the content of a ```...``` block under a given heading."""
    # Find the heading
    pattern = rf"##\s+{re.escape(heading)}.*?```[^\n]*\n(.*?)```"
    match = re.search(pattern, prompt_md, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find '{heading}' section with a code block in prompt file")
    return match.group(1).strip()


# ---------------------------------------------------------------------------
# Gemini model cache (separate from generator_llm.py — different system prompt)
# ---------------------------------------------------------------------------

_model_lock = threading.Lock()
_client_cache: dict[str, Any] = {}


def _get_client() -> Any:
    """Return a cached Gen AI client."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

    if api_key in _client_cache:
        return _client_cache[api_key]

    with _model_lock:
        if api_key not in _client_cache:
            _client_cache[api_key] = genai.Client(api_key=api_key)
    return _client_cache[api_key]


# ---------------------------------------------------------------------------
# Result dataclasses
# ---------------------------------------------------------------------------

@dataclass
class VerifierGenerationResult:
    success: bool
    module_path: Optional[str]
    condition_labels: Optional[list[str]]
    n_conditions: Optional[int]
    n_hyp: Optional[int]
    neg_q_index: Optional[int]
    canonical_witness: Optional[str]
    witness_passes_verifier: bool
    generation_attempts: int
    error: Optional[str]


# ---------------------------------------------------------------------------
# Module source parsing
# ---------------------------------------------------------------------------

def _parse_module_constants(source: str) -> tuple[list[str], int, int]:
    """
    Extract CONDITION_LABELS, N_HYP, NEG_Q_INDEX from generated module source.

    Returns (condition_labels, n_hyp, neg_q_index).
    Raises ValueError if any constant is missing or malformed.
    """
    # CONDITION_LABELS
    labels_match = re.search(
        r"CONDITION_LABELS\s*(?::\s*list\[str\])?\s*=\s*(\[.*?\])",
        source, re.DOTALL
    )
    if not labels_match:
        raise ValueError("CONDITION_LABELS not found in generated module")
    try:
        labels = eval(labels_match.group(1))  # safe: only string literals
        if not isinstance(labels, list) or not all(isinstance(s, str) for s in labels):
            raise ValueError("CONDITION_LABELS must be a list of strings")
    except Exception as exc:
        raise ValueError(f"Could not parse CONDITION_LABELS: {exc}") from exc

    # N_HYP
    nhyp_match = re.search(r"N_HYP\s*(?::\s*int)?\s*=\s*(\d+)", source)
    if not nhyp_match:
        raise ValueError("N_HYP not found in generated module")
    n_hyp = int(nhyp_match.group(1))

    # NEG_Q_INDEX
    negq_match = re.search(r"NEG_Q_INDEX\s*(?::\s*int)?\s*=\s*(\d+)", source)
    if not negq_match:
        raise ValueError("NEG_Q_INDEX not found in generated module")
    neg_q_index = int(negq_match.group(1))

    # Consistency checks
    if neg_q_index != n_hyp:
        raise ValueError(
            f"NEG_Q_INDEX ({neg_q_index}) must equal N_HYP ({n_hyp}) — "
            "negated conclusion must be the last condition"
        )
    if len(labels) != n_hyp + 1:
        raise ValueError(
            f"CONDITION_LABELS length ({len(labels)}) must equal N_HYP+1 ({n_hyp+1})"
        )

    return labels, n_hyp, neg_q_index


def _extract_python_from_response(raw: str) -> str:
    """Strip markdown fences from LLM response if present."""
    match = re.search(r"```[^\n]*\n(.*?)```", raw, re.DOTALL)
    if match:
        return match.group(1).strip()
    return raw.strip()


# ---------------------------------------------------------------------------
# Verifier module generation
# ---------------------------------------------------------------------------

def _build_user_prompt_verifier(record: dict, system_prompt_md: str) -> str:
    """Render the verifier-generation user prompt from a record."""
    remaining = record.get("remaining_hypotheses", [])
    conclusion = record.get("conclusion", "")
    domain = record.get("domain", "Algebra")
    theorem_name = record.get("theorem_name", record.get("theorem_id", "unknown"))

    bulleted = "\n  - ".join(remaining) if remaining else "(none)"

    # Extract just the user prompt section from the MD file
    match = re.search(r"##\s+USER PROMPT TEMPLATE.*?```[^\n]*\n(.*?)```", system_prompt_md, re.DOTALL)
    if not match:
        raise ValueError("USER PROMPT TEMPLATE not found in verifier_generator.md")

    template = match.group(1).strip()
    return template.format(
        domain=domain,
        theorem_name=theorem_name,
        remaining_hypotheses_bulleted=f"  - {bulleted}",
        conclusion=conclusion,
    )


def _build_user_prompt_witness(record: dict, witness_prompt_md: str, use_fallback: bool = False) -> str:
    """Render the witness-extraction user prompt from a record."""
    remaining = record.get("remaining_hypotheses", [])
    conclusion = record.get("conclusion", "")
    domain = record.get("domain", "Algebra")
    counterexample_code = record.get("counterexample_code", "")

    bulleted = "\n".join(f"  - {h}" for h in remaining) if remaining else "  (none)"

    if use_fallback or not counterexample_code.strip():
        # Use fallback prompt
        match = re.search(r"##\s+FALLBACK USER PROMPT TEMPLATE.*?```[^\n]*\n(.*?)```", witness_prompt_md, re.DOTALL)
        if not match:
            raise ValueError("FALLBACK USER PROMPT TEMPLATE not found in witness_extractor.md")
        template = match.group(1).strip()
        return template.format(
            domain=domain,
            remaining_hypotheses_bulleted=bulleted,
            conclusion=conclusion,
        )
    else:
        # Use primary extraction prompt
        match = re.search(r"##\s+USER PROMPT TEMPLATE.*?```[^\n]*\n(.*?)```", witness_prompt_md, re.DOTALL)
        if not match:
            raise ValueError("USER PROMPT TEMPLATE not found in witness_extractor.md")
        template = match.group(1).strip()
        code_snippet = counterexample_code[:3000]  # truncate for safety
        return template.format(
            remaining_hypotheses_bulleted=bulleted,
            conclusion=conclusion,
            counterexample_code=code_snippet,
        )


def _module_filename(record: dict) -> str:
    """Build a safe filename from theorem_id + dropped_hypothesis_name."""
    theorem_id = record.get("theorem_id", "unknown")
    hyp_name = record.get("dropped_hypothesis_name", "h0")
    # Sanitise: allow only alphanumeric, hyphens, underscores
    safe_id = re.sub(r"[^\w\-]", "_", theorem_id)
    safe_hyp = re.sub(r"[^\w\-]", "_", hyp_name)
    return f"{safe_id}__{safe_hyp}.py"


def _module_dir(record: dict, verifiers_dir: Path) -> Path:
    domain = re.sub(r"[^\w\-]", "_", record.get("domain", "Unknown"))
    return verifiers_dir / domain


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_verifier(
    record: dict,
    verifiers_dir: str | Path,
    verifier_model: str = "gemini-3.1-pro-preview",
    verifier_temperature: float = 0.2,
    witness_model: str = "gemini-3.1-pro-preview",
    witness_temperature: float = 0.5,
    max_retries: int = 2,
    sandbox_timeout: float = 8.0,
) -> VerifierGenerationResult:
    """
    Generate a per-theorem verifier module and canonical witness for a record.

    Args:
        record: A v1 pipeline record dict (must contain remaining_hypotheses, conclusion,
                counterexample_code, theorem_id, dropped_hypothesis_name, domain).
        verifiers_dir: Root directory for verifier modules (e.g. data/verifiers/).
        verifier_model / verifier_temperature: Gemini model for verifier code generation.
        witness_model / witness_temperature: Gemini model for witness extraction.
        max_retries: Correction turns if sandbox rejects the verifier (per stage).
        sandbox_timeout: Seconds allowed for each oracle subprocess call.

    Returns:
        VerifierGenerationResult with module_path, labels, witness, and pass/fail status.
    """
    from src.oracle.sandbox import run_oracle  # late import to avoid circular

    verifiers_dir = Path(verifiers_dir)

    # Load prompts
    verifier_prompt_md = _load_prompt("verifier_generator.md")
    witness_prompt_md = _load_prompt("witness_extractor.md")

    verifier_sys = _extract_section(verifier_prompt_md, "SYSTEM PROMPT")
    witness_sys = _extract_section(witness_prompt_md, "SYSTEM PROMPT")

    client = _get_client()

    # Determine output path
    out_dir = _module_dir(record, verifiers_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    module_path = out_dir / _module_filename(record)

    # -----------------------------------------------------------------------
    # Stage A: Generate verifier module
    # -----------------------------------------------------------------------
    user_prompt_v = _build_user_prompt_verifier(record, verifier_prompt_md)
    chat_v = client.chats.create(
        model=verifier_model,
        config=types.GenerateContentConfig(
            system_instruction=verifier_sys,
            temperature=verifier_temperature,
            max_output_tokens=32768,
            candidate_count=1,
        ),
    )

    source: str | None = None
    condition_labels: list[str] | None = None
    n_hyp: int | None = None
    neg_q_index: int | None = None
    generation_attempts = 0
    last_error: str | None = None

    for attempt in range(max_retries + 1):
        generation_attempts += 1
        try:
            if attempt == 0:
                from src.generator_llm import _send_with_retry
                resp = _send_with_retry(chat_v, user_prompt_v)
            else:
                correction_msg = (
                    f"The generated module failed validation:\n{last_error}\n\n"
                    "Please fix the issue and regenerate the complete module. "
                    "Remember: output ONLY the Python file, no prose, no markdown fences."
                )
                from src.generator_llm import _send_with_retry
                resp = _send_with_retry(chat_v, correction_msg)
        except RuntimeError as exc:
            return VerifierGenerationResult(
                success=False, module_path=None, condition_labels=None,
                n_conditions=None, n_hyp=None, neg_q_index=None,
                canonical_witness=None, witness_passes_verifier=False,
                generation_attempts=generation_attempts,
                error=f"Gemini API error: {exc}",
            )

        raw_source = _extract_python_from_response(resp.text or "")

        # Parse constants
        try:
            condition_labels, n_hyp, neg_q_index = _parse_module_constants(raw_source)
        except ValueError as exc:
            last_error = f"Module constants parse error: {exc}"
            logger.warning("Verifier parse error (attempt %d): %s", attempt + 1, exc)
            continue

        # Write module to disk for sandbox execution
        module_path.write_text(raw_source, encoding="utf-8")
        source = raw_source

        # Quick syntax check via subprocess (don't run full oracle yet — no witness)
        import subprocess, tempfile, sys, os as _os
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", prefix="syntax_check_", delete=False) as tmp:
            tmp.write(f"import importlib.util\n"
                      f"spec = importlib.util.spec_from_file_location('m', {str(module_path)!r})\n"
                      f"mod = importlib.util.module_from_spec(spec)\n"
                      f"spec.loader.exec_module(mod)\n"
                      f"print('ok')\n")
            tmp_path = tmp.name
        try:
            proc = subprocess.run(
                [sys.executable, tmp_path], capture_output=True, text=True, timeout=sandbox_timeout
            )
            if proc.returncode != 0:
                last_error = f"Module load error:\n{proc.stderr[-600:]}"
                logger.warning("Module load check failed (attempt %d): %s", attempt + 1, last_error)
                continue
        except subprocess.TimeoutExpired:
            last_error = f"Module load timed out after {sandbox_timeout}s"
            continue
        finally:
            if _os.path.exists(tmp_path):
                _os.unlink(tmp_path)

        # Syntax + load passed
        break
    else:
        return VerifierGenerationResult(
            success=False, module_path=None, condition_labels=None,
            n_conditions=None, n_hyp=None, neg_q_index=None,
            canonical_witness=None, witness_passes_verifier=False,
            generation_attempts=generation_attempts,
            error=f"Verifier generation failed after {generation_attempts} attempts: {last_error}",
        )

    # -----------------------------------------------------------------------
    # Stage B: Extract canonical witness
    # -----------------------------------------------------------------------
    chat_w = client.chats.create(
        model=witness_model,
        config=types.GenerateContentConfig(
            system_instruction=witness_sys,
            temperature=witness_temperature,
            max_output_tokens=8192,
            candidate_count=1,
        ),
    )
    canonical_witness: str | None = None
    witness_passes = False
    witness_error: str | None = None
    use_fallback = False

    for attempt in range(max_retries + 1):
        try:
            if attempt == 0:
                user_prompt_w = _build_user_prompt_witness(record, witness_prompt_md, use_fallback=use_fallback)
                from src.generator_llm import _send_with_retry
                resp_w = _send_with_retry(chat_w, user_prompt_w)
            else:
                correction_msg = (
                    f"The witness expression '{candidate_expr}' failed validation:\n"
                    f"{witness_error}\n\n"
                    "Please provide a corrected witness expression. Output ONLY the Python expression, "
                    "one line, no explanation."
                )
                from src.generator_llm import _send_with_retry
                resp_w = _send_with_retry(chat_w, correction_msg)
        except Exception as exc:
            witness_error = f"Error in witness stage: {exc}"
            break

        resp_w_text = resp_w.text or ""
        candidate_expr = resp_w_text.strip().splitlines()[0].strip() if resp_w_text.strip() else ""
        # Strip any accidental quotes
        candidate_expr = candidate_expr.strip('"\'`')

        oracle_result = run_oracle(
            verifier_module_path=str(module_path),
            witness_expr=candidate_expr,
            n_conditions=n_hyp + 1,
            timeout_seconds=sandbox_timeout,
        )

        if oracle_result.parse_ok and oracle_result.conditions is not None:
            if all(oracle_result.conditions):
                canonical_witness = candidate_expr
                witness_passes = True
                witness_error = None
                break
            else:
                failed = [
                    condition_labels[i]
                    for i, ok in enumerate(oracle_result.conditions)
                    if not ok
                ]
                witness_error = f"Not all conditions satisfied. Failed: {failed}"
        else:
            witness_error = oracle_result.error or "Oracle returned no conditions"
            if not use_fallback and not record.get("counterexample_code", "").strip():
                use_fallback = True

    n_conditions = (n_hyp + 1) if n_hyp is not None else None

    return VerifierGenerationResult(
        success=(source is not None),
        module_path=str(module_path) if source is not None else None,
        condition_labels=condition_labels,
        n_conditions=n_conditions,
        n_hyp=n_hyp,
        neg_q_index=neg_q_index,
        canonical_witness=canonical_witness,
        witness_passes_verifier=witness_passes,
        generation_attempts=generation_attempts,
        error=None if (source is not None and witness_passes) else (witness_error or last_error),
    )
