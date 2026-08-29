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
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, N = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            is_sub = all(G.contains(g) for g in N.generators)
            is_norm = all(N.contains(g * n * ~g) for g in G.generators for n in N.generators)
            h2 = bool(is_sub and is_norm)
    except Exception:
        h2 = False

    # neg_Q: N is NOT contained in the center Z(G)
    try:
        # N is contained in Z(G) iff all generators of N commute with all generators of G
        contained_in_center = all(n * g == g * n for n in N.generators for g in G.generators)
        neg_q = not contained_in_center
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: N is not contained in the center Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2