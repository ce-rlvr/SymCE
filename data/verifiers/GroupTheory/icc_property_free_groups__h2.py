import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        F, x = witness
    except Exception:
        return [False, False, False]

    # H_1: F is a free group
    try:
        h1 = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1 = False

    # H_2: x is a non-identity element of F
    try:
        h2 = (getattr(x, 'group', None) == F) and (x != F.identity)
    except Exception:
        h2 = False

    # neg_Q: The conjugacy class of x in F is infinite -> FAILS -> is finite
    try:
        if type(F).__name__ == 'FreeGroup':
            if x == F.identity:
                neg_q = True
            else:
                neg_q = F.rank < 2
        else:
            neg_q = getattr(F, 'is_finite', False) or getattr(F, 'is_abelian', False)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: x is a non-identity element of F",
    "¬Q: The conjugacy class of x in F is finite"
]

N_HYP = 2
NEG_Q_INDEX = 2