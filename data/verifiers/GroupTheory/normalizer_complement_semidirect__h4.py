import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import itertools
import functools
import math

# Top-level setup for potential witness expressions
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

def is_subgroup(sub, G):
    try:
        if not isinstance(sub, PermutationGroup): 
            return False
        return all(G.contains(g) for g in sub.generators)
    except Exception:
        return False

def is_normal(N, G):
    try:
        if not is_subgroup(N, G): 
            return False
        for g in G.generators:
            g_inv = ~g
            for n in N.generators:
                if not N.contains(g * n * g_inv):
                    return False
        return True
    except Exception:
        return False

def normalizer(G, H):
    norm_elements = []
    H_elems = set(H.elements)
    for g in G.elements:
        g_inv = ~g
        if all((g * h * g_inv) in H_elems for h in H.generators):
            norm_elements.append(g)
    return PermutationGroup(norm_elements)

def centralizer_in_N(N, H):
    cent_elements = []
    for n in N.elements:
        n_inv = ~n
        if all((n * h * n_inv) == h for h in H.generators):
            cent_elements.append(n)
    return PermutationGroup(cent_elements)

def conditions(witness):
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = is_subgroup(N, G) and is_normal(N, G)
    except Exception:
        h2 = False
        
    # H_3: H is a subgroup of G
    try:
        h3 = is_subgroup(H, G)
    except Exception:
        h3 = False
        
    # ¬Q: N_G(H) is NOT the internal semidirect product of C_N(H) and H
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            N_G_H = normalizer(G, H)
            C_N_H = centralizer_in_N(N, H)
            
            # For N_G(H) to be the internal semidirect product of C_N(H) and H:
            # 1. C_N(H) intersect H must be trivial
            # 2. C_N(H) * H must equal N_G(H) (checked via orders since intersection is trivial)
            intersect_size = len(set(C_N_H.elements).intersection(set(H.elements)))
            is_semidirect = (intersect_size == 1) and (C_N_H.order() * H.order() == N_G_H.order())
            
            neg_q = not is_semidirect
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "¬Q: N_G(H) is not the internal semidirect product of C_N(H) and H"
]

N_HYP = 3
NEG_Q_INDEX = 3