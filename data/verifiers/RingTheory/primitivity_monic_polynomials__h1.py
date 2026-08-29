import sympy
from sympy import Poly, Rational, Integer
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness)
        h1 = bool(f.is_monic)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness)
        neg_q = not bool(f.is_primitive)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a monic polynomial",
    "not Q: f is not a primitive polynomial"
]

N_HYP = 1
NEG_Q_INDEX = 1