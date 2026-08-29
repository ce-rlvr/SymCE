import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol
import itertools
import functools
import math
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

def is_nilpotent(z, max_k=200):
    def check_zero(val):
        try:
            if val == 0:
                return True
        except Exception:
            pass
        try:
            if hasattr(val, 'is_zero') and val.is_zero:
                return True
        except Exception:
            pass
        try:
            if hasattr(val, 'is_zero_matrix') and val.is_zero_matrix:
                return True
        except Exception:
            pass
        try:
            if isinstance(val, sympy.MatrixBase):
                return val.is_zero_matrix
        except Exception:
            pass
        return False

    if check_zero(z):
        return True
    
    curr = z
    for _ in range(1, max_k):
        try:
            curr = curr * z
            if check_zero(curr):
                return True
        except Exception:
            return False
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, x, y = witness
            elif len(witness) == 2:
                x, y = witness
            else:
                return [False, False, False]
        else:
            x, y = witness.x, witness.y
    except Exception:
        return [False, False, False]
    
    try:
        # Check if x and y belong to a ring-like structure
        _ = x + y
        _ = x - y
        _ = x * y
        _ = y * x
        h1 = True
    except Exception:
        h1 = False

    try:
        xy = x * y
        h2 = is_nilpotent(xy)
    except Exception:
        h2 = False

    try:
        yx = y * x
        neg_q = not is_nilpotent(yx)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: xy is a nilpotent element",
    "¬Q: yx is not a nilpotent element"
]

N_HYP = 2
NEG_Q_INDEX = 2