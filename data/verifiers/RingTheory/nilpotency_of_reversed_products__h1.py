import sympy
from sympy import eye, zeros, Rational, Integer
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
    """Safely check if a mathematical object is zero."""
    if isinstance(val, (int, float)):
        return val == 0
    if hasattr(val, 'is_zero_matrix'):
        return val.is_zero_matrix
    if hasattr(val, 'is_zero') and val.is_zero is not None:
        return val.is_zero
    try:
        eq = (val == 0)
        if isinstance(eq, bool):
            return eq
        if hasattr(eq, 'all'):
            return bool(eq.all())
    except Exception:
        pass
    if isinstance(val, sympy.Expr):
        try:
            if sympy.simplify(val) == 0:
                return True
        except Exception:
            pass
    return False

def is_nilpotent(val, max_power=50):
    """Check if an element is nilpotent (val^n == 0 for some n > 0)."""
    if is_zero(val):
        return True
    
    # Try using the ** operator
    try:
        for i in range(1, max_power + 1):
            if is_zero(val**i):
                return True
    except Exception:
        pass
        
    # Try repeated right multiplication (for non-associative or custom objects)
    try:
        curr = val
        for i in range(1, max_power + 1):
            curr = curr * val
            if is_zero(curr):
                return True
    except Exception:
        pass

    # Try repeated left multiplication
    try:
        curr = val
        for i in range(1, max_power + 1):
            curr = val * curr
            if is_zero(curr):
                return True
    except Exception:
        pass
        
    return False

def conditions(witness):
    """
    Given a witness (typically a tuple of two elements x and y),
    evaluate the hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, dict):
            x_elem = witness['x']
            y_elem = witness['y']
        else:
            x_elem, y_elem = witness
    except Exception:
        return [False, False, False]

    # H_1: x and y are elements of R
    # We verify this by checking if they support the ring multiplication operation.
    try:
        _ = x_elem * y_elem
        _ = y_elem * x_elem
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: xy is a nilpotent element
    try:
        xy = x_elem * y_elem
        h2_ok = is_nilpotent(xy)
    except Exception:
        h2_ok = False

    # neg_Q: yx is NOT a nilpotent element
    try:
        yx = y_elem * x_elem
        neg_q_ok = not is_nilpotent(yx)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x and y are elements of R",
    "H_2: xy is a nilpotent element",
    "¬Q: yx is not a nilpotent element"
]

N_HYP = 2
NEG_Q_INDEX = 2