import sympy
from sympy import Poly, Symbol, QQ, ZZ, GF, Rational
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            domain, expr = witness
            poly = Poly(expr, x, domain=domain)
        elif isinstance(witness, Poly):
            poly = witness
        else:
            poly = Poly(witness, x, domain=QQ)
    except Exception:
        return [False, False, False]

    try:
        is_f = poly.domain.is_Field
        h1 = False if is_f is None else bool(is_f)
    except Exception:
        h1 = False

    try:
        is_uni = poly.is_univariate
        is_z = poly.is_zero
        if is_uni is None or is_z is None:
            h2 = False
        else:
            h2 = bool(is_uni) and not bool(is_z)
    except Exception:
        h2 = False

    try:
        irr = poly.is_irreducible
        if irr is None:
            neg_q = False
        else:
            neg_q = not bool(irr)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a non-zero polynomial over F",
    "¬Q: f is not an irreducible polynomial over F"
]

N_HYP = 2
NEG_Q_INDEX = 2