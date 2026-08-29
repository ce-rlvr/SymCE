import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        if callable(witness.is_abelian):
            h2 = not witness.is_abelian()
        else:
            h2 = not witness.is_abelian
    except Exception:
        h2 = False

    try:
        if callable(witness.order):
            order = witness.order()
        else:
            order = witness.order
        h3 = order > 0
    except Exception:
        h3 = False

    try:
        if callable(witness.center):
            center = witness.center()
        else:
            center = witness.center
            
        if callable(center.order):
            c_order = center.order()
        else:
            c_order = center.order
            
        neg_q = c_order > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is non-abelian",
    "H_3: Order of G is pq",
    "¬Q: The center Z(G) is not the trivial subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3