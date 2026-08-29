import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import FreeGroup, free_group
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        F, x = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(F, FreeGroup)
    except Exception:
        h1 = False

    try:
        h2 = (getattr(x, 'group', None) == F) or (x in F)
    except Exception:
        h2 = False

    try:
        from sympy import oo
        if hasattr(x, 'order') and callable(x.order):
            neg_q = (x.order() != oo)
        elif hasattr(x, 'is_identity'):
            val = x.is_identity
            if callable(val):
                neg_q = bool(val())
            else:
                neg_q = bool(val)
        elif hasattr(F, 'identity'):
            neg_q = (x == F.identity)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: x is an element of F",
    "¬Q: x does not have infinite order"
]

N_HYP = 2
NEG_Q_INDEX = 2