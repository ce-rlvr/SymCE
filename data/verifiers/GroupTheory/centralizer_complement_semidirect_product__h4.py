import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_elements(grp):
    if hasattr(grp, 'generate') and callable(grp.generate):
        return set(grp.generate())
    elif hasattr(grp, 'elements'):
        el = grp.elements
        if callable(el):
            return set(el())
        return set(el)
    else:
        return set(grp)

def is_subgroup(sub_set, G_set):
    if not sub_set.issubset(G_set): return False
    if not sub_set: return False
    for a in sub_set:
        try:
            inv_a = ~a
        except Exception:
            inv_a = a**-1
        if inv_a not in sub_set: return False
        for b in sub_set:
            if a * b not in sub_set: return False
    return True

def is_normal_subgroup(sub_set, G_set):
    if not is_subgroup(sub_set, G_set): return False
    for g in G_set:
        try:
            inv_g = ~g
        except Exception:
            inv_g = g**-1
        for n in sub_set:
            if g * n * inv_g not in sub_set: return False
    return True

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]
    
    try:
        G_set = get_elements(G)
        N_set = get_elements(N)
        H_set = get_elements(H)
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = is_normal_subgroup(N_set, G_set) and is_subgroup(H_set, G_set)
    except Exception:
        h1_ok = False
        
    try:
        intersection = N_set.intersection(H_set)
        id_elements = {e for e in intersection if e * e == e}
        h2_ok = len(intersection) == 1 and len(id_elements) == 1 and len(N_set) * len(H_set) == len(G_set)
    except Exception:
        h2_ok = False
        
    try:
        C_G_H = {g for g in G_set if all(g * h == h * g for h in H_set)}
        C_N_H = {n for n in N_set if all(n * h == h * n for h in H_set)}
        Z_H = {h for h in H_set if all(h * x == x * h for x in H_set)}
        
        int_CZ = C_N_H.intersection(Z_H)
        cond1 = len(int_CZ) == 1 and list(int_CZ)[0] * list(int_CZ)[0] == list(int_CZ)[0]
        
        cond2 = all(n * h == h * n for n in C_N_H for h in Z_H)
        
        product_set = {n * h for n in C_N_H for h in Z_H}
        cond3 = product_set == C_G_H
        
        is_direct_product = cond1 and cond2 and cond3
        neg_q_ok = not is_direct_product
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G, and H is a subgroup of G",
    "H_2: G is the internal semidirect product of N and H",
    "¬Q: C_G(H) is not equal to the internal direct product C_N(H) x Z(H)"
]

N_HYP = 2
NEG_Q_INDEX = 2