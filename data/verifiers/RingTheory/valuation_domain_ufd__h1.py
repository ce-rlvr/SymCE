import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y

# Top-level setup: named object bindings that the witness expression may reference.
Z = ZZ
Q = QQ
Qx = QQ[x]
Zx = ZZ[x]

def conditions(witness) -> list[bool]:
    try:
        # A valid witness should be a ring domain in SymPy, which typically has the 'is_UFD' attribute.
        if not hasattr(witness, 'is_UFD'):
            return [False]
    except Exception:
        return [False]

    try:
        is_ufd = bool(getattr(witness, 'is_UFD', False))
    except Exception:
        is_ufd = False

    try:
        is_field = bool(getattr(witness, 'is_Field', False))
    except Exception:
        is_field = False

    try:
        # SymPy does not have a built-in representation for Discrete Valuation Rings.
        # Standard domains like ZZ, QQ, QQ[x] are not DVRs.
        # We check for custom attributes just in case a mock object is provided.
        is_dvr = bool(getattr(witness, 'is_DVR', False) or getattr(witness, 'is_discrete_valuation_ring', False))
    except Exception:
        is_dvr = False

    try:
        # The conclusion is: R is a UFD iff R is a field or a DVR.
        # We want the negation of this conclusion (i.e., the biconditional fails).
        conclusion = (is_ufd == (is_field or is_dvr))
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: It is not the case that R is a UFD iff R is a field or a DVR"
]

N_HYP = 0
NEG_Q_INDEX = 0