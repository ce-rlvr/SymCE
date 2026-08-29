import sympy
from sympy import Poly
from sympy.abc import x

QQ = sympy.QQ
ZZ = sympy.ZZ
RR = sympy.RR
CC = sympy.CC

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a polynomial over F",
    "not Q: the quotient ring is not an n-dimensional vector space over F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            domain, expr = witness
            poly = Poly(expr, x, domain=domain)
        elif isinstance(witness, Poly):
            poly = witness
        else:
            poly = Poly(witness, x, domain='QQ')
    except Exception:
        return [False, False, False]

    try:
        H1 = poly.domain.is_Field
    except Exception:
        H1 = False

    try:
        H2 = len(poly.gens) <= 1
    except Exception:
        H2 = False

    try:
        neg_Q = poly.is_zero
    except Exception:
        neg_Q = False

    return [bool(H1), bool(H2), bool(neg_Q)]