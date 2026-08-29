import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

def is_normal(G, H):
    try:
        if not H.is_subgroup(G):
            return False
        for g in G.generators:
            for h in H.generators:
                if (g * h * ~g) not in H:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False] * 5
        G, M, N = witness
    except Exception:
        return [False] * 5

    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(M, PermutationGroup) and isinstance(N, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = h1 and is_normal(G, M)
    except Exception:
        h2 = False

    try:
        h3 = h1 and is_normal(G, N)
    except Exception:
        h3 = False

    try:
        h4 = h1 and bool(N.is_nilpotent)
    except Exception:
        h4 = False

    try:
        if not h1:
            neg_q = False
        else:
            MN = PermutationGroup(M.generators + N.generators)
            q = is_normal(G, MN) and bool(MN.is_nilpotent)
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: M is a normal subgroup of G",
    "H_3: N is a normal subgroup of G",
    "H_4: N is a nilpotent group",
    "¬Q: The product MN is not a normal nilpotent subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4