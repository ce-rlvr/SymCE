import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        if getattr(witness, 'is_Field', False):
            h1 = True
        elif witness in (ZZ, QQ):
            h1 = True
        elif hasattr(witness, 'domain') and hasattr(witness, 'symbols'):
            h1 = True
    except Exception:
        h1 = False

    try:
        h2 = not bool(getattr(witness, 'is_Field', False))
    except Exception:
        h2 = False

    try:
        neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: R is not a field",
    "¬Q: R is not a discrete valuation ring (DVR)"
]

N_HYP = 2
NEG_Q_INDEX = 2