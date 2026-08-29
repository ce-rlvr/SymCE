import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        G, N, K = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and G.is_normal(N)
    except Exception:
        h2 = False

    # H_3: N is a subset of K
    try:
        if isinstance(N, PermutationGroup):
            if isinstance(K, PermutationGroup):
                h3 = all(g in K for g in N.generators)
            else:
                h3 = all(g in K for g in N.elements)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: K/N is not a normal subgroup of G/N, or (G/N)/(K/N) is not isomorphic to G/K
    try:
        if not isinstance(K, PermutationGroup) or not isinstance(N, PermutationGroup):
            neg_q = True
        elif not K.is_subgroup(G):
            neg_q = True
        elif not G.is_normal(K):
            neg_q = True
        elif not G.is_normal(N):
            neg_q = True
        elif not all(g in K for g in N.generators):
            neg_q = True
        else:
            # If K is a normal subgroup of G, N is normal in G, and N <= K,
            # then by the Third Isomorphism Theorem, the conclusion holds.
            neg_q = False
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: N is a subset of K",
    "¬Q: K/N is not a normal subgroup of G/N, or (G/N)/(K/N) is not isomorphic to G/K"
]

N_HYP = 3
NEG_Q_INDEX = 3