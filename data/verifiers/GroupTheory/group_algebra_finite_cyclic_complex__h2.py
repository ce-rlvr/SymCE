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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        if isinstance(witness, PermutationGroup):
            if witness.is_cyclic:
                h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = False
        if isinstance(witness, PermutationGroup):
            if not witness.is_abelian:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group of order n",
    "¬Q: the group algebra is not isomorphic as a ring to the direct product of n copies of C"
]

N_HYP = 1
NEG_Q_INDEX = 1