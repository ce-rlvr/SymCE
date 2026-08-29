import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.polys.domains import GF

FF2 = GF(2)
FF3 = GF(3)
FF5 = GF(5)
FF7 = GF(7)

def conditions(witness):
    try:
        h1 = bool(getattr(witness, 'is_PID', False) or getattr(witness, 'is_Field', False))
    except Exception:
        h1 = False

    try:
        # The polynomial ring over R is a principal ideal domain if and only if R is a field.
        neg_q = bool(getattr(witness, 'is_Field', False))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: the polynomial ring over R is a principal ideal domain"
]

N_HYP = 1
NEG_Q_INDEX = 1