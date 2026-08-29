import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    try:
        G, H = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: index of H in G is 2
    try:
        elements_H = set(H.elements) if hasattr(H, 'elements') else set(H)
        elements_G = set(G.elements)
        
        if not elements_H.issubset(elements_G):
            h2 = False
        elif len(elements_H) == 0:
            h2 = False
        else:
            if len(elements_G) == 2 * len(elements_H):
                h2 = True
            else:
                h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: H is not a normal subgroup of G OR G/H is not isomorphic to Z_2
    try:
        elements_H = set(H.elements) if hasattr(H, 'elements') else set(H)
        elements_G = set(G.elements)
        
        if not elements_H.issubset(elements_G) or len(elements_H) == 0:
            is_normal_subgroup = False
        else:
            has_id = any((h * h == h) for h in elements_H)
            if not has_id:
                is_subgroup = False
            else:
                is_subgroup = True
                for a in elements_H:
                    for b in elements_H:
                        if a * ~b not in elements_H:
                            is_subgroup = False
                            break
                    if not is_subgroup:
                        break
            
            if not is_subgroup:
                is_normal_subgroup = False
            else:
                is_normal_subgroup = True
                for g in elements_G:
                    for h in elements_H:
                        if g * h * ~g not in elements_H:
                            is_normal_subgroup = False
                            break
                    if not is_normal_subgroup:
                        break
                        
        neg_q = not is_normal_subgroup
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: index of H in G is 2",
    "¬Q: H is not a normal subgroup of G or G/H is not isomorphic to Z_2"
]

N_HYP = 2
NEG_Q_INDEX = 2