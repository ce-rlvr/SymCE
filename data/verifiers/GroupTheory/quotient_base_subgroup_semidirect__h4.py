import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_group(G):
    return isinstance(G, PermutationGroup)

def is_subgroup(H, G):
    try:
        if not is_group(H) or not is_group(G): 
            return False
        for h in H.generators:
            if h not in G:
                return False
        return True
    except Exception:
        return False

def is_normal(N, G):
    try:
        if not is_subgroup(N, G): 
            return False
        for g in G.generators:
            for n in N.generators:
                if (g * n * ~g) not in N:
                    return False
        return True
    except Exception:
        return False

def safe_group(gens):
    if not gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens)

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False] * 6
        G, N, H, K = witness
    except Exception:
        return [False] * 6

    # H1: G is a group
    try:
        h1 = is_group(G)
    except Exception:
        h1 = False

    # H2: N is a normal subgroup of G
    try:
        h2 = is_normal(N, G)
    except Exception:
        h2 = False

    # H3: H is a subgroup of G
    try:
        h3 = is_subgroup(H, G)
    except Exception:
        h3 = False

    # H4: K is a normal subgroup of G
    try:
        h4 = is_normal(K, G)
    except Exception:
        h4 = False

    # H5: K is a subgroup of N
    try:
        h5 = is_subgroup(K, N)
    except Exception:
        h5 = False

    # neg_Q: G/K is NOT isomorphic to the internal semidirect product of N/K and HK/K
    # This means either N/K intersect HK/K is not trivial (i.e., N intersect HK != K)
    # or (N/K)(HK/K) != G/K (i.e., NH != G).
    try:
        if not (is_group(G) and is_group(N) and is_group(H) and is_group(K)):
            neg_q = False
        else:
            HK = safe_group(list(H.generators) + list(K.generators))
            N_int_HK = N.intersect(HK)
            cond1 = (N_int_HK.order() == K.order())
            
            NH = safe_group(list(N.generators) + list(H.generators))
            cond2 = (NH.order() == G.order())
            
            Q = cond1 and cond2
            neg_q = not Q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "H_4: K is a normal subgroup of G",
    "H_5: K is a subgroup of N",
    "¬Q: G/K is not isomorphic to the internal semidirect product of N/K and HK/K"
]

N_HYP = 5
NEG_Q_INDEX = 5