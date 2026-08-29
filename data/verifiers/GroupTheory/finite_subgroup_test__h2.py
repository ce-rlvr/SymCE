import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: H is finite
    try:
        # H must be a finite collection and a subset of G
        h2 = isinstance(H, (list, set, tuple)) and all(h in G for h in H)
    except Exception:
        h2 = False
        
    # H_3: For all a, b \in H, the product ab is in H
    try:
        h3 = True
        H_list = list(H)
        for a in H_list:
            for b in H_list:
                if a * b not in H_list:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False
        
    # neg_Q: H is not a subgroup of G
    try:
        H_list = list(H)
        is_subset = all(h in G for h in H_list)
        is_non_empty = len(H_list) > 0
        
        is_closed_mult = True
        for a in H_list:
            for b in H_list:
                if a * b not in H_list:
                    is_closed_mult = False
                    break
            if not is_closed_mult:
                break
                
        is_closed_inv = True
        for a in H_list:
            if a**-1 not in H_list:
                is_closed_inv = False
                break
                
        is_subgroup = is_subset and is_non_empty and is_closed_mult and is_closed_inv
        neg_q = not is_subgroup
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is finite",
    "H_3: For all a, b in H, the product ab is in H",
    "¬Q: H is not a subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3