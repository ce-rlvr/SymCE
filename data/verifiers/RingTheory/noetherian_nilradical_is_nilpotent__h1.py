import sympy
from sympy import symbols
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        if hasattr(witness, 'is_noetherian'):
            h1 = bool(witness.is_noetherian() if callable(witness.is_noetherian) else witness.is_noetherian)
        elif hasattr(witness, 'is_Noetherian'):
            h1 = bool(witness.is_Noetherian() if callable(witness.is_Noetherian) else witness.is_Noetherian)
    except Exception:
        h1 = False

    try:
        q = True
        if hasattr(witness, 'nilradical_is_nilpotent'):
            q = bool(witness.nilradical_is_nilpotent() if callable(witness.nilradical_is_nilpotent) else witness.nilradical_is_nilpotent)
        elif hasattr(witness, 'is_nilradical_nilpotent'):
            q = bool(witness.is_nilradical_nilpotent() if callable(witness.is_nilradical_nilpotent) else witness.is_nilradical_nilpotent)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "¬Q: The nilradical of R is not a nilpotent ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1