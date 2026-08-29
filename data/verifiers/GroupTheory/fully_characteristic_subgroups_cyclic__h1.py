import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

def conditions(witness) -> list[bool]:
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False]
        
    # H_1: H is a subgroup of G
    try:
        elements_G_set = set(G.generate())
        if hasattr(H, "generate"):
            H_set = set(H.generate())
        else:
            H_set = set(H)
            
        is_subset = H_set.issubset(elements_G_set)
        is_nonempty = len(H_set) > 0
        is_closed = all(h1 * h2 in H_set for h1 in H_set for h2 in H_set)
        has_inverses = all(h**-1 in H_set for h in H_set)
        
        h1 = bool(is_subset and is_nonempty and is_closed and has_inverses)
    except Exception:
        h1 = False
        
    # H_2: phi is a group endomorphism of G
    try:
        if callable(phi):
            phi_func = phi
        else:
            phi_func = lambda x: phi[x]
            
        elements_G = list(G.generate())
        elements_G_set = set(elements_G)
        
        maps_to_G = all(phi_func(g) in elements_G_set for g in elements_G)
        if maps_to_G:
            is_hom = all(phi_func(g1 * g2) == phi_func(g1) * phi_func(g2) 
                         for g1 in elements_G for g2 in elements_G)
            h2 = bool(is_hom)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: phi(H) is not a subset of H
    try:
        if callable(phi):
            phi_func = phi
        else:
            phi_func = lambda x: phi[x]
            
        if hasattr(H, "generate"):
            elements_H = list(H.generate())
        else:
            elements_H = list(H)
            
        elements_H_set = set(elements_H)
            
        neg_q = any(phi_func(h) not in elements_H_set for h in elements_H)
        neg_q = bool(neg_q)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: phi is a group endomorphism of G",
    "¬Q: phi(H) is not a subset of H"
]

N_HYP = 2
NEG_Q_INDEX = 2