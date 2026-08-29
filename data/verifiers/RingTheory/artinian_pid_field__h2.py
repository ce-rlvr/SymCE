import sympy
from sympy import ZZ, QQ
from sympy.abc import x

# Top-level setup
Z = ZZ
Q = QQ
try:
    Qx = QQ.poly_ring(x)
    Zx = ZZ.poly_ring(x)
except Exception:
    pass

def conditions(witness):
    try:
        if witness == sympy.S.Integers:
            witness = ZZ
        elif witness == sympy.S.Rationals:
            witness = QQ
    except Exception:
        pass

    try:
        h1 = bool(getattr(witness, 'is_PID', False))
    except Exception:
        h1 = False

    try:
        is_field = getattr(witness, 'is_Field', None)
        if is_field is None:
            neg_q = False
        else:
            neg_q = not bool(is_field)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: R is not a field"
]

N_HYP = 1
NEG_Q_INDEX = 1