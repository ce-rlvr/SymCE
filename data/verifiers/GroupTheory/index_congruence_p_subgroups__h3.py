import sympy
import sympy.combinatorics
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
from sympy.abc import x, y, z
import math
import itertools
import functools
import z3

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, H, p = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = False
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            h1 = True
            for gen in H.generators:
                if not G.contains(gen):
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    try:
        norm_elements_count = 0
        h_gens = H.generators
        for g in G.generate():
            is_in_norm = True
            for h in h_gens:
                conj = g * h * (~g)
                if not H.contains(conj):
                    is_in_norm = False
                    break
            if is_in_norm:
                norm_elements_count += 1
        
        N_G_H_order = norm_elements_count
        H_order = H.order()
        G_order = G.order()
        
        index_G_H = G_order // H_order
        index_N_H = N_G_H_order // H_order
        
        neg_q = (index_G_H % p) != (index_N_H % p)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group and H is a subgroup of G",
    "H_2: p is a prime number",
    "¬Q: Index of H in G is not congruent to index of H in N_G(H) mod p"
]

N_HYP = 2
NEG_Q_INDEX = 2