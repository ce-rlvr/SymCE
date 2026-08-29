import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.matrices import eye, zeros, Matrix
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: x is an element of X",
    "H_3: x is fixed by g",
    "H_4: x is fixed by h",
    "¬Q: The element x is not fixed by the commutator of g and h"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            G, x, g, h = witness
            X = None
        elif len(witness) == 5:
            G, X, x, g, h = witness
        else:
            return [False] * 5
    except Exception:
        return [False] * 5

    try:
        h1 = bool(g in G and h in G)
    except Exception:
        h1 = False

    try:
        if X is not None:
            h2 = bool(x in X)
        else:
            h2 = True
    except Exception:
        h2 = False

    try:
        if hasattr(g, '__call__') and not isinstance(g, sympy.MatrixBase):
            h3 = bool(g(x) == x)
        else:
            h3 = bool(g * x == x)
    except Exception:
        h3 = False

    try:
        if hasattr(h, '__call__') and not isinstance(h, sympy.MatrixBase):
            h4 = bool(h(x) == x)
        else:
            h4 = bool(h * x == x)
    except Exception:
        h4 = False

    try:
        try:
            g_inv = g**-1
        except Exception:
            g_inv = ~g
        try:
            h_inv = h**-1
        except Exception:
            h_inv = ~h
            
        comm = g_inv * h_inv * g * h
        
        if hasattr(comm, '__call__') and not isinstance(comm, sympy.MatrixBase):
            neg_q = bool(comm(x) != x)
        else:
            neg_q = bool(comm * x != x)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]