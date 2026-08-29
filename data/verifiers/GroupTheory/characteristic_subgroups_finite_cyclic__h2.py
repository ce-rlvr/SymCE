import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def is_group(G):
    return hasattr(G, 'generators') and hasattr(G, 'order')

def check_is_cyclic(G):
    try:
        if hasattr(G, 'is_cyclic') and G.is_cyclic is not None:
            return bool(G.is_cyclic)
        
        order = G.order
        if callable(order):
            order = order()
            
        for g in G.elements:
            g_order = g.order
            if callable(g_order):
                g_order = g_order()
            if g_order == order:
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = False
        if is_group(G):
            h1 = check_is_cyclic(G)
    except Exception:
        h1 = False
        
    try:
        is_subgroup = False
        if is_group(H) and is_group(G):
            try:
                is_subgroup = all(g in G for g in H.generators)
            except Exception:
                is_subgroup = False
                
        if not is_subgroup:
            is_characteristic = False
        else:
            is_characteristic = True
            
        neg_q = not is_characteristic
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite cyclic group",
    "¬Q: H is not a characteristic subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1