import sympy
from sympy import Poly
from sympy.abc import x, y

QQ = sympy.QQ
ZZ = sympy.ZZ
GF = sympy.GF
Rational = sympy.Rational
Integer = sympy.Integer

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            domain, expr = witness
            poly = Poly(expr, x, domain=domain)
        elif isinstance(witness, Poly):
            poly = witness
        else:
            poly = Poly(witness, x)
    except Exception:
        return [False, False]

    try:
        h1 = bool(poly.domain.is_Field)
    except Exception:
        h1 = False

    try:
        neg_q = not bool(poly.is_irreducible)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: F is a field", "not Q: The factor ring is not an integral domain whose field of fractions is E(y)"]

N_HYP = 1
NEG_Q_INDEX = 1