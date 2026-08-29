import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness) -> list[bool]:
    try:
        order = int(witness.order())
        h1 = order > 0
    except Exception:
        h1 = False

    try:
        order = int(witness.order())
        h2 = order > 1
    except Exception:
        h2 = False

    try:
        order = int(witness.order())
        neg_q = (order % 60) != 0
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a non-trivial group",
    "¬Q: The order of G is not an integer multiple of 60"
]

N_HYP = 2
NEG_Q_INDEX = 2