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
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_elements(G):
    if hasattr(G, 'elements'):
        return G.elements
    elif hasattr(G, 'generate'):
        return list(G.generate())
    else:
        return list(G)

def contains(G, g):
    try:
        return bool(g in G)
    except Exception:
        pass
    try:
        return bool(G.contains(g))
    except Exception:
        pass
    return g in get_elements(G)

def is_normal(N, G):
    try:
        res = N.is_normal(G)
        if res is not None:
            return bool(res)
    except Exception:
        pass
    
    for n in N.generators:
        for g in G.generators:
            conj1 = g * n * (~g)
            conj2 = (~g) * n * g
            if not contains(N, conj1) or not contains(N, conj2):
                return False
    return True

def is_subgroup(H, G):
    try:
        res = H.is_subgroup(G)
        if res is not None:
            return bool(res)
    except Exception:
        pass
    
    for h in H.generators:
        if not contains(G, h):
            return False
    return True

def is_abelian(G):
    try:
        res = G.is_abelian
        if res is not None:
            return bool(res)
    except Exception:
        pass
    
    gens = G.generators
    for g1 in gens:
        for g2 in gens:
            if g1 * g2 != g2 * g1:
                return False
    return True

def get_order(G):
    try:
        if callable(G.order):
            return G.order()
        return G.order
    except Exception:
        return len(get_elements(G))

def intersection_is_trivial(N, H):
    common = 0
    for g in get_elements(N):
        if contains(H, g):
            common += 1
            if common > 1:
                return False
    return True

def is_trivial(G):
    return get_order(G) == 1

def h1_check(G, N, H):
    return is_subgroup(N, G) and is_normal(N, G) and is_abelian(N)

def h2_check(G, N, H):
    if not is_subgroup(H, G):
        return False
    if not is_normal(N, G):
        return False
    if not intersection_is_trivial(N, H):
        return False
    if get_order(N) * get_order(H) != get_order(G):
        return False
    return True

def neg_q_check(G, N, H):
    Q = is_trivial(N) and is_subgroup(H, G) and get_order(H) == get_order(G)
    return not Q

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(h1_check(G, N, H))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(h2_check(G, N, H))
    except Exception:
        h2 = False
        
    try:
        neg_q = bool(neg_q_check(G, N, H))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is an abelian normal subgroup of G",
    "H_2: H is a subgroup of G such that G is the internal semidirect product of N and H",
    "¬Q: N is not the trivial subgroup or H != G"
]

N_HYP = 2
NEG_Q_INDEX = 2