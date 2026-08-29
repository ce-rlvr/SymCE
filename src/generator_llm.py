"""
LLM-based counterexample code generator using the Gemini API.

Configuration via environment variables (or a .env file):
    GEMINI_API_KEY   — Google Generative AI API key (required)
    GEMINI_MODEL     — model name (default: gemini-2.0-flash)
"""

import os
import re
import time
import math
import random
import threading
import logging
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Retry helper — wraps chat.send_message with exponential backoff.
# Retries on transient API errors: rate limits (429), server errors (500/503),
# and network timeouts. Hard-stops on auth errors and client 4xx.
# ---------------------------------------------------------------------------

_RETRY_ATTEMPTS = 3
_RETRY_BASE_SECONDS = 2.0
_RETRY_JITTER = 0.25


def _send_with_retry(chat: Any, prompt: str) -> Any:
    """Send a chat message with up to _RETRY_ATTEMPTS retries on transient errors."""
    last_exc: Exception | None = None
    for attempt in range(_RETRY_ATTEMPTS):
        try:
            return chat.send_message(prompt)
        except Exception as exc:
            exc_name = type(exc).__name__
            exc_str = str(exc).lower()

            # Decide whether to retry based on error type / message.
            retryable = (
                "resourceexhausted" in exc_name.lower()   # 429 quota
                or "internalservererror" in exc_name.lower()  # 500
                or "serviceunavailable" in exc_name.lower()   # 503
                or "timeout" in exc_name.lower()
                or "429" in exc_str
                or "500" in exc_str
                or "503" in exc_str
                or "quota" in exc_str
                or "deadline" in exc_str
            )

            if not retryable or attempt == _RETRY_ATTEMPTS - 1:
                last_exc = exc
                break

            delay = _RETRY_BASE_SECONDS * (2 ** attempt)
            jitter = delay * _RETRY_JITTER * (2 * random.random() - 1)
            wait = max(0.5, delay + jitter)
            logger.warning(
                "Gemini API transient error (attempt %d/%d): %s — retrying in %.1fs",
                attempt + 1, _RETRY_ATTEMPTS, exc_name, wait,
            )
            time.sleep(wait)

    raise RuntimeError(f"Gemini API call failed after {_RETRY_ATTEMPTS} attempts: {last_exc}") from last_exc

# ---------------------------------------------------------------------------
# Thread-safe model cache
# ---------------------------------------------------------------------------

_model_lock = threading.Lock()
_client_cache: dict[str, Any] = {}


def _get_client() -> Any:
    """Return a cached Gen AI client, creating it on first call (thread-safe)."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set. "
            "Create a .env file from .env.example and fill in your key."
        )

    if api_key in _client_cache:
        return _client_cache[api_key]

    with _model_lock:
        if api_key not in _client_cache:
            _client_cache[api_key] = genai.Client(api_key=api_key)
    return _client_cache[api_key]

# ---------------------------------------------------------------------------
# System prompt
#
# This is the fixed instruction that primes every Gemini call. It explains
# the logical structure of the task, the critical mistake to avoid, and
# the exact assert pattern required by the verifier.
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a mathematical expert and Python programmer specializing in abstract algebra.

## Your Role

You generate Python scripts that find and verify counterexamples to FALSE algebraic
conjectures. The conjectures are obtained by dropping one hypothesis from a true theorem.

## STEP 0 — WELL-POSEDNESS CHECK (MANDATORY)

Before attempting any counterexample, determine if the statement is mathematically well-defined.

Check:
- Are all symbols defined?
- Does dropping hypotheses make any expression undefined or ambiguous?
- Are any remaining hypotheses actually definitions rather than assumptions?

If NOT well-posed, stop immediately.

Return EXACTLY ONE of the following (based on your analysis):

### CASE 1 — COUNTEREXAMPLE EXISTS
[Normal output as Python code]

### CASE 2 — STATEMENT IS TRUE OR UNDISPROVABLE
If the dropped hypothesis wasn't actually required, and the remaining hypotheses still prove the conclusion, return EXACTLY:
[STATEMENT_IS_TRUE]

### CASE 3 — ILL-DEFINED / NOT WELL-POSED
If the statement is completely broken, ambiguous, or lacks context, return EXACTLY:
[ILL_DEFINED]

- Never assume reinterpretation of symbols.
- Never silently redefine notation.
- Never search for counterexamples if well-posedness fails.
- If unsure, prefer "ill-defined" over "theorem is true", and "counterexample exists" over "theorem is true".

## The Logical Structure (For Case 1)

Given a true theorem:  ∀x. (H₁(x) ∧ H₂(x)) → Q(x)
After dropping H₂, the FALSE conjecture is: ∀x. H₁(x) → Q(x)

Your task: find a witness x such that:
  • H₁(x) = True   ← remaining hypothesis HOLDS at x
  • Q(x)  = False  ← conclusion FAILS at x  (this is ¬Q(x), the disproof)

This is the negation of the universal: ∃x. H₁(x) ∧ ¬Q(x)

## CRITICAL WARNING — The #1 Mistake to Avoid

DO NOT find x such that H₁(x) = True AND Q(x) = True.
That demonstrates the conjecture is *satisfiable*, not that it is *false*.
You MUST negate the conclusion.

Required assert pattern:
  assert <remaining_hypothesis_check>   # this evaluates to True
  assert not <conclusion_check>          # conclusion evaluates to False at x

## Allowed Libraries

Import ONLY from: sympy, sympy.combinatorics, sympy.matrices, sympy.ntheory,
                  z3, math, itertools, functools, random, numpy, scipy

Do NOT import: os, sys, subprocess, socket, requests, urllib, open, eval, exec

## Code Requirements

1. Find a concrete counterexample (specific mathematical objects, not symbolic variables)
2. Verify all remaining hypotheses hold with explicit `assert` statements
3. Assert the conclusion is FALSE using `assert not <check>` or `assert <lhs> != <rhs>`
4. Print the counterexample clearly so a human can inspect it
5. Code must complete in under 5 seconds
6. Code must be self-contained — no file I/O, no network access

## Output Contract Required By Verifier

Your script MUST include at least one explicit negation-style assert for the
conclusion check, such as:
    - assert not conclusion_holds
    - assert lhs != rhs
    - assert conclusion_holds == False
    - assert conclusion_holds is False

Never use only `assert conclusion_holds` for the target conclusion; that proves
the opposite of what we need.

## Illustrative Example

Conjecture: "For all a, b in any group G: (a*b)² = a²*b²"
(Dropped hypothesis: G is abelian)
Task: find a, b in a non-abelian group where (a*b)² ≠ a²*b²

```python
from sympy.combinatorics import Permutation, PermutationGroup

# S3 — the smallest non-abelian group
r = Permutation([1, 2, 0])   # rotation (0 1 2)
s = Permutation([1, 0, 2])   # reflection (0 1)
G = PermutationGroup(r, s)

a, b = r, s

# Remaining hypothesis: G is a group (always true for PermutationGroup)
assert G.order() > 0, "G must be a non-trivial group"

# Conclusion must FAIL: (a*b)^2 != a^2 * b^2
ab_sq = (a * b) ** 2
a2b2 = a**2 * b**2
assert ab_sq != a2b2, (
    f"Logic error: equality holds — not a counterexample. "
    f"(a*b)^2 = {ab_sq}, a^2*b^2 = {a2b2}"
)

print("Counterexample found!")
print(f"Group: S3 (order {G.order()})")
print(f"a = {a}, b = {b}")
print(f"(a*b)^2 = {ab_sq}")
print(f"a^2 * b^2 = {a2b2}")
```

## Output

If Case 2 or 3, output JUST the exact tag requested.
If Case 1, output ONLY Python code. Begin directly with import statements. No prose, no markdown.
"""


def _extract_code(raw_text: str) -> str:
    """Strip markdown code fences if the LLM wrapped the response in them."""
    if "[ILL_DEFINED]" in raw_text:
        return "[ILL_DEFINED]"
    if "[STATEMENT_IS_TRUE]" in raw_text:
        return "[STATEMENT_IS_TRUE]"

    match = re.search(r"```(?:python)?\s*\n(.*?)```", raw_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return raw_text.strip()


# ---------------------------------------------------------------------------
# Session-based API (multi-turn self-correction)
# ---------------------------------------------------------------------------

def start_generation_session(user_prompt: str) -> tuple[Any, str]:
    """
    Start a Gemini chat session and return the first code attempt.

    Each theorem gets its own session so that correction turns carry context
    about the specific task and previous errors.

    Returns:
        (chat_session, python_code) — the session object to pass to
        correct_from_session() on failure, and the extracted code string.

    Raises:
        RuntimeError: on API or config errors.
    """
    client = _get_client()
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    logger.info(f"Starting Gemini session ({model_name})...")

    chat = client.chats.create(
        model=model_name,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.6,
            max_output_tokens=16384,
            candidate_count=1,
        ),
    )
    try:
        response = _send_with_retry(chat, user_prompt)
    except RuntimeError:
        raise

    code = _extract_code(response.text)
    logger.debug(f"Session started — {len(code)} chars generated/extracted")
    return chat, code


def correct_from_session(chat: Any, failed_code: str, error_message: str) -> str:
    """
    Send a self-correction prompt to an existing chat session.

    The session already has context about the theorem and the previous attempt,
    so we only need to report what went wrong. The LLM revises its own output.

    Args:
        chat: The chat session returned by start_generation_session().
        failed_code: The Python code that failed verification.
        error_message: The verifier's error string (stderr or error_message).

    Returns:
        Revised Python code as a string.

    Raises:
        RuntimeError: on API errors.
    """
    snippet = error_message[:600] if error_message else "(no error details)"
    code_snippet = failed_code[:1200] if failed_code else ""
    negation_failure = "Negation-form check failed" in (error_message or "")

    negation_fix_block = ""
    if negation_failure:
        negation_fix_block = (
            "IMPORTANT: The previous script violated the logical contract.\n"
            "You MUST explicitly assert the conclusion is false.\n"
            "Include at least one of these literal forms:\n"
            "  - assert not <expr>\n"
            "  - assert <lhs> != <rhs>\n"
            "  - assert <expr> == False\n"
            "  - assert <expr> is False\n"
            "Do not return code that only asserts the conclusion is true.\n\n"
        )

    correction_prompt = (
        "Your code failed verification with the following error:\n\n"
        f"```\n{snippet}\n```\n\n"
        "The failing code was:\n\n"
        f"```python\n{code_snippet}\n```\n\n"
        f"{negation_fix_block}"
        "Please diagnose the error and generate a fully corrected Python script.\n"
        "Reminders:\n"
        "  - All remaining hypotheses must hold — verify each with an `assert`\n"
        "  - The conclusion must be FALSE — use `assert not <check>` or `assert lhs != rhs`\n"
        "  - Check SymPy API usage carefully (e.g. use `.order()` on Permutation objects)\n"
        "If you realize the statement is actually ill-defined or true, you can return [ILL_DEFINED] or [STATEMENT_IS_TRUE]. Otherwise, output ONLY valid Python code. No prose, no markdown."
    )

    try:
        response = _send_with_retry(chat, correction_prompt)
    except RuntimeError:
        raise

    code = _extract_code(response.text)
    logger.debug(f"Correction received — {len(code)} chars")
    return code


# ---------------------------------------------------------------------------
# Convenience single-shot wrapper (kept for backward compatibility / dry-run)
# ---------------------------------------------------------------------------

def generate_counterexample_code(user_prompt: str) -> str:
    """Single-shot generation without a persistent session."""
    _, code = start_generation_session(user_prompt)
    return code
