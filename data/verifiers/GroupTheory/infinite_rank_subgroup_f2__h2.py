import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import free_group, FreeGroup

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

F1 = free_group("x")[0]
F2 = free_group("x, y")[0]
F3 = free_group("x, y, z")[0]

def conditions(witness):
    try:
        h1 = isinstance(witness, FreeGroup)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, FreeGroup):
            # A free group contains a subgroup of countably infinite rank iff its rank is >= 2.
            # Thus, it does NOT contain such a subgroup iff its rank is < 2.
            neg_q = len(witness.generators) < 2
        else:
            # For non-free groups, if it's finite, it definitely doesn't contain an infinite free group.
            if hasattr(witness, 'order') and witness.order() < float('inf'):
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: F does not contain a subgroup isomorphic to the free group of countably infinite rank"
]

N_HYP = 1
NEG_Q_INDEX = 1