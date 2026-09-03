"""
Canonical prompt strings shared across the v2.0 training stack.

Single source of truth so the splitter (``tools/build_splits.py``), the SFT
and RLVR data loaders, the reward computation harness, and any future eval
code all reference identical text. Avoids prompt drift between
training-time and eval-time generation.
"""

from __future__ import annotations


def _format_witness_schema_hint(record: dict) -> str:
    schema = (record.get("witness_schema") or "").strip()
    if not schema:
        return ""
    return (
        "Witness schema hint: "
        f"{schema}\n"
        "Use this structural hint when constructing the [COUNTEREXAMPLE: ...] expression."
    )


def build_v2_user_message(record: dict) -> str:
    remaining = record.get("remaining_hypotheses", [])
    conclusion = record.get("conclusion", "")
    if remaining and conclusion:
        bulleted = "\n - ".join(remaining)
        message = (
            f"Claim: For all mathematical objects satisfying:\n"
            f" - {bulleted}\n"
            f"the following conclusion holds:\n"
            f"  {conclusion}"
        )
    else:
        message = (record.get("false_conjecture") or "").strip()

    schema_hint = _format_witness_schema_hint(record)
    if schema_hint:
        if message:
            return f"{message}\n\n{schema_hint}"
        return schema_hint
    return message


# Global system prompt for the v2.0 task framing as used in the paper.
#
# The policy is expected to produce free reasoning inside <reasoning>...</reasoning>
# tags followed by a single ``[COUNTEREXAMPLE: <expr>]`` tag. ``<expr>`` is a
# Python expression evaluable inside the per-theorem verifier's
# ``setup_namespace()``. The sentinel ``[COUNTEREXAMPLE: NONE]`` lets the model
# decline to disprove; in Stage 1 (``counterexample_only``) that is a "gave up"
# signal and is penalised by the oracle reward (see
# ``training/rlvr/reward_oracle.py``).
V2_SYSTEM_PROMPT: str = (
    "You are a mathematician evaluating a proposed conjecture.\n"
    "First, think through the conjecture step by step inside "
    "<reasoning> ... </reasoning> tags.\n"
    "Then, output a single line of the form:\n"
    "    [COUNTEREXAMPLE: <expression>]\n"
    "where <expression> is a Python expression evaluable under "
    "`from sympy import *`,\n"
    "referring to standard SymPy constructions (PermutationGroup, Matrix, "
    "ZZ, QQ, etc.).\n"
    "If you believe the conjecture is true and no counterexample exists, "
    "output:\n"
    "    [COUNTEREXAMPLE: NONE]\n"
    "Output nothing else after the tag."
)


__all__ = ["V2_SYSTEM_PROMPT", "build_v2_user_message"]
