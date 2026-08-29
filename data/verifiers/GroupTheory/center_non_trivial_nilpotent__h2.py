import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    # H_1: G is a nilpotent group
    try:
        if callable(witness.is_nilpotent):
            h1 = bool(witness.is_nilpotent())
        else:
            h1 = bool(witness.is_nilpotent)
    except Exception:
        h1 = False

    # ¬Q: The center Z(G) is trivial (order == 1)
    try:
        if callable(witness.center):
            c = witness.center()
        else:
            c = witness.center
            
        if callable(c.order):
            order = c.order()
        else:
            order = c.order
            
        neg_q = bool(order == 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: The center Z(G) is trivial"
]

N_HYP = 1
NEG_Q_INDEX = 1