import sympy
from sympy import ZZ, QQ
from sympy.abc import x

Z = sympy.ZZ
Q = sympy.QQ
Zx = sympy.ZZ.poly_ring(x)
Qx = sympy.QQ.poly_ring(x)

def conditions(witness) -> list[bool]:
    try:
        h1 = hasattr(witness, 'is_Field') and hasattr(witness, 'get_ring')
    except Exception:
        h1 = False

    try:
        neg_q = not witness.is_Field
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: R is not a field"
]

N_HYP = 1
NEG_Q_INDEX = 1