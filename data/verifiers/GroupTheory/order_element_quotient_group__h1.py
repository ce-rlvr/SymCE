import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        G, N, g = witness
    except Exception:
        return [False, False, False]
    
    # H_1: N is a normal subgroup of G
    try:
        h1 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h1 = False
        
    # H_2: g \in G is an element of finite order
    try:
        h2 = bool(g in G and g.order() > 0)
    except Exception:
        h2 = False
        
    # ¬Q: The order of the coset gN in G/N does NOT divide the order of g in G
    try:
        order_g = g.order()
        k = 1
        curr = g
        max_k = order_g + 100
        
        # Find the order of the coset gN, which is the smallest k >= 1 such that g^k \in N
        while curr not in N and k <= max_k:
            curr = curr * g
            k += 1
            
        if curr in N:
            neg_q = bool(order_g % k != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: g in G is an element of finite order",
    "¬Q: The order of the coset gN in G/N does not divide the order of g in G"
]

N_HYP = 2
NEG_Q_INDEX = 2