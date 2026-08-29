import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
        elements = list(witness.generate())
        seen = set()
        c_count = 0
        for g in elements:
            if g not in seen:
                c_count += 1
                for x in elements:
                    seen.add(x * g * ~x)
        h1 = bool(c_count == 3)
    except Exception:
        h1 = False

    try:
        neg_q = not bool(witness.is_solvable)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G has exactly three conjugacy classes",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1