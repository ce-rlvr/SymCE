import sympy
from sympy.polys.domains import RR, CC, QQ, ZZ, EX
from sympy.abc import x, y, z

def conditions(witness):
    try:
        h1 = False
        if getattr(witness, 'is_Field', False):
            if RR.unify(witness) == witness:
                h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = False
        if witness != RR and witness != CC:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: E is a field extension of the real numbers R",
    "not Q: The degree of E over R is not equal to 1 or 2"
]

N_HYP = 1
NEG_Q_INDEX = 1