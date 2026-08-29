import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        if int(witness) != witness or isinstance(witness, bool):
            h1 = False
        else:
            h1 = bool(witness >= 3)
    except Exception:
        h1 = False

    try:
        if int(witness) != witness or isinstance(witness, bool):
            neg_q = False
        else:
            n = int(witness)
            if n < 1:
                neg_q = False
            else:
                G = SymmetricGroup(n)
                C = G.center()
                neg_q = bool(C.order() != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 3",
    "¬Q: The center of S_n is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1