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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        x, y = witness
    except Exception:
        return [False, False, False]
    
    try:
        _ = x * y
        _ = x**-1
        _ = y**-1
        h1 = True
    except Exception:
        h1 = False

    h2 = True

    try:
        c_xy = (x**-1) * (y**-1) * x * y
        c_yx = (y**-1) * (x**-1) * y * x
        c_xy_inv = c_xy**-1
        
        if hasattr(c_xy_inv, 'equals') and callable(c_xy_inv.equals):
            eq = c_xy_inv.equals(c_yx)
            if eq is None:
                eq = (c_xy_inv == c_yx)
            neg_q = not bool(eq)
        else:
            neg_q = not bool(c_xy_inv == c_yx)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of G",
    "H_2: The commutator is defined as comm(x, y) = x^-1 y^-1 x y",
    "not Q: comm(x, y)^-1 != comm(y, x)"
]

N_HYP = 2
NEG_Q_INDEX = 2