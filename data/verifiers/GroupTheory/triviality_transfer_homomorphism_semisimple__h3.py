import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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

def conjugacy_class(G, g):
    cc = set([g])
    queue = [g]
    while queue:
        curr = queue.pop(0)
        for gen in G.generators:
            conj1 = gen * curr * ~gen
            if conj1 not in cc:
                cc.add(conj1)
                queue.append(conj1)
            conj2 = ~gen * curr * gen
            if conj2 not in cc:
                cc.add(conj2)
                queue.append(conj2)
    return list(cc)

def is_semisimple(G):
    if G.order() == 1:
        return False
    id_perm = G.generators[0] * ~G.generators[0]
    seen_cc = set()
    for g in G.elements:
        if g == id_perm:
            continue
        if g in seen_cc:
            continue
        cc = conjugacy_class(G, g)
        for x in cc:
            seen_cc.add(x)
        N = PermutationGroup(cc)
        if N.is_abelian:
            return False
    return True

def is_sylow_p_subgroup(G, P):
    if not P.is_subgroup(G):
        return False
    order_G = G.order()
    order_P = P.order()
    if order_P == 1:
        return False
    factors = factorint(order_P)
    if len(factors) != 1:
        return False
    p = list(factors.keys())[0]
    index = order_G // order_P
    if index % p == 0:
        return False
    return True

def transfer_homomorphism_image_is_trivial(G, P):
    if G.order() == 1:
        return True
    P_prime = P.derived_subgroup()
    P_prime_elements = set(P_prime.elements)
    
    reps = []
    seen = set()
    P_elements = list(P.elements)
    for g in G.elements:
        if g not in seen:
            reps.append(g)
            for p in P_elements:
                seen.add(g * p)
                
    rep_map = {}
    for x in reps:
        for p in P_elements:
            rep_map[x * p] = x
            
    id_perm = G.generators[0] * ~G.generators[0]
    for g in G.generators:
        v = id_perm
        for x in reps:
            gx = g * x
            y = rep_map[gx]
            h = ~y * gx
            v = v * h
        if v not in P_prime_elements:
            return False
    return True

def conditions(witness):
    try:
        G, P = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_semisimple(G)
    except Exception:
        h1 = False
        
    try:
        h2 = is_sylow_p_subgroup(G, P)
    except Exception:
        h2 = False
        
    try:
        if not P.is_subgroup(G):
            neg_q = False
        else:
            neg_q = not transfer_homomorphism_image_is_trivial(G, P)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a semisimple finite group",
    "H_2: P is a Sylow p-subgroup of G",
    "¬Q: The image of V is not the trivial subgroup of P mod P_prime"
]

N_HYP = 2
NEG_Q_INDEX = 2