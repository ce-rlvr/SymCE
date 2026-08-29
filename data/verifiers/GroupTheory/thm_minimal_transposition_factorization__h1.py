import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        h1 = isinstance(witness, Permutation)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, Permutation):
            neg_q = False
        else:
            n = witness.size
            c_sigma = len(witness.full_cyclic_form)
            min_trans = sum(len(c) - 1 for c in witness.cyclic_form)
            neg_q = not (min_trans == n - c_sigma)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: witness is a Permutation",
    "¬Q: The minimal number of transpositions is NOT exactly n - c(sigma)"
]

N_HYP = 1
NEG_Q_INDEX = 1