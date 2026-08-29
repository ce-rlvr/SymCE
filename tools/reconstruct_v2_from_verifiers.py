"""
Reconstruct v2 JSONL records from existing verifier modules.

This script rebuilds a v2-style JSONL by pairing the current v1 records
with verifier modules in data/verifiers/<domain>/<theorem_id>__<hyp_name>.py.
Optionally, it can ask Gemini to extract canonical witnesses in batches.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import random
import re
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logger = logging.getLogger(__name__)

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))


_WRITE_LOCK = threading.Lock()


@dataclass
class VerifierMeta:
    module_path: str
    condition_labels: list[str]
    n_conditions: int
    n_hyp: int
    neg_q_index: int
    setup_bindings: list[str]


def _safe_slug(text: str) -> str:
    return re.sub(r"[^\w\-]", "_", text or "")


def _module_path_for_record(record: dict, verifiers_dir: Path) -> Path:
    domain = _safe_slug(record.get("domain", "Unknown"))
    theorem_id = _safe_slug(record.get("theorem_id", "unknown"))
    hyp_name = _safe_slug(record.get("dropped_hypothesis_name", "h0"))
    filename = f"{theorem_id}__{hyp_name}.py"
    return verifiers_dir / domain / filename


def _parse_module_constants(source: str) -> tuple[list[str], int, int]:
    labels_match = re.search(
        r"CONDITION_LABELS\s*(?::\s*list\[str\])?\s*=\s*(\[.*?\])",
        source,
        re.DOTALL,
    )
    if not labels_match:
        raise ValueError("CONDITION_LABELS not found in verifier module")
    try:
        labels = eval(labels_match.group(1))  # only string literals expected
        if not isinstance(labels, list) or not all(isinstance(s, str) for s in labels):
            raise ValueError("CONDITION_LABELS must be a list of strings")
    except Exception as exc:
        raise ValueError(f"Failed to parse CONDITION_LABELS: {exc}") from exc

    nhyp_match = re.search(r"N_HYP\s*(?::\s*int)?\s*=\s*(\d+)", source)
    if not nhyp_match:
        raise ValueError("N_HYP not found in verifier module")
    n_hyp = int(nhyp_match.group(1))

    negq_match = re.search(r"NEG_Q_INDEX\s*(?::\s*int)?\s*=\s*(\d+)", source)
    if not negq_match:
        raise ValueError("NEG_Q_INDEX not found in verifier module")
    neg_q_index = int(negq_match.group(1))

    if neg_q_index != n_hyp:
        raise ValueError(
            f"NEG_Q_INDEX ({neg_q_index}) must equal N_HYP ({n_hyp})"
        )
    if len(labels) != n_hyp + 1:
        raise ValueError(
            f"CONDITION_LABELS length ({len(labels)}) must equal N_HYP+1 ({n_hyp + 1})"
        )

    return labels, n_hyp, neg_q_index


def _extract_setup_bindings(source: str, max_lines: int = 40) -> list[str]:
    bindings: list[str] = []
    for line in source.splitlines():
        if "CONDITION_LABELS" in line or line.strip().startswith("def conditions"):
            break
        if line.strip().startswith("import ") or line.strip().startswith("from "):
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*.+", line)
        if match:
            name = match.group(1)
            if name.isupper() or len(name) <= 4:
                bindings.append(line.strip())
        if len(bindings) >= max_lines:
            break
    return bindings


def _load_verifier_meta(module_path: Path) -> VerifierMeta:
    source = module_path.read_text(encoding="utf-8")
    labels, n_hyp, neg_q_index = _parse_module_constants(source)
    return VerifierMeta(
        module_path=str(module_path.resolve()),
        condition_labels=labels,
        n_conditions=len(labels),
        n_hyp=n_hyp,
        neg_q_index=neg_q_index,
        setup_bindings=_extract_setup_bindings(source),
    )


# ---------------------------------------------------------------------------
# Gemini client + witness extraction
# ---------------------------------------------------------------------------

_client_cache: dict[str, Any] = {}


def _get_client() -> Any:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set. "
            "Create a .env file from .env.example and fill in your key."
        )

    if api_key in _client_cache:
        return _client_cache[api_key]

    _client_cache[api_key] = genai.Client(api_key=api_key)
    return _client_cache[api_key]


def _extract_json_payload(raw: str) -> str:
    match = re.search(r"```(?:json)?\n(.*?)```", raw, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return raw.strip()


def _is_transient_error(exc: Exception) -> bool:
    exc_name = type(exc).__name__.lower()
    exc_str = str(exc).lower()
    return (
        "resourceexhausted" in exc_name
        or "internalservererror" in exc_name
        or "serviceunavailable" in exc_name
        or "timeout" in exc_name
        or "429" in exc_str
        or "500" in exc_str
        or "503" in exc_str
        or "quota" in exc_str
        or "deadline" in exc_str
    )


def _send_with_backoff(
    chat: Any,
    prompt: str,
    max_attempts: int,
    base_seconds: float,
    jitter: float,
) -> Any:
    last_exc: Exception | None = None
    for attempt in range(max_attempts):
        try:
            return chat.send_message(prompt)
        except Exception as exc:
            last_exc = exc
            if not _is_transient_error(exc) or attempt == max_attempts - 1:
                break
            delay = base_seconds * (2 ** attempt)
            noise = delay * jitter * (2 * random.random() - 1)
            wait = max(0.5, delay + noise)
            logger.warning(
                "Gemini transient error (attempt %d/%d): %s — retrying in %.1fs",
                attempt + 1,
                max_attempts,
                type(exc).__name__,
                wait,
            )
            time.sleep(wait)

    raise RuntimeError(f"Gemini API call failed after {max_attempts} attempts: {last_exc}")


def _load_fewshot_examples(path: Path, max_examples: int) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Few-shot file not found: {path}")
    examples: list[dict] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec.get("migration_failed"):
                continue
            if not rec.get("canonical_witness"):
                continue
            examples.append(rec)
            if len(examples) >= max_examples:
                break
    return examples


def _load_seen_pairs(path: Path) -> set[str]:
    seen: set[str] = set()
    if not path.exists():
        return seen

    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue

            theorem_id = rec.get("theorem_id")
            hyp_name = rec.get("dropped_hypothesis_name")
            if theorem_id and hyp_name:
                seen.add(f"{theorem_id}:{hyp_name}")

    return seen


def _format_fewshot_block(examples: list[dict]) -> str:
    if not examples:
        return ""
    lines = ["FEW-SHOT EXAMPLES:"]
    for ex in examples:
        lines.append("Input:")
        lines.append(f"- theorem_id: {ex.get('theorem_id')}")
        lines.append(f"- dropped_hypothesis_name: {ex.get('dropped_hypothesis_name')}")
        lines.append("- remaining_hypotheses:")
        for h in ex.get("remaining_hypotheses", []):
            lines.append(f"  - {h}")
        lines.append(f"- conclusion: {ex.get('conclusion', '')}")
        code = ex.get("counterexample_code", "")
        if code:
            snippet = code[:1200]
            lines.append("- counterexample_code_snippet:")
            lines.append(snippet)
        lines.append("Output:")
        lines.append(
            json.dumps(
                {
                    "theorem_id": ex.get("theorem_id"),
                    "dropped_hypothesis_name": ex.get("dropped_hypothesis_name"),
                    "canonical_witness": ex.get("canonical_witness"),
                }
            )
        )
        lines.append("")
    return "\n".join(lines).strip()


def _build_witness_prompt(
    record: dict,
    fewshot_block: str,
    max_code_chars: int,
    prior_error: str | None,
    prior_output: str | None,
) -> str:
    lines = [
        "You extract a canonical witness expression for a single item.",
        "Return a JSON object with:",
        "  - theorem_id",
        "  - dropped_hypothesis_name",
        "  - canonical_witness (string or null)",
        "If you cannot infer a witness, set canonical_witness to null.",
        "Output ONLY JSON, no prose.",
        "",
    ]
    if prior_error:
        lines.append("Previous attempt failed with error:")
        lines.append(prior_error)
        lines.append("")
    if prior_output:
        lines.append("Previous output (for reference):")
        lines.append(prior_output[:600])
        lines.append("")
    if fewshot_block:
        lines.append(fewshot_block)
        lines.append("")

    lines.append("ITEM:")
    lines.append(f"theorem_id: {record.get('theorem_id')}")
    lines.append(f"dropped_hypothesis_name: {record.get('dropped_hypothesis_name')}")
    lines.append(f"domain: {record.get('domain', '')}")
    lines.append("remaining_hypotheses:")
    for h in record.get("remaining_hypotheses", []):
        lines.append(f"  - {h}")
    lines.append(f"conclusion: {record.get('conclusion', '')}")
    bindings = record.get("_setup_bindings", [])
    if bindings:
        lines.append("setup_bindings:")
        for b in bindings[:20]:
            lines.append(f"  - {b}")
    code = record.get("counterexample_code", "") or ""
    if code:
        lines.append("counterexample_code_snippet:")
        lines.append(code[:max_code_chars])

    return "\n".join(lines)


def _generate_witness_for_record(
    record: dict,
    model: str,
    temperature: float,
    fewshot_block: str,
    max_code_chars: int,
    validate_witness: bool,
    sandbox_timeout: float,
    witness_retries: int,
    transient_retries: int,
    retry_base_seconds: float,
    retry_jitter: float,
) -> tuple[str | None, bool, int]:
    client = _get_client()
    from src.oracle.sandbox import run_oracle

    attempts = 0
    last_error: str | None = None
    last_output: str | None = None

    for _ in range(witness_retries + 1):
        attempts += 1
        chat = client.chats.create(
            model=model,
            config=types.GenerateContentConfig(
                system_instruction="Return only JSON per the user instructions.",
                temperature=temperature,
                max_output_tokens=2048,
                candidate_count=1,
            ),
        )

        prompt = _build_witness_prompt(
            record=record,
            fewshot_block=fewshot_block,
            max_code_chars=max_code_chars,
            prior_error=last_error,
            prior_output=last_output,
        )

        try:
            resp = _send_with_backoff(
                chat,
                prompt,
                max_attempts=transient_retries,
                base_seconds=retry_base_seconds,
                jitter=retry_jitter,
            )
            print(resp.text)  # for debugging
        except Exception as exc:
            last_error = f"TransientError: {exc}"
            continue

        raw_text = resp.text or ""
        last_output = raw_text.strip()
        payload = _extract_json_payload(raw_text)

        try:
            data = json.loads(payload)
        except json.JSONDecodeError as exc:
            last_error = f"JSONParseError: {exc}"
            continue

        if not isinstance(data, dict):
            last_error = "Response is not a JSON object"
            continue

        witness = data.get("canonical_witness")
        if witness is not None:
            witness = str(witness).strip()
            if witness == "":
                witness = None

        if validate_witness and witness:
            oracle = run_oracle(
                verifier_module_path=record["verifier"]["module_path"],
                witness_expr=witness,
                n_conditions=record["verifier"]["n_conditions"],
                timeout_seconds=sandbox_timeout,
            )
            if oracle.parse_ok and oracle.conditions and all(oracle.conditions):
                return witness, True, attempts

            if oracle.conditions:
                labels = record["verifier"].get("condition_labels", [])
                failed = [labels[i] for i, ok in enumerate(oracle.conditions) if not ok]
                last_error = f"OracleFailed: failed conditions: {failed}"
            else:
                last_error = f"OracleFailed: {oracle.error or 'no conditions'}"
            continue

        return witness, False, attempts

    logger.warning(
        "Witness extraction failed for %s:%s after %d attempts: %s",
        record.get("theorem_id"),
        record.get("dropped_hypothesis_name"),
        attempts,
        last_error,
    )
    return None, False, attempts


# ---------------------------------------------------------------------------
# Reconstruction
# ---------------------------------------------------------------------------


def _append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _WRITE_LOCK:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def _failure_record(record: dict, migration_error: str) -> dict:
    failed = dict(record)
    failed["verifier"] = None
    failed["canonical_witness"] = None
    failed["witness_passes_verifier"] = False
    failed["verifier_generation_attempts"] = 0
    failed["migration_failed"] = True
    failed["migration_error"] = migration_error
    return failed


def reconstruct(
    input_path: Path,
    output_path: Path,
    failures_path: Path,
    verifiers_dir: Path,
    witness_mode: str,
    witness_model: str,
    witness_temperature: float,
    batch_size: int,
    fewshot_path: Path | None,
    fewshot_count: int,
    max_code_chars: int,
    validate_witness: bool,
    sandbox_timeout: float,
    max_records: int,
    witness_retries: int,
    transient_retries: int,
    retry_base_seconds: float,
    retry_jitter: float,
) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Input JSONL not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    failures_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.touch(exist_ok=True)
    failures_path.touch(exist_ok=True)

    seen_pairs = _load_seen_pairs(output_path)
    seen_pairs.update(_load_seen_pairs(failures_path))

    records: list[dict] = []
    with open(input_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
            if max_records > 0 and len(records) >= max_records:
                break

    logger.info("Loaded %d records from %s", len(records), input_path)

    pending: list[dict] = []
    for rec in records:
        pair_key = f"{rec.get('theorem_id')}:{rec.get('dropped_hypothesis_name')}"
        if pair_key in seen_pairs:
            logger.info(
                "Skipping already processed record %s:%s",
                rec.get("theorem_id"),
                rec.get("dropped_hypothesis_name"),
            )
            continue

        module_path = _module_path_for_record(rec, verifiers_dir)
        try:
            if not module_path.exists():
                raise FileNotFoundError(f"Verifier module not found: {module_path}")
            meta = _load_verifier_meta(module_path)
        except Exception as exc:
            failed = _failure_record(rec, str(exc))
            failed["original_theorem_validated"] = rec.get("original_theorem_validated")
            _append_jsonl(failures_path, failed)
            seen_pairs.add(pair_key)
            continue

        out = dict(rec)
        out["verifier"] = {
            "module_path": meta.module_path,
            "condition_labels": meta.condition_labels,
            "n_conditions": meta.n_conditions,
            "n_hyp": meta.n_hyp,
            "neg_q_index": meta.neg_q_index,
        }
        out["canonical_witness"] = None
        out["witness_passes_verifier"] = False
        out["verifier_generation_attempts"] = 0
        out["migration_failed"] = False
        out["original_theorem_validated"] = rec.get("original_theorem_validated")
        out["_setup_bindings"] = meta.setup_bindings
        pending.append(out)

    logger.info("Records with verifiers found: %d", len(pending))

    if witness_mode == "gemini" and pending:
        fewshot_block = ""
        if fewshot_path is not None:
            examples = _load_fewshot_examples(fewshot_path, fewshot_count)
            fewshot_block = _format_fewshot_block(examples)
        if batch_size != 1:
            logger.warning("Batch size > 1 is deprecated and ignored; processing records individually.")

        worker_count = max(1, batch_size)
        logger.info("Witness generation workers: %d", worker_count)

        def _process_record(rec: dict) -> dict:
            witness, passes, attempts = _generate_witness_for_record(
                record=rec,
                model=witness_model,
                temperature=witness_temperature,
                fewshot_block=fewshot_block,
                max_code_chars=max_code_chars,
                validate_witness=validate_witness,
                sandbox_timeout=sandbox_timeout,
                witness_retries=witness_retries,
                transient_retries=transient_retries,
                retry_base_seconds=retry_base_seconds,
                retry_jitter=retry_jitter,
            )
            rec["canonical_witness"] = witness
            rec["witness_passes_verifier"] = passes
            rec["verifier_generation_attempts"] = attempts
            return rec

        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            futures = {executor.submit(_process_record, rec): rec for rec in pending}
            for fut in as_completed(futures):
                rec = fut.result()
                rec.pop("_setup_bindings", None)
                _append_jsonl(output_path, rec)
    else:
        for rec in pending:
            rec.pop("_setup_bindings", None)
            _append_jsonl(output_path, rec)

    logger.info("Reconstruction complete.")
    logger.info("Output JSONL: %s", output_path)
    logger.info("Failures JSONL: %s", failures_path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reconstruct v2 JSONL from existing verifier modules."
    )
    parser.add_argument(
        "--input",
        default="data/algebra_counterexamples.jsonl",
        help="Source v1 JSONL (default: data/algebra_counterexamples.jsonl)",
    )
    parser.add_argument(
        "--output",
        default="data/algebra_counterexamples_v2_reconstructed.jsonl",
        help="Output v2 JSONL (default: data/algebra_counterexamples_v2_reconstructed.jsonl)",
    )
    parser.add_argument(
        "--output-failures",
        default=None,
        help="Failures JSONL (default: <output>_failures.jsonl)",
    )
    parser.add_argument(
        "--verifiers-dir",
        default="data/verifiers",
        help="Verifier modules root directory (default: data/verifiers)",
    )
    parser.add_argument(
        "--max-records",
        type=int,
        default=0,
        help="Process at most N records (0 = unlimited)",
    )
    parser.add_argument(
        "--witness-mode",
        choices=["none", "gemini"],
        default="none",
        help="Witness mode: none (set nulls) or gemini (extract with LLM)",
    )
    parser.add_argument(
        "--witness-model",
        default="gemini-3-flash-preview",
        help="Gemini model for witness extraction",
    )
    parser.add_argument(
        "--witness-temperature",
        type=float,
        default=0.2,
        help="Temperature for witness extraction",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of parallel Gemini workers (default: 1)",
    )
    parser.add_argument(
        "--batch-size",
        dest="workers",
        type=int,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--fewshot-path",
        default=None,
        help="JSONL file with canonical witnesses for few-shot prompting",
    )
    parser.add_argument(
        "--fewshot-count",
        type=int,
        default=5,
        help="Number of few-shot examples to include",
    )
    parser.add_argument(
        "--max-code-chars",
        type=int,
        default=1800,
        help="Max counterexample code chars per item",
    )
    parser.add_argument(
        "--witness-retries",
        type=int,
        default=2,
        help="Number of logical retries for witness extraction (default: 2)",
    )
    parser.add_argument(
        "--transient-retries",
        type=int,
        default=3,
        help="Number of transient API retries with backoff (default: 3)",
    )
    parser.add_argument(
        "--retry-base-seconds",
        type=float,
        default=2.0,
        help="Base delay for exponential backoff (default: 2.0)",
    )
    parser.add_argument(
        "--retry-jitter",
        type=float,
        default=0.25,
        help="Jitter fraction for backoff delays (default: 0.25)",
    )
    parser.add_argument(
        "--validate-witness",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Validate witness via oracle sandbox (default: False)",
    )
    parser.add_argument(
        "--sandbox-timeout",
        type=float,
        default=8.0,
        help="Oracle timeout seconds (default: 8.0)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    input_path = _PROJECT_ROOT / args.input
    output_path = _PROJECT_ROOT / args.output
    if args.output_failures:
        failures_path = _PROJECT_ROOT / args.output_failures
    else:
        base = output_path.name
        if base.endswith(".jsonl"):
            base = base.replace(".jsonl", "_failures.jsonl")
        else:
            base = base + "_failures.jsonl"
        failures_path = output_path.parent / base

    verifiers_dir = _PROJECT_ROOT / args.verifiers_dir
    fewshot_path = Path(args.fewshot_path).resolve() if args.fewshot_path else None

    reconstruct(
        input_path=input_path,
        output_path=output_path,
        failures_path=failures_path,
        verifiers_dir=verifiers_dir,
        witness_mode=args.witness_mode,
        witness_model=args.witness_model,
        witness_temperature=args.witness_temperature,
        batch_size=args.workers,
        fewshot_path=fewshot_path,
        fewshot_count=args.fewshot_count,
        max_code_chars=args.max_code_chars,
        validate_witness=args.validate_witness,
        sandbox_timeout=args.sandbox_timeout,
        max_records=args.max_records,
        witness_retries=args.witness_retries,
        transient_retries=args.transient_retries,
        retry_base_seconds=args.retry_base_seconds,
        retry_jitter=args.retry_jitter,
    )


if __name__ == "__main__":
    main()
