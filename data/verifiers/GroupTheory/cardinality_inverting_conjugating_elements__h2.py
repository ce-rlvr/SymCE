import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import *
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        G, x = witness
    except Exception:
        return [False, False]

    try:
        h1 = getattr(G, 'is_group', False) and getattr(G, 'order', lambda: float('inf'))() < float('inf')
    except Exception:
        h1 = False

    try:
        x_inv = x**-1
        c_g_x_count = 0
        s_count = 0
        for g in G.elements:
            conj = g * x * g**-1
            if conj == x:
                c_g_x_count += 1
            if conj == x_inv:
                s_count += 1
        neg_q = (s_count != 0) and (s_count != c_g_x_count)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The cardinality of S is neither 0 nor |C_G(x)|"
]

N_HYP = 1
NEG_Q_INDEX = 1