import math
import itertools
import functools
import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, H, p = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = False
        p_val = int(p)
        if p_val >= 2 and p_val == p and isprime(p_val):
            if isinstance(H, PermutationGroup) and H.is_subgroup(G):
                order_H = H.order()
                curr = 1
                while curr < order_H:
                    curr *= p_val
                if curr == order_H:
                    h2 = True
    except Exception:
        h2 = False
        
    try:
        neg_q = False
        if h1 and h2:
            order_G = G.order()
            order_H = H.order()
            index_G_H = order_G // order_H
            
            H_elements = set(H.generate())
            H_gens = H.generators
            norm_count = 0
            
            for g in G.generate():
                normalizes = True
                for h in H_gens:
                    conj = g * h * (~g)
                    if conj not in H_elements:
                        normalizes = False
                        break
                if normalizes:
                    norm_count += 1
            
            index_N_H = norm_count // order_H
            
            if (index_G_H % p_val) != (index_N_H % p_val):
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a p-subgroup of G",
    "not Q: index of H in G is not congruent to index of H in N_G(H) modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2