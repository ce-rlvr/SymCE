import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)

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

def conditions(witness):
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = bool(witness.is_nilpotent())
    except Exception:
        h2 = False

    try:
        G_prime = witness.derived_subgroup()
        Z_G = witness.center()
        
        is_subgroup = all(g in Z_G for g in G_prime.generators)
        is_non_trivial = (G_prime.order() > 1)
        
        neg_q = not (is_subgroup and is_non_trivial)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is a nilpotent group",
    "¬Q: The commutator subgroup G' is not a non-trivial subgroup of the center Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2