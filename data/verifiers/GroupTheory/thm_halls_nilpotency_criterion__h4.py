import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools
import functools
import math

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup):
            is_sub = True
            for gen in N.generators:
                if gen not in G:
                    is_sub = False
                    break
            if is_sub:
                is_norm = True
                for g in G.generators:
                    for n in N.generators:
                        if (g * n * ~g) not in N:
                            is_norm = False
                            break
                    if not is_norm:
                        break
                h2 = is_norm
    except Exception:
        h2 = False

    # H_3: N is a nilpotent group
    try:
        h3 = isinstance(N, PermutationGroup) and bool(N.is_nilpotent)
    except Exception:
        h3 = False

    # ¬Q: G is not nilpotent
    try:
        neg_q = isinstance(G, PermutationGroup) and not bool(G.is_nilpotent)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a nilpotent group",
    "¬Q: G is not nilpotent"
]

N_HYP = 3
NEG_Q_INDEX = 3