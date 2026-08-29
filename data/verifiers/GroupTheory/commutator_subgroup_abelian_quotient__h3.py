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

def conditions(witness) -> list[bool]:
    try:
        if not (isinstance(witness, tuple) or isinstance(witness, list)) or len(witness) != 2:
            h1 = False
        else:
            G, N = witness
            h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            G, N = witness
            is_sub = all(n in G for n in N.generators)
            if is_sub:
                is_normal = True
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N:
                            is_normal = False
                            break
                    if not is_normal:
                        break
                h2 = is_normal
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1:
            G, N = witness
            is_abelian = True
            for g in G.generators:
                for h in G.generators:
                    if (g * h * ~g * ~h) not in N:
                        is_abelian = False
                        break
                if not is_abelian:
                    break
            neg_q = not is_abelian
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: G/N is not abelian"
]

N_HYP = 2
NEG_Q_INDEX = 2