import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        G, n, H = witness
    except Exception:
        return [False, False, False, False]

    # H1: G is a group
    try:
        h1 = bool(isinstance(G, PermutationGroup))
    except Exception:
        h1 = False

    # H2: n is a positive integer
    try:
        h2 = bool(isinstance(n, int) and n > 0)
    except Exception:
        h2 = False

    # H3: H is a subgroup of G of index n
    try:
        if isinstance(H, PermutationGroup):
            if hasattr(H, 'is_subgroup'):
                is_sub = H.is_subgroup(G)
            else:
                is_sub = all(g in G for g in H.generators)
            h3 = bool(is_sub and (G.order() == n * H.order()))
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: H is NOT a normal subgroup of G
    try:
        if h1 and h3:
            if hasattr(H, 'is_normal'):
                is_normal = H.is_normal(G)
            else:
                is_normal = True
                for g in G.generators:
                    g_inv = ~g
                    for h in H.generators:
                        if (g * h * g_inv) not in H:
                            is_normal = False
                            break
                        if (g_inv * h * g) not in H:
                            is_normal = False
                            break
                    if not is_normal:
                        break
            neg_q = bool(not is_normal)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: n is a positive integer",
    "H_3: H is a subgroup of G of index n",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3