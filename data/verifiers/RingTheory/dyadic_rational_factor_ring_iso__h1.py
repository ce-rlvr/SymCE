import sympy
from sympy import ZZ, QQ
from sympy.abc import x

def conditions(witness):
    try:
        # Check if 2x - 1 is in the ring
        _ = witness(2*x - 1)
        h1 = True
    except Exception:
        h1 = False

    try:
        is_iso = False
        if hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
            if witness.domain == ZZ and set(witness.symbols) == {x}:
                is_iso = True
        neg_q = not is_iso
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: 2x - 1 is in R",
    "not Q: R/(2x - 1) is not isomorphic to Z(1/2)"
]

N_HYP = 1
NEG_Q_INDEX = 1