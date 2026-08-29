import sympy
from sympy import Matrix, zeros, eye
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: x and y are nilpotent elements in R",
    "¬Q: The product xy is not a nilpotent element"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_nilpotent(m):
    try:
        if hasattr(m, 'is_Matrix') and m.is_Matrix:
            n = m.shape[0]
            zero_mat = zeros(n, n)
            mn = m**n
            if mn == zero_mat:
                return True
            return sympy.simplify(mn) == zero_mat
        else:
            for k in range(1, 11):
                mk = m**k
                if mk == 0:
                    return True
                if hasattr(mk, 'is_zero') and mk.is_zero:
                    return True
            return False
    except Exception:
        return False

def not_nilpotent(m):
    try:
        if hasattr(m, 'is_Matrix') and m.is_Matrix:
            n = m.shape[0]
            zero_mat = zeros(n, n)
            mn = m**n
            if mn == zero_mat:
                return False
            return sympy.simplify(mn) != zero_mat
        else:
            for k in range(1, 11):
                mk = m**k
                if mk == 0:
                    return False
                if hasattr(mk, 'is_zero') and mk.is_zero:
                    return False
            return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, x, y = witness
            elif len(witness) == 2:
                x, y = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    # H_1: R is a ring (x and y are elements of a ring)
    try:
        h1 = False
        if hasattr(x, 'is_Matrix') and x.is_Matrix:
            if hasattr(y, 'is_Matrix') and y.is_Matrix:
                if x.shape == y.shape and x.shape[0] == x.shape[1]:
                    h1 = True
        else:
            _ = x + y
            _ = x * y
            _ = x - y
            h1 = True
    except Exception:
        h1 = False

    # H_2: x and y are nilpotent elements in R
    try:
        h2 = is_nilpotent(x) and is_nilpotent(y)
    except Exception:
        h2 = False

    # ¬Q: The product xy is not a nilpotent element
    try:
        xy = x * y
        neg_q = not_nilpotent(xy)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]