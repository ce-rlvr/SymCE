import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
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
    # H_1: G is a locally cyclic group.
    # For finite groups (which SymPy PermutationGroups are), 
    # being locally cyclic is equivalent to being cyclic.
    try:
        h1 = bool(witness.is_cyclic)
    except Exception:
        h1 = False

    # ¬Q: G is NOT isomorphic to a subgroup of the additive group of rational numbers (Q, +).
    # The only finite subgroup of (Q, +) is the trivial group {0}.
    # Therefore, a finite group is isomorphic to a subgroup of (Q, +) if and only if its order is 1.
    try:
        try:
            order = witness.order()
        except TypeError:
            order = witness.order
            
        if order == sympy.oo:
            # If the group is infinite and cyclic (e.g., Z), it is isomorphic to a subgroup of Q.
            neg_q = False
        else:
            # For finite groups, it fails to embed in Q iff its order > 1.
            neg_q = bool(order > 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a locally cyclic group",
    "¬Q: G is not isomorphic to a subgroup of the additive group of rational numbers (Q, +)"
]

N_HYP = 1
NEG_Q_INDEX = 1