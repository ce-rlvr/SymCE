import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            # Z(G) is the center of G; verify the center is well-defined
            center_group = witness.center()
            h2 = isinstance(center_group, PermutationGroup)
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1:
            # The conclusion is that G is nilpotent.
            # We want the negation: G is NOT nilpotent.
            neg_q = not bool(witness.is_nilpotent)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Z(G) is the center of G",
    "¬Q: G is not a nilpotent group"
]

N_HYP = 2
NEG_Q_INDEX = 2