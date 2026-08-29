import sympy
from sympy import ZZ, QQ

# Top-level setup
Z = ZZ
Q = QQ

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        R, M = witness
    else:
        R = witness
        M = witness

    try:
        h1 = False
        if hasattr(R, 'is_ring') and R.is_ring:
            h1 = True
        elif R in (ZZ, QQ):
            h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = False
        # ZZ and QQ as modules over themselves are not finitely cogenerated.
        # For ZZ, the intersection of all pZ is 0, but no finite intersection is 0.
        if M in (ZZ, QQ):
            neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: M is not finitely cogenerated"
]

N_HYP = 1
NEG_Q_INDEX = 1