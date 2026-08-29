"""
Sandbox execution verifier for LLM-generated counterexample scripts.

Writes the code to a temporary file, runs it in a subprocess with a strict
timeout, and returns a structured result dict.

Key design choices:
  - check_negation_form() is a mandatory static check that guards against
    the "Learning to Disprove" logical specification bug: scripts that assert
    Q(x) is True instead of asserting Q(x) is False.
  - A successful verification (success=True) means exit code 0, which in
    turn means all assert statements passed — including `assert not Q(x)`.
"""

import os
import re
import ast
import subprocess
import tempfile
import logging

logger = logging.getLogger(__name__)

TIMEOUT_SECONDS: float = 5.0

# Fallback patterns used when AST parsing fails.
_NEGATION_PATTERNS: list[str] = [
    r"assert\s+not\b",             # assert not <expr>
    r"assert\s+.*!=.*",             # assert lhs != rhs
    r"assert\s+.*==\s*False\b",   # assert expr == False
    r"assert\s+False\s*==.*",      # assert False == expr
    r"assert\s+.*\sis\sFalse\b", # assert expr is False
]

# Modules that must not appear in generated code.
_DANGEROUS_MODULES: tuple[str, ...] = (
    "os", "sys", "subprocess", "shutil", "socket",
    "urllib", "http", "requests", "ftplib", "smtplib",
)

# Builtins whose presence suggests code injection or unsafe file access.
_DANGEROUS_BUILTINS: tuple[str, ...] = (
    "__import__",
    "eval(",
    "exec(",
    "open(",
    "compile(",
)


def check_negation_form(code: str) -> bool:
    """
    Unit test for the critical logical constraint.

    Returns True if the code contains at least one pattern that asserts the
    *negation* of the conclusion (e.g. `assert not Q(x)` or `assert a != b`).

    A False result is a red flag — the code may be asserting Q(x) is True
    (existential satisfiability) rather than False (disproof).

    This is a conservative heuristic; execution is the authoritative check.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        # Syntax-invalid code may still contain useful signals for correction loops.
        for pattern in _NEGATION_PATTERNS:
            if re.search(pattern, code, flags=re.IGNORECASE | re.MULTILINE):
                return True
        return False

    def _is_false_constant(node: ast.AST) -> bool:
        return isinstance(node, ast.Constant) and node.value is False

    for node in ast.walk(tree):
        if not isinstance(node, ast.Assert):
            continue

        test = node.test

        # assert not <expr>
        if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
            return True

        # assert <lhs> != <rhs>
        if isinstance(test, ast.Compare) and any(
            isinstance(op, ast.NotEq) for op in test.ops
        ):
            return True

        # assert <expr> == False / assert False == <expr>
        # assert <expr> is False / assert False is <expr>
        if isinstance(test, ast.Compare):
            nodes = [test.left, *test.comparators]
            has_false = any(_is_false_constant(n) for n in nodes)
            has_eq_like = any(isinstance(op, (ast.Eq, ast.Is)) for op in test.ops)
            if has_false and has_eq_like:
                return True

    return False


def check_safety(code: str) -> tuple[bool, str]:
    """
    Lightweight static safety check.

    Returns (is_safe: bool, reason: str). An empty reason string means safe.
    """
    for mod in _DANGEROUS_MODULES:
        if re.search(rf"\bimport\s+{re.escape(mod)}\b", code):
            return False, f"Dangerous module import detected: '{mod}'"
        if re.search(rf"\bfrom\s+{re.escape(mod)}\s+import\b", code):
            return False, f"Dangerous module import detected: 'from {mod} import'"
    for builtin in _DANGEROUS_BUILTINS:
        if builtin in code:
            return False, f"Dangerous builtin detected: '{builtin}'"
    return True, ""


def execute_and_verify(python_code: str) -> dict:
    """
    Execute a counterexample script in a subprocess sandbox.

    Args:
        python_code: Python source code produced by the LLM generator.

    Returns:
        {
            "success": bool,           # True iff script exits with code 0
            "exit_code": int,          # subprocess return code (-1 = timeout)
            "stdout": str,             # captured standard output
            "stderr": str,             # captured standard error
            "timed_out": bool,
            "syntax_error": bool,
            "runtime_error": bool,
            "negation_form_ok": bool,  # passed check_negation_form()
            "safety_ok": bool,         # passed check_safety()
            "error_message": str,      # human-readable summary of failure
        }
    """
    result: dict = {
        "success": False,
        "exit_code": -1,
        "stdout": "",
        "stderr": "",
        "timed_out": False,
        "syntax_error": False,
        "runtime_error": False,
        "negation_form_ok": False,
        "safety_ok": True,
        "error_message": "",
    }

    # --- Static checks (before touching disk) ---

    result["negation_form_ok"] = check_negation_form(python_code)
    if not result["negation_form_ok"]:
        logger.warning(
            "Negation form check FAILED — code may assert Q(x) is True "
            "instead of False. Proceeding to execution but flagging the issue."
        )
        result["error_message"] = (
            "Negation-form check failed: no 'assert not ...', 'assert ... != ...', "
            "or 'assert ... == False' pattern found. This strongly suggests the "
            "code asserts the conclusion is True (wrong) instead of False (correct)."
        )

    is_safe, safety_reason = check_safety(python_code)
    result["safety_ok"] = is_safe
    if not is_safe:
        result["error_message"] = f"Safety check failed: {safety_reason}"
        logger.error(f"Safety check blocked execution: {safety_reason}")
        return result

    # --- Write to temp file and execute ---

    tmp_path: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            prefix="ce_verify_",
            delete=False,
            encoding="utf-8",
        ) as tmp:
            tmp.write(python_code)
            tmp_path = tmp.name

        proc = subprocess.run(
            ["python3", tmp_path],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )

        result["exit_code"] = proc.returncode
        result["stdout"] = proc.stdout.strip()
        result["stderr"] = proc.stderr.strip()
        result["success"] = proc.returncode == 0

        if not result["success"]:
            stderr = proc.stderr
            if "SyntaxError" in stderr:
                result["syntax_error"] = True
                result["error_message"] = "SyntaxError in generated code"
            elif "AssertionError" in stderr:
                result["runtime_error"] = True
                result["error_message"] = (
                    "AssertionError: a hypothesis or negated-conclusion check failed"
                )
            elif "ModuleNotFoundError" in stderr or "ImportError" in stderr:
                result["error_message"] = (
                    "ImportError: a required library is not installed "
                    "(check that z3-solver and sympy are in the environment)"
                )
            else:
                result["runtime_error"] = True
                result["error_message"] = (
                    f"Runtime error (exit code {proc.returncode}): "
                    + (stderr[:200] if stderr else "(no stderr)")
                )

    except subprocess.TimeoutExpired:
        result["timed_out"] = True
        result["error_message"] = (
            f"Execution timed out after {TIMEOUT_SECONDS}s — "
            "the search loop may be too slow; try a smaller search space."
        )
        logger.warning(f"Script timed out after {TIMEOUT_SECONDS}s")

    except Exception as exc:
        result["error_message"] = f"Unexpected error during subprocess execution: {exc}"
        logger.exception("Unexpected error in execute_and_verify")

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)

    return result
