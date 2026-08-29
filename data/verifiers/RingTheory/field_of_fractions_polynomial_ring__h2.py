import sympy
from sympy.abc import x
from sympy.polys.domains import ZZ, QQ, Domain

def conditions(witness):
    try:
        if witness == sympy.S.Integers:
            R = ZZ
        elif witness == sympy.S.Rationals:
            R = QQ
        else:
            R = witness
    except Exception:
        R = witness

    try:
        h1 = isinstance(R, Domain)
    except Exception:
        h1 = False

    try:
        h2 = hasattr(R, 'poly_ring')
    except Exception:
        h2 = False

    try:
        # The conclusion implies R itself must be a field (so K = R is a field).
        # If R is not a field, the field of fractions of R[x] is not isomorphic to R(x).
        neg_q = not R.is_Field
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: Polynomial ring in one variable over R",
    "neg_Q: Field of fractions is not isomorphic to K(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2