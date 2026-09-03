"""
Subprocess-based oracle executor for the v2.0 independent-verifier pipeline.

Given a verifier module path and a witness expression string, this module:
1. Static-checks the verifier source for dangerous patterns.
2. Writes a tiny driver script to a temp file.
3. Runs it in a subprocess with a hard timeout.
4. Parses the JSON result and returns an OracleResult dataclass.

The verifier module is expected to define:
    def conditions(witness) -> list[bool]
    CONDITION_LABELS: list[str]
    N_HYP: int
    NEG_Q_INDEX: int

and whatever top-level setup is needed (imports, named objects).
"""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_SECONDS: float = 8.0

# Reuse the same safety constants as src/verifier.py
_DANGEROUS_MODULES: tuple[str, ...] = (
    "os", "sys", "subprocess", "shutil", "socket",
    "urllib", "http", "requests", "ftplib", "smtplib",
)

_DANGEROUS_BUILTINS: tuple[str, ...] = (
    "__import__",
    "eval(",
    "exec(",
    "open(",
    "compile(",
)


@dataclass
class OracleResult:
    parse_ok: bool
    conditions: Optional[list[bool]]
    error: Optional[str]
    timed_out: bool
    elapsed_ms: int
    module_load_ok: bool = True  # False if the verifier module itself failed to import


def _check_safety(source: str) -> tuple[bool, str]:
    """Lightweight static safety check on verifier source. Returns (is_safe, reason)."""
    for mod in _DANGEROUS_MODULES:
        if re.search(rf"\bimport\s+{re.escape(mod)}\b", source):
            return False, f"Dangerous module import detected: '{mod}'"
        if re.search(rf"\bfrom\s+{re.escape(mod)}\s+import\b", source):
            return False, f"Dangerous module import detected: 'from {mod} import'"
    for builtin in _DANGEROUS_BUILTINS:
        if builtin in source:
            return False, f"Dangerous builtin detected: '{builtin}'"
    return True, ""


# ---------------------------------------------------------------------------
# Driver script template - written to a tempfile and executed in subprocess.
# ---------------------------------------------------------------------------

_DRIVER_TEMPLATE = """\
import sys
import json
import importlib.util

_module_path = {module_path!r}
_witness_expr = {witness_expr!r}

_result = {{"parse_ok": False, "conditions": None, "error": None,
            "timed_out": False, "module_load_ok": True}}

try:
    _spec = importlib.util.spec_from_file_location("_verifier_mod", _module_path)
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
except Exception as _e:
    _result["error"] = f"ModuleLoadError: {{type(_e).__name__}}: {{str(_e)[:200]}}"
    _result["module_load_ok"] = False
    print(json.dumps(_result))
    sys.exit(0)

_ns = {{k: getattr(_mod, k) for k in dir(_mod) if not k.startswith("_")}}

try:
    _witness = eval(_witness_expr, _ns)
    _result["parse_ok"] = True
except Exception as _e:
    _result["error"] = f"WitnessEvalError: {{type(_e).__name__}}: {{str(_e)[:200]}}"
    print(json.dumps(_result))
    sys.exit(0)

try:
    _conds = _mod.conditions(_witness)
    _result["conditions"] = [bool(_c) for _c in _conds]
except Exception as _e:
    _result["error"] = f"ConditionsError: {{type(_e).__name__}}: {{str(_e)[:200]}}"

print(json.dumps(_result))
sys.exit(0)
"""


def run_oracle(
    verifier_module_path: str,
    witness_expr: str,
    n_conditions: int,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
) -> OracleResult:
    """
    Execute the verifier for a single witness expression.

    Args:
        verifier_module_path: Absolute or repo-relative path to the .py verifier module.
        witness_expr: A Python expression string evaluable in the module's namespace.
        n_conditions: Expected number of conditions (used for validation only).
        timeout_seconds: Hard subprocess timeout.

    Returns:
        OracleResult with parse_ok, conditions list, any error message, timing.
    """
    t_start = time.monotonic()

    module_path = str(Path(verifier_module_path).resolve())

    # --- Static safety check on the verifier source ---
    try:
        source = Path(module_path).read_text(encoding="utf-8")
    except OSError as exc:
        elapsed = int((time.monotonic() - t_start) * 1000)
        return OracleResult(
            parse_ok=False,
            conditions=None,
            error=f"VerifierFileError: {exc}",
            timed_out=False,
            elapsed_ms=elapsed,
            module_load_ok=False,
        )

    is_safe, reason = _check_safety(source)
    if not is_safe:
        elapsed = int((time.monotonic() - t_start) * 1000)
        return OracleResult(
            parse_ok=False,
            conditions=None,
            error=f"SafetyCheckFailed: {reason}",
            timed_out=False,
            elapsed_ms=elapsed,
            module_load_ok=False,
        )

    driver = _DRIVER_TEMPLATE.format(
        module_path=module_path,
        witness_expr=witness_expr,
    )

    tmp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            prefix="oracle_driver_",
            delete=False,
            encoding="utf-8",
        ) as tmp:
            tmp.write(driver)
            tmp_path = tmp.name

        proc = subprocess.run(
            ["python3", tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )

        elapsed = int((time.monotonic() - t_start) * 1000)

        stdout = proc.stdout.strip()
        if not stdout:
            stderr_snippet = proc.stderr.strip()[:300] if proc.stderr else "(no output)"
            return OracleResult(
                parse_ok=False,
                conditions=None,
                error=f"EmptyOutput: {stderr_snippet}",
                timed_out=False,
                elapsed_ms=elapsed,
            )

        try:
            data = json.loads(stdout)
        except json.JSONDecodeError:
            return OracleResult(
                parse_ok=False,
                conditions=None,
                error=f"JSONDecodeError: could not parse driver output: {stdout[:200]}",
                timed_out=False,
                elapsed_ms=elapsed,
            )

        conds_raw = data.get("conditions")
        conds: Optional[list[bool]] = [bool(c) for c in conds_raw] if conds_raw is not None else None

        return OracleResult(
            parse_ok=bool(data.get("parse_ok", False)),
            conditions=conds,
            error=data.get("error"),
            timed_out=bool(data.get("timed_out", False)),
            elapsed_ms=elapsed,
            module_load_ok=bool(data.get("module_load_ok", True)),
        )

    except subprocess.TimeoutExpired:
        elapsed = int((time.monotonic() - t_start) * 1000)
        logger.warning("Oracle subprocess timed out after %.1fs", timeout_seconds)
        return OracleResult(
            parse_ok=False,
            conditions=None,
            error=f"TimeoutExpired after {timeout_seconds}s",
            timed_out=True,
            elapsed_ms=elapsed,
        )

    except Exception as exc:
        elapsed = int((time.monotonic() - t_start) * 1000)
        logger.exception("Unexpected error in run_oracle")
        return OracleResult(
            parse_ok=False,
            conditions=None,
            error=f"UnexpectedError: {type(exc).__name__}: {exc}",
            timed_out=False,
            elapsed_ms=elapsed,
        )

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
