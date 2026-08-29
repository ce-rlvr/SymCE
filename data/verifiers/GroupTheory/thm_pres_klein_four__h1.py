import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1), Permutation(2, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if witness.order() != 4:
            is_V4 = False
        else:
            is_V4 = True
            for g in witness.elements:
                if g.order() > 2:
                    is_V4 = False
                    break
        neg_q = not is_V4
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: V does not admit the presentation <a, b | a^2 = 1, b^2 = 1, ab = ba>"
]

N_HYP = 0
NEG_Q_INDEX = 0