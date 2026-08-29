import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation(0)])
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_subgroup(G, H):
    for h in H.generators:
        if not G.contains(h):
            return False
    return True

def is_normal(G, H):
    if not is_subgroup(G, H):
        return False
    for g in G.generators:
        g_inv = ~g
        for h in H.generators:
            if not H.contains(g * h * g_inv):
                return False
    return True

def intersection_is_trivial(N, M):
    smaller, larger = (N, M) if N.order() < M.order() else (M, N)
    for g in smaller.generate():
        # Check if g is the identity permutation
        if all(i == g(i) for i in range(g.size)):
            continue
        if larger.contains(g):
            return False
    return True

def direct_product(N, M):
    deg_N = N.degree
    deg_M = M.degree
    if deg_N == 0: deg_N = 1
    if deg_M == 0: deg_M = 1
    gens = []
    
    for g in N.generators:
        arr = list(g.array_form)
        if len(arr) < deg_N:
            arr += list(range(len(arr), deg_N))
        arr += list(range(deg_N, deg_N + deg_M))
        gens.append(Permutation(arr))
        
    for h in M.generators:
        arr = list(h.array_form)
        if len(arr) < deg_M:
            arr += list(range(len(arr), deg_M))
        arr = list(range(deg_N)) + [x + deg_N for x in arr]
        gens.append(Permutation(arr))
        
    if not gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens)

def conditions(witness) -> list[bool]:
    try:
        G, N, M = witness
    except Exception:
        return [False] * 5

    # H_1: G is a group (and N, M are groups)
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(N, PermutationGroup) and isinstance(M, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        h2 = is_subgroup(G, N) and is_normal(G, N)
    except Exception:
        h2 = False

    # H_3: M is a normal subgroup of G
    try:
        h3 = is_subgroup(G, M) and is_normal(G, M)
    except Exception:
        h3 = False

    # H_4: The intersection of N and M is the trivial subgroup {e}
    try:
        h4 = intersection_is_trivial(N, M)
    except Exception:
        h4 = False

    # ¬Q: G is NOT isomorphic to the direct product N \times M
    try:
        if G.order() != N.order() * M.order():
            neg_q = True
        else:
            NxM = direct_product(N, M)
            if G.is_abelian != NxM.is_abelian:
                neg_q = True
            else:
                neg_q = not G.is_isomorphic(NxM)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: M is a normal subgroup of G",
    "H_4: The intersection of N and M is the trivial subgroup {e}",
    "¬Q: G is not isomorphic to the direct product N \\times M"
]

N_HYP = 4
NEG_Q_INDEX = 4