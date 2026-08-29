import sympy
from sympy.abc import x, y, z

# Top-level setup
# (No specific named bindings required for this dictionary-based witness)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_proper_ideal", False))
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            neg_q = not bool(witness.get("has_finite_primary_decomposition", True))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: I cannot be expressed as the intersection of a finite number of primary ideals"
]

N_HYP = 1
NEG_Q_INDEX = 1