import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
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
        classes = witness.conjugacy_classes()
        h1 = (len(list(classes)) == 3)
    except Exception:
        h1 = False

    is_z3 = False
    try:
        is_z3 = (witness.order() == 3)
    except Exception:
        pass

    is_s3 = False
    try:
        is_s3 = (witness.order() == 6 and not witness.is_abelian)
    except Exception:
        pass

    neg_q = not (is_z3 or is_s3)

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G has exactly three conjugacy classes",
    "¬Q: G is not isomorphic to Z_3 or S_3"
]

N_HYP = 1
NEG_Q_INDEX = 1