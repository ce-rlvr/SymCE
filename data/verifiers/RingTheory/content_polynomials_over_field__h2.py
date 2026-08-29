import sympy
from sympy import Poly, QQ, ZZ, Rational
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            domain, f = witness
        else:
            f = witness
            domain = f.domain
        h1 = domain.is_Field
    except Exception:
        h1 = False

    try:
        if isinstance(witness, tuple):
            domain, f = witness
        else:
            f = witness
            domain = f.domain
            
        c = f.content()
        # In a field, an element is a unit iff it is non-zero.
        is_unit = bool(c != 0)
        is_primitive = is_unit
        neg_q = not (is_unit and is_primitive)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: The content of f(x) is not a unit in F, or f(x) is not primitive"
]

N_HYP = 1
NEG_Q_INDEX = 1