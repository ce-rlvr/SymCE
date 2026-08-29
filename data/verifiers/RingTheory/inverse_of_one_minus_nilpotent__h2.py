import sympy
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_eq(a, b):
    if a == b:
        return True
    try:
        diff = a - b
        if hasattr(diff, 'is_zero') and diff.is_zero:
            return True
        if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix:
            return True
        if diff == 0:
            return True
        if sympy.simplify(diff) == 0:
            return True
    except Exception:
        pass
    return False

def is_in(elem, lst):
    for x in lst:
        if is_eq(elem, x):
            return True
    return False

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (R, x, n) where R is the ring (e.g., a list of elements),
    x is the nilpotent element, and n is the index of nilpotency.
    """
    try:
        R, x, n = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a ring
    try:
        if hasattr(R, 'is_ring') and callable(R.is_ring):
            h1 = bool(R.is_ring())
        else:
            R_list = list(R)
            h1 = True
            for a in R_list:
                for b in R_list:
                    if not is_in(a + b, R_list): h1 = False
                    if not is_in(a - b, R_list): h1 = False
                    if not is_in(a * b, R_list): h1 = False
    except Exception:
        h1 = False
        
    # H_2: n is a positive integer such that x^n = 0
    try:
        try:
            n_val = int(n)
            h2 = (n_val == n) and (n_val > 0)
        except Exception:
            h2 = False
            
        if h2:
            xn = x
            for _ in range(n_val - 1):
                xn = xn * x
                
            if hasattr(R, 'zero'):
                zero_elem = R.zero
            else:
                R_list = list(R)
                zero_elem = None
                for e in R_list:
                    if all(is_eq(e + a, a) and is_eq(a + e, a) for a in R_list):
                        zero_elem = e
                        break
            if zero_elem is not None and is_eq(xn, zero_elem):
                h2 = True
            else:
                h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: 1 - x is not invertible in R, or its inverse is not \sum_{i=0}^{n-1} x^i
    try:
        if hasattr(R, 'identity'):
            identity = R.identity
        else:
            R_list = list(R)
            identity = None
            for e in R_list:
                if all(is_eq(e * a, a) and is_eq(a * e, a) for a in R_list):
                    identity = e
                    break
                    
        if identity is None:
            # R does not have a multiplicative identity, so 1 - x is not defined/invertible in R
            neg_q = True
        else:
            one_minus_x = identity - x
            if hasattr(R, '__contains__'):
                if isinstance(R, (list, tuple, set)):
                    in_R = is_in(one_minus_x, list(R))
                else:
                    in_R = one_minus_x in R
            else:
                in_R = is_in(one_minus_x, R_list)
                
            if not in_R:
                neg_q = True
            else:
                if hasattr(R, 'inverse'):
                    inv = R.inverse(one_minus_x)
                else:
                    if hasattr(R, 'elements'):
                        elements = R.elements
                    else:
                        elements = R_list
                        
                    inv = None
                    for e in elements:
                        if is_eq(one_minus_x * e, identity) and is_eq(e * one_minus_x, identity):
                            inv = e
                            break
                if inv is None:
                    neg_q = True
                else:
                    n_val = int(n)
                    inv_sum = identity
                    term = identity
                    for i in range(1, n_val):
                        term = term * x
                        inv_sum = inv_sum + term
                    if not is_eq(inv, inv_sum):
                        neg_q = True
                    else:
                        neg_q = False
    except Exception:
        # If any operation fails (e.g., identity - x raises an error), 
        # it means 1 - x is not well-defined in R, so it's not invertible in R.
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: n is a positive integer such that x^n = 0",
    "¬Q: 1 - x is not invertible in R, or its inverse is not \\sum_{i=0}^{n-1} x^i"
]

N_HYP = 2
NEG_Q_INDEX = 2