import sympy
from sympy.combinatorics import PermutationGroup
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
    # H_1: F is a group (the hypothesis establishes notation for the lower central series of F)
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # ¬Q: The intersection of the lower central series of F is not trivial.
    # For finite groups, the lower central series stabilizes.
    # The intersection is trivial if and only if the group is nilpotent.
    # Therefore, the intersection is NOT trivial iff the group is NOT nilpotent.
    try:
        if not h1:
            neg_q = False
        else:
            val = witness.is_nilpotent
            if callable(val):
                is_nilp = val()
            else:
                is_nilp = bool(val)
            neg_q = not is_nilp
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a group",
    "¬Q: The intersection of the lower central series of F is not trivial"
]

N_HYP = 1
NEG_Q_INDEX = 1