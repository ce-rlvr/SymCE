import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
        if len(witness) != 2:
            return [False, False]
        G, H = witness
    except Exception:
        return [False, False]
    
    try:
        if hasattr(H, 'is_subgroup'):
            h1 = bool(H.is_subgroup(G))
        elif hasattr(G, 'has_subgroup'):
            h1 = bool(G.has_subgroup(H))
        else:
            h1 = False
    except Exception:
        h1 = False
        
    try:
        if not hasattr(G, 'order') or not hasattr(H, 'order'):
            neg_q = False
        else:
            order_G = G.order() if callable(G.order) else G.order
            order_H = H.order() if callable(H.order) else H.order
            
            if order_H == 0:
                divides = False
            elif order_G in (sympy.oo, math.inf, float('inf')):
                divides = False
            else:
                rem = order_G % order_H
                divides = (rem == 0)
                
            neg_q = not divides
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "¬Q: The order of H does not divide the order of G"
]

N_HYP = 1
NEG_Q_INDEX = 1