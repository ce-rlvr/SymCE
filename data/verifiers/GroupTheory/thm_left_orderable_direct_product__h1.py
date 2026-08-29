import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    try:
        # H is a left-orderable group.
        # For finite groups, a group is left-orderable if and only if it is the trivial group.
        h1 = isinstance(H, PermutationGroup) and H.order() == 1
    except Exception:
        h1 = False

    try:
        # Conclusion: The direct product G x H is a left-orderable group.
        # Negated conclusion: G x H is NOT a left-orderable group.
        # For finite groups, this means the order of G x H is strictly greater than 1.
        neg_q = (isinstance(G, PermutationGroup) and 
                 isinstance(H, PermutationGroup) and 
                 (G.order() * H.order() > 1))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a left-orderable group",
    "¬Q: The direct product G x H is not a left-orderable group"
]

N_HYP = 1
NEG_Q_INDEX = 1
