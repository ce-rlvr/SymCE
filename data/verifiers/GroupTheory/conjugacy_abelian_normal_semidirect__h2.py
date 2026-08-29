import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
        G, N, H, n1, n2 = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False
        
    # H2: H is a subgroup of G such that G is the internal semidirect product of N and H
    try:
        h2_ok = False
        if isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup):
            if N.is_subgroup(G) and H.is_subgroup(G) and N.is_normal(G):
                NH_gens = list(N.generators) + list(H.generators)
                NH = PermutationGroup(NH_gens)
                if NH.order() == G.order() and N.order() * H.order() == G.order():
                    h2_ok = True
    except Exception:
        h2_ok = False
        
    # H3: n1 and n2 are elements of N
    try:
        h3_ok = (n1 in N) and (n2 in N)
    except Exception:
        h3_ok = False
        
    # ¬Q: n1 and n2 are conjugate in G iff there exists h in H such that h n1 h^-1 = n2
    try:
        conjugate_in_G = False
        for g in G.elements:
            if g * n1 * g**-1 == n2:
                conjugate_in_G = True
                break
                
        conjugate_via_H = False
        for h in H.elements:
            if h * n1 * h**-1 == n2:
                conjugate_via_H = True
                break
                
        neg_q_ok = (conjugate_in_G != conjugate_via_H)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G such that G is the internal semidirect product of N and H",
    "H_3: n1 and n2 are elements of N",
    "¬Q: (n1 and n2 are conjugate in G iff there exists h in H such that h n1 h^-1 = n2) is FALSE"
]

N_HYP = 3
NEG_Q_INDEX = 3