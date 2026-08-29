import sympy
from sympy import Symbol

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC
Z = sympy.ZZ
Q = sympy.QQ
R = sympy.RR
C = sympy.CC

x = Symbol('x')
ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)

def conditions(witness):
    # H_1: R is an integral domain
    try:
        h1 = False
        if witness in (ZZ, QQ, RR, CC, sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes, ZZ_x, QQ_x):
            h1 = True
        elif hasattr(witness, 'is_Field'):
            if getattr(witness, 'is_Field', False):
                h1 = True
            elif getattr(witness, 'is_PID', False):
                h1 = True
            elif getattr(witness, 'is_UFD', False):
                h1 = True
            elif hasattr(witness, 'domain') and getattr(witness.domain, 'is_UFD', False):
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: Every non-zero element of R is a unit in R (fails)
    # i.e., R is NOT a field.
    try:
        neg_q = False
        if witness in (ZZ, sympy.S.Integers, ZZ_x, QQ_x):
            neg_q = True
        elif witness in (QQ, RR, CC, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
            neg_q = False
        elif hasattr(witness, 'is_Field'):
            neg_q = not getattr(witness, 'is_Field', False)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: R has a non-zero element that is not a unit (R is not a field)"
]

N_HYP = 1
NEG_Q_INDEX = 1