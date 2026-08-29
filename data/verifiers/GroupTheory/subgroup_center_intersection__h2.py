import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
        G, H = witness
        H = list(H)
    except Exception:
        return [False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
        if h1:
            h1 = all(h in G for h in H)
    except Exception:
        h1 = False
        
    # neg_Q: H \cap Z(G) is NOT a subgroup of Z(H)
    try:
        Z_G = G.center()
        H_cap_ZG = [x for x in H if x in Z_G]
        Z_H = [x for x in H if all(x * y == y * x for y in H)]
        
        is_subset = all(x in Z_H for x in H_cap_ZG)
        
        is_subgrp = True
        if not H_cap_ZG:
            is_subgrp = False
        elif not any(x.is_Identity for x in H_cap_ZG):
            is_subgrp = False
        else:
            for a in H_cap_ZG:
                if ~a not in H_cap_ZG:
                    is_subgrp = False
                    break
                for b in H_cap_ZG:
                    if a * b not in H_cap_ZG:
                        is_subgrp = False
                        break
                if not is_subgrp:
                    break
                    
        neg_q = not (is_subset and is_subgrp)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "¬Q: H ∩ Z(G) is not a subgroup of Z(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1