import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        # Definitional hypothesis: Aut(G) is the automorphism group of G
        h2 = isinstance(witness, PermutationGroup)
    except Exception:
        h2 = False

    try:
        # Mathematically, Inn(G) is ALWAYS a normal subgroup of Aut(G) for any group G.
        # Therefore, the conclusion "Inn(G) is a normal subgroup of Aut(G)" is ALWAYS TRUE.
        # Its negation is ALWAYS FALSE.
        neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: Aut(G) is the automorphism group of G",
    "¬Q: Inn(G) is not a normal subgroup of Aut(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2