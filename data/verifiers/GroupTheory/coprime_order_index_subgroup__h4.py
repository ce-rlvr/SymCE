import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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
        G, N, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if isinstance(N, PermutationGroup) and isinstance(G, PermutationGroup):
            if N.is_subgroup(G):
                h2 = True
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N:
                            h2 = False
                            break
                    if not h2:
                        break
    except Exception:
        h2 = False

    # H_3: H is a subgroup of G
    try:
        h3 = False
        if isinstance(H, PermutationGroup) and isinstance(G, PermutationGroup):
            h3 = bool(H.is_subgroup(G))
    except Exception:
        h3 = False

    # ¬Q: H is not a subset of N
    try:
        neg_q = False
        if isinstance(H, PermutationGroup) and isinstance(N, PermutationGroup):
            neg_q = not bool(H.is_subgroup(N))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "¬Q: H is not a subset of N"
]

N_HYP = 3
NEG_Q_INDEX = 3