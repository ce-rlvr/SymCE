import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def get_elements(G):
    if hasattr(G, 'elements'):
        return list(G.elements)
    return list(G)

def conditions(witness) -> list[bool]:
    try:
        G, x, g = witness
    except Exception:
        return [False, False]
        
    try:
        elements = get_elements(G)
        h1 = (x in elements) and (g in elements)
    except Exception:
        h1 = False
        
    try:
        elements = get_elements(G)
        
        # C_G(x)
        cg_x = []
        for h in elements:
            if h * x == x * h:
                cg_x.append(h)
                
        # g C_G(x) g^-1
        g_inv = g**-1
        g_cg_x_g_inv = []
        for h in cg_x:
            g_cg_x_g_inv.append(g * h * g_inv)
            
        # g x g^-1
        gxg_inv = g * x * g_inv
        
        # C_G(g x g^-1)
        cg_gxg_inv = []
        for h in elements:
            if h * gxg_inv == gxg_inv * h:
                cg_gxg_inv.append(h)
                
        def is_subset(list1, list2):
            for item1 in list1:
                if item1 not in list2:
                    return False
            return True
            
        # The conclusion is that the two sets are equal.
        # The negated conclusion is that they are NOT equal.
        neg_q = not (is_subset(g_cg_x_g_inv, cg_gxg_inv) and is_subset(cg_gxg_inv, g_cg_x_g_inv))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and g are elements of G",
    "¬Q: C_G(gxg^{-1}) is not equal to g C_G(x) g^{-1}"
]

N_HYP = 1
NEG_Q_INDEX = 1