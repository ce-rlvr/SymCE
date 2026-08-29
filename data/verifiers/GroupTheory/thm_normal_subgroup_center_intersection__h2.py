import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]
    
    # H1: G is a nilpotent group
    try:
        is_nilp = G.is_nilpotent
        if callable(is_nilp):
            is_nilp = is_nilp()
        h1 = bool(is_nilp)
    except Exception:
        h1 = False

    # H2: N is not the trivial group (and is a subgroup of G)
    try:
        is_sub = N.is_subgroup(G)
        if callable(is_sub):
            is_sub = is_sub()
        
        order_N = N.order
        if callable(order_N):
            order_N = order_N()
            
        h2 = bool(is_sub and order_N > 1)
    except Exception:
        h2 = False

    # neg_Q: The intersection of N and Z(G) is the trivial group
    try:
        Z = G.center
        if callable(Z):
            Z = Z()
            
        try:
            elements = list(N.generate())
        except Exception:
            elements = list(N.elements)
            
        intersection_size = 0
        for g in elements:
            if g in Z:
                intersection_size += 1
                if intersection_size > 1:
                    break
        
        neg_q = (intersection_size == 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "H_2: N is a non-trivial subgroup of G",
    "¬Q: The intersection of N and Z(G) is the trivial group"
]

N_HYP = 2
NEG_Q_INDEX = 2