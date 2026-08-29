import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def inv(g):
    try:
        return ~g
    except Exception:
        return g**-1

def group_contains(H, elem):
    try:
        if hasattr(H, 'contains'):
            return H.contains(elem)
        return elem in H
    except Exception:
        for x in H.generate():
            if x == elem:
                return True
        return False

def is_subgroup(G, H):
    if hasattr(H, 'is_subgroup'):
        try:
            return H.is_subgroup(G)
        except Exception:
            pass
    for gen in H.generators:
        if not group_contains(G, gen):
            return False
    return True

def is_normal(G, H):
    if hasattr(G, 'is_normal'):
        try:
            return G.is_normal(H)
        except Exception:
            pass
    if not is_subgroup(G, H):
        return False
    for g in G.generators:
        ginv = inv(g)
        for h in H.generators:
            if not group_contains(H, g * h * ginv):
                return False
            if not group_contains(H, ginv * h * g):
                return False
    return True

def intersection_order(G, N, M):
    if hasattr(N, 'intersection'):
        try:
            return N.intersection(M).order()
        except Exception:
            pass
    if hasattr(N, 'intersect'):
        try:
            return N.intersect(M).order()
        except Exception:
            pass
    
    count = 0
    for n in N.generate():
        if group_contains(M, n):
            count += 1
    return count

def check_G_eq_NM(G, N, M):
    if not is_subgroup(G, N) or not is_subgroup(G, M):
        return False
    int_order = intersection_order(G, N, M)
    if int_order is None:
        return False
    return G.order() * int_order == N.order() * M.order()

def check_intersection_trivial(G, N, M):
    if not is_subgroup(G, N) or not is_subgroup(G, M):
        return False
    int_order = intersection_order(G, N, M)
    return int_order == 1

def direct_product(N, M):
    if not all(isinstance(g, Permutation) for g in N.generators) or \
       not all(isinstance(g, Permutation) for g in M.generators):
        raise ValueError("direct_product only supports PermutationGroups")
        
    size_N = getattr(N, 'degree', None)
    if size_N is None:
        size_N = max([g.size for g in N.generators] + [0])
        
    size_M = getattr(M, 'degree', None)
    if size_M is None:
        size_M = max([g.size for g in M.generators] + [0])
        
    gens = []
    for g in N.generators:
        arr = list(g.array_form)
        if len(arr) < size_N:
            arr += list(range(len(arr), size_N))
        arr += list(range(size_N, size_N + size_M))
        gens.append(Permutation(arr))
        
    for g in M.generators:
        arr = list(g.array_form)
        if len(arr) < size_M:
            arr += list(range(len(arr), size_M))
        shifted = list(range(size_N)) + [x + size_N for x in arr]
        gens.append(Permutation(shifted))
        
    if not gens:
        return PermutationGroup([Permutation(0)])
    return PermutationGroup(gens)

def conditions(witness):
    """
    Given a witness (G, N, M), checks the hypotheses and the negated conclusion.
    Returns a list of booleans: [H1, H2, H3, H4, neg_Q]
    """
    try:
        G, N, M = witness
    except Exception:
        return [False] * 5

    try:
        h1 = bool(is_normal(G, N))
    except Exception:
        h1 = False

    try:
        h2 = bool(is_normal(G, M))
    except Exception:
        h2 = False

    try:
        h3 = bool(check_G_eq_NM(G, N, M))
    except Exception:
        h3 = False

    try:
        h4 = bool(check_intersection_trivial(G, N, M))
    except Exception:
        h4 = False

    try:
        NxM = direct_product(N, M)
        q = G.is_isomorphic(NxM)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: M is a normal subgroup of G",
    "H_3: G = NM",
    "H_4: The intersection of N and M is the trivial subgroup {e}",
    "¬Q: G is not isomorphic to the direct product N \\times M"
]

N_HYP = 4
NEG_Q_INDEX = 4