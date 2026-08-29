import sympy as sp
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero(val):
    if val == 0:
        return True
    try:
        if hasattr(val, 'is_zero_matrix') and val.is_zero_matrix:
            return True
    except Exception:
        pass
    try:
        if hasattr(val, 'is_zero') and val.is_zero:
            return True
    except Exception:
        pass
    try:
        from sympy import MatrixBase
        if isinstance(val, MatrixBase):
            for i in range(val.rows):
                for j in range(val.cols):
                    if not is_zero(val[i, j]):
                        return False
            return True
    except Exception:
        pass
    return False

def get_identity(val):
    try:
        from sympy import MatrixBase, eye
        if isinstance(val, MatrixBase):
            if val.rows == val.cols:
                return eye(val.rows)
    except Exception:
        pass
    return 1

def is_identity(val):
    if val == 1:
        return True
    try:
        if hasattr(val, 'is_Identity') and val.is_Identity:
            return True
    except Exception:
        pass
    try:
        from sympy import MatrixBase, eye
        if isinstance(val, MatrixBase):
            if val.rows == val.cols:
                return val == eye(val.rows)
    except Exception:
        pass
    try:
        if is_zero(val - 1):
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # H_1: x is an element of R
    try:
        x_val, n_val = witness
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: n is a positive integer such that x^n = 0
    try:
        x_val, n_val = witness
        if isinstance(n_val, int) and n_val > 0:
            xn = x_val**n_val
            h2_ok = is_zero(xn)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: 1 - x is not invertible in R, or its inverse is not \sum_{i=0}^{n-1} x^i
    try:
        x_val, n_val = witness
        
        I = get_identity(x_val)
        
        try:
            one_minus_x = I - x_val
        except Exception:
            neg_q_ok = True
            return [h1_ok, h2_ok, neg_q_ok]
            
        try:
            S = x_val**0
            for i in range(1, n_val):
                S = S + x_val**i
        except Exception:
            neg_q_ok = True
            return [h1_ok, h2_ok, neg_q_ok]
            
        try:
            prod1 = one_minus_x * S
            prod2 = S * one_minus_x
        except Exception:
            neg_q_ok = True
            return [h1_ok, h2_ok, neg_q_ok]
            
        if is_identity(prod1) and is_identity(prod2):
            neg_q_ok = False
        else:
            neg_q_ok = True
            
    except Exception:
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x is an element of R",
    "H_2: n is a positive integer such that x^n = 0",
    "¬Q: 1 - x is not invertible in R, or its inverse is not \\sum_{i=0}^{n-1} x^i"
]

N_HYP = 2
NEG_Q_INDEX = 2