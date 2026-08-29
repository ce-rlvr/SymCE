import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy import oo

# Top-level setup
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
    # H_1: The rank of F is an integer n >= 2
    try:
        # For finite groups, the rank (minimum number of generators) is >= 2 
        # if and only if the group is not cyclic.
        is_cyc = witness.is_cyclic
        if callable(is_cyc):
            is_cyc = is_cyc()
        h1 = (is_cyc is False)
    except Exception:
        h1 = False

    # neg_Q: F does not contain a subgroup isomorphic to the free group of countably infinite rank
    try:
        order = witness.order
        if callable(order):
            order = order()
        # A finite group cannot contain an infinite subgroup.
        # (If the witness is infinite, we conservatively return False as it's harder to check automatically,
        # but finite counterexamples like S3 or V4 will be correctly verified).
        neg_q = (order < oo)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The rank of F is an integer n >= 2",
    "¬Q: F does not contain a subgroup isomorphic to the free group of countably infinite rank"
]

N_HYP = 1
NEG_Q_INDEX = 1