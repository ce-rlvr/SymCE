import sympy
from sympy import ZZ, QQ, RR, CC, S, Set
from sympy.polys.domains import Domain

# Top-level setup
Z = ZZ
Q = QQ

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                R, a, b, c = witness
            elif len(witness) == 3:
                a, b, c = witness
                R = ZZ
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        if isinstance(R, Domain):
            h1 = True
        elif isinstance(R, Set) and R in (S.Integers, S.Rationals, S.Reals, S.Complexes):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        h2 = (a in R) and (b in R) and (c in R)
    except Exception:
        h2 = False

    try:
        h3 = bool(a != 0)
    except Exception:
        h3 = False

    try:
        neg_q = bool(b != c)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: a, b, c are elements of R",
    "H_3: a is not equal to 0",
    "¬Q: b != c"
]

N_HYP = 3
NEG_Q_INDEX = 3