import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

# Standard group bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]

    # H_1: G is a cyclic group
    try:
        if not isinstance(G, PermutationGroup):
            h1 = False
        else:
            order_G = G.order()
            h1 = any(g.order() == order_G for g in G.elements)
    except Exception:
        h1 = False

    # neg_Q: G and H are isomorphic if and only if |G| = |H| (Negated)
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(H, PermutationGroup):
            neg_q = False
        else:
            order_G = G.order()
            order_H = H.order()
            same_order = (order_G == order_H)
            iso = G.is_isomorphic(H)
            
            # The conclusion is (iso == same_order). We want the negation.
            neg_q = bool(iso != same_order)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "¬Q: It is false that G and H are isomorphic iff |G| = |H|"
]

N_HYP = 1
NEG_Q_INDEX = 1