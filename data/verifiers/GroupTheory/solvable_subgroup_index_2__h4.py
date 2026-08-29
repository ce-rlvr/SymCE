import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
        G, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        if hasattr(H, "is_subgroup"):
            h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
        else:
            h2 = isinstance(H, PermutationGroup) and all(g in G for g in H.generators)
    except Exception:
        try:
            h2 = isinstance(H, PermutationGroup) and all(g in G for g in H.generators)
        except Exception:
            h2 = False

    # H_3: H is a solvable group
    try:
        h3 = isinstance(H, PermutationGroup) and bool(H.is_solvable)
    except Exception:
        h3 = False

    # ¬Q: G is not a solvable group
    try:
        neg_q = isinstance(G, PermutationGroup) and not bool(G.is_solvable)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: H is a solvable group",
    "¬Q: G is not a solvable group"
]

N_HYP = 3
NEG_Q_INDEX = 3