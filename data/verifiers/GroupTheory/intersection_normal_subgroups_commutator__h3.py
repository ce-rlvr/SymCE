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
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
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
    
    try:
        if not isinstance(G, PermutationGroup):
            G = PermutationGroup(G)
        if not isinstance(N, PermutationGroup):
            N = PermutationGroup(N)
    except Exception:
        return [False, False, False]

    # H_1: G is a nilpotent group
    try:
        if callable(G.is_nilpotent):
            h1 = bool(G.is_nilpotent())
        else:
            h1 = bool(G.is_nilpotent)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = True
        # Check if N is a subgroup of G
        for n in N.generators:
            if not G.contains(n):
                h2 = False
                break
        # Check normality: g * n * g^-1 in N for all generators
        if h2:
            for g in G.generators:
                for n in N.generators:
                    if not N.contains(g * n * ~g):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # ¬Q: N is NOT contained in the center Z(G)
    try:
        neg_q = False
        for n in N.generators:
            for g in G.generators:
                if n * g != g * n:
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: N is a normal subgroup of G",
    "¬Q: N is not contained in the center Z(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2