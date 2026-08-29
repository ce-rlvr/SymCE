import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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

def conditions(witness) -> list[bool]:
    try:
        G, K, N = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: K is a normal subgroup of G
    try:
        h2 = isinstance(K, PermutationGroup) and K.is_subgroup(G) and K.is_normal(G)
    except Exception:
        h2 = False
        
    # H_3: N is a subset of K
    try:
        if hasattr(N, 'elements'):
            n_elems = list(N.elements)
        else:
            n_elems = list(N)
            
        if hasattr(K, 'elements'):
            k_elems = list(K.elements)
        else:
            k_elems = list(K)
            
        h3 = all(n in k_elems for n in n_elems)
    except Exception:
        h3 = False
        
    # ¬Q: K/N is not a normal subgroup of G/N, or (G/N)/(K/N) is not isomorphic to G/K
    # The conclusion holds if and only if N is a normal subgroup of G, K is a normal subgroup of G, 
    # and N is a subset of K. If any of these fail, the quotient groups are either undefined 
    # or the isomorphism/normality fails.
    try:
        if isinstance(N, PermutationGroup):
            n_is_normal_in_G = N.is_subgroup(G) and N.is_normal(G)
        else:
            n_list = list(N)
            if not n_list:
                n_is_normal_in_G = False
            else:
                N_group = PermutationGroup(n_list)
                # Check if N is exactly the subgroup it generates
                if len(list(N_group.elements)) != len(n_list):
                    n_is_normal_in_G = False
                else:
                    n_is_normal_in_G = N_group.is_subgroup(G) and N_group.is_normal(G)
                    
        conclusion_holds = h2 and h3 and n_is_normal_in_G
        neg_q = not conclusion_holds
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a normal subgroup of G",
    "H_3: N is a subset of K",
    "¬Q: K/N is not a normal subgroup of G/N, or (G/N)/(K/N) is not isomorphic to G/K"
]

N_HYP = 3
NEG_Q_INDEX = 3