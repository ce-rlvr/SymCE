import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def direct_product(H, K):
    deg_H = H.degree
    deg_K = K.degree
    gens = []
    for h in H.generators:
        if h.is_Identity:
            continue
        p = [h(i) for i in range(deg_H)] + list(range(deg_H, deg_H + deg_K))
        gens.append(Permutation(p))
    for k in K.generators:
        if k.is_Identity:
            continue
        p = list(range(deg_H)) + [k(i) + deg_H for i in range(deg_K)]
        gens.append(Permutation(p))
    if not gens:
        return PermutationGroup([Permutation(max(0, deg_H + deg_K - 1))])
    return PermutationGroup(gens)

def quotient_group(G, H):
    H_els = set(H.elements)
    G_els = list(G.elements)
    cosets = []
    seen = set()
    for g in G_els:
        if g not in seen:
            coset = frozenset(g * h for h in H_els)
            cosets.append(coset)
            seen.update(coset)
            
    cosets = list(cosets)
    element_to_coset = {}
    for i, c in enumerate(cosets):
        for x in c:
            element_to_coset[x] = i
            
    gens = []
    for g in G.generators:
        p = []
        for i, c in enumerate(cosets):
            rep = next(iter(c))
            target = g * rep
            p.append(element_to_coset[target])
        gens.append(Permutation(p))
        
    if not gens:
        return PermutationGroup([Permutation(max(0, len(cosets)-1))])
    return PermutationGroup(gens)

def conditions(witness):
    try:
        G, H, K = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: H and K are normal subgroups of G
    try:
        h_sub = all(h in G for h in H.generators)
        k_sub = all(k in G for k in K.generators)
        
        h_normal = True
        if h_sub:
            for g in G.generators:
                for h in H.generators:
                    if (g * h * ~g) not in H:
                        h_normal = False
                        break
                if not h_normal: break
        else:
            h_normal = False
            
        k_normal = True
        if k_sub:
            for g in G.generators:
                for k in K.generators:
                    if (g * k * ~g) not in K:
                        k_normal = False
                        break
                if not k_normal: break
        else:
            k_normal = False
            
        H1 = h_normal and k_normal
    except Exception:
        H1 = False

    # H2: H ∩ K = {e}
    try:
        H_els = set(H.elements)
        K_els = set(K.elements)
        intersection = H_els.intersection(K_els)
        H2 = (len(intersection) == 1)
    except Exception:
        H2 = False

    # H3: HK = G
    try:
        HK_els = set(h * k for h in H_els for k in K_els)
        G_els = set(G.elements)
        H3 = (HK_els == G_els)
    except Exception:
        H3 = False

    # neg_Q: not (G ≅ H × K and G/H ≅ K)
    try:
        HxK = direct_product(H, K)
        G_mod_H = quotient_group(G, H)
        
        iso1 = G.is_isomorphic(HxK)
        iso2 = G_mod_H.is_isomorphic(K)
        
        Q = iso1 and iso2
        neg_Q = not Q
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: H and K are normal subgroups of G",
    "H_2: H ∩ K = {e}",
    "H_3: HK = G",
    "¬Q: G is not isomorphic to H × K or G/H is not isomorphic to K"
]

N_HYP = 3
NEG_Q_INDEX = 3