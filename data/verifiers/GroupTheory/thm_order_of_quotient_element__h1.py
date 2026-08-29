import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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

def conditions(witness):
    try:
        G, N, g = witness
    except Exception:
        return [False, False, False]
    
    # H_1: N is a normal subgroup of G
    try:
        h1 = hasattr(N, 'is_normal') and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h1 = False
        
    # H_2: g is an element of G with finite order k
    try:
        h2 = g in G and hasattr(g, 'order') and g.order() > 0
    except Exception:
        h2 = False
        
    # ¬Q: The order of the coset gN in the quotient group G/N does NOT divide k
    try:
        k = g.order()
        m = 1
        while (g**m) not in N:
            m += 1
        neg_q = (k % m != 0)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: g is an element of G with finite order k",
    "¬Q: The order of the coset gN in G/N does not divide k"
]

N_HYP = 2
NEG_Q_INDEX = 2