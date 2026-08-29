import sympy
import sympy.combinatorics
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros
import math
import itertools
import functools

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

def conditions(witness):
    try:
        G, H, K, x = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h2 = False
        
    try:
        h3 = x in G
    except Exception:
        h3 = False
        
    try:
        if hasattr(H, 'generate'):
            H_elems = list(H.generate())
        else:
            H_elems = list(H)
            
        if hasattr(K, 'generate'):
            K_elems = list(K.generate())
        else:
            K_elems = list(K)
            
        HxK = set()
        for h in H_elems:
            for k in K_elems:
                HxK.add(h * x * k)
                
        xKx_inv = set()
        x_inv = ~x
        for k in K_elems:
            xKx_inv.add(x * k * x_inv)
            
        H_set = set(H_elems)
        intersection = H_set.intersection(xKx_inv)
        
        lhs = len(HxK)
        rhs_num = len(H_elems) * len(K_elems)
        rhs_den = len(intersection)
        
        if rhs_den == 0:
            neg_q = True
        else:
            neg_q = (lhs * rhs_den) != rhs_num
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: H is a subgroup of G",
    "H_3: x is an element of G",
    "¬Q: The cardinality of HxK is not equal to |H||K| / |H \\cap xKx^{-1}|"
]

N_HYP = 3
NEG_Q_INDEX = 3