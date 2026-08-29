import sympy
from sympy import ZZ, QQ, RR, CC, S
from sympy.polys.domains import Domain, FF
from sympy.abc import x, y, z

Z = ZZ
Q = QQ
R = RR
C = CC

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) > 0:
        F = witness[0]
    else:
        F = witness

    try:
        if isinstance(F, Domain):
            h1 = True
            is_field = F.is_Field
        elif F == S.Integers:
            h1 = True
            is_field = False
        elif F in (S.Rationals, S.Reals, S.Complexes):
            h1 = True
            is_field = True
        else:
            h1 = False
            is_field = False
    except Exception:
        h1 = False
        is_field = False

    try:
        if h1:
            neg_q = not is_field
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ['H_1: R is the ring of Laurent polynomials over F', 'not Q: R is not a Euclidean domain']

N_HYP = 1
NEG_Q_INDEX = 1