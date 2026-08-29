import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.combinatorics.permutations import Permutation

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G is cyclic
    try:
        h2 = False
        if h1:
            order = witness.order()
            # A finite group is cyclic if it contains an element of order equal to the group's order
            elements = witness.elements if hasattr(witness, 'elements') else witness.generate()
            for g in elements:
                if g.order() == order:
                    h2 = True
                    break
    except Exception:
        h2 = False

    # ¬Q: G is not isomorphic to the additive group of integers Z
    try:
        neg_q = False
        if h1:
            # The additive group of integers Z is infinite.
            # Any valid PermutationGroup in SymPy is finite, hence cannot be isomorphic to Z.
            neg_q = witness.order() < float('inf')
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is cyclic",
    "¬Q: G is not isomorphic to the additive group of integers Z"
]

N_HYP = 2
NEG_Q_INDEX = 2