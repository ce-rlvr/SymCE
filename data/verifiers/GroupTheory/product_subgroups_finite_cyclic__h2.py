import math
import itertools
import functools
import z3
import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
        G, H, K = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(G.is_cyclic)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(K.is_subgroup(G))
    except Exception:
        h2 = False
        
    try:
        if hasattr(H, 'generate'):
            H_elements = list(H.generate())
            H_order = H.order()
        else:
            H_elements = list(H)
            H_order = len(H_elements)
            
        if hasattr(K, 'generate'):
            K_elements = list(K.generate())
            K_order = K.order()
        else:
            K_elements = list(K)
            K_order = len(K_elements)
            
        HK = set()
        for h in H_elements:
            for k in K_elements:
                HK.add(h * k)
                
        lcm_val = sympy.lcm(H_order, K_order)
        neg_q = (len(HK) != lcm_val)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "H_2: K is a subgroup of G",
    "¬Q: The order of the product HK is not equal to lcm(|H|, |K|)"
]

N_HYP = 2
NEG_Q_INDEX = 2