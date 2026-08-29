import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import PermutationGroup
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
        G, x, z = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1_ok = isinstance(G, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: x is an element of G (and z must also be in G for the expressions to be valid)
    try:
        h2_ok = (x in G) and (z in G)
    except Exception:
        h2_ok = False

    # ¬Q: The conjugacy class of zx is NOT equal to {zy | y is conjugate to x in G}
    try:
        if not (h1_ok and h2_ok):
            neg_q_ok = False
        else:
            elements = list(G.elements)
            
            # Conjugacy class of x
            C_x = set()
            for g in elements:
                C_x.add(g * x * g**-1)
                
            # Conjugacy class of zx
            C_zx = set()
            zx = z * x
            for g in elements:
                C_zx.add(g * zx * g**-1)
                
            # Set {zy | y is conjugate to x in G}
            S = set()
            for y in C_x:
                S.add(z * y)
                
            neg_q_ok = (C_zx != S)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: x is an element of G",
    "¬Q: The conjugacy class of zx is not equal to {zy | y is conjugate to x in G}"
]

N_HYP = 2
NEG_Q_INDEX = 2