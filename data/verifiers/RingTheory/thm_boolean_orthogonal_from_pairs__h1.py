import sympy
from sympy import Matrix, eye, zeros, Rational, Integer, Symbol, simplify, expand
from sympy.abc import a, b, c, d, t, u, v, w, x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_element(val):
    if hasattr(val, 'is_zero_matrix') and val.is_zero_matrix:
        return True
    if hasattr(val, 'is_zero') and val.is_zero:
        return True
    if val == 0:
        return True
    try:
        exp_val = expand(val)
        if hasattr(exp_val, 'is_zero_matrix') and exp_val.is_zero_matrix:
            return True
        if hasattr(exp_val, 'is_zero') and exp_val.is_zero:
            return True
        if exp_val == 0:
            return True
            
        simp_val = simplify(val)
        if hasattr(simp_val, 'is_zero_matrix') and simp_val.is_zero_matrix:
            return True
        if hasattr(simp_val, 'is_zero') and simp_val.is_zero:
            return True
        if simp_val == 0:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False]
        x_val, y_val = witness
    except Exception:
        return [False, False]
    
    try:
        _ = x_val + y_val
        _ = x_val * y_val
        _ = x_val - y_val
        _ = (x_val - x_val * y_val) * (y_val - x_val * y_val)
        h1 = True
    except Exception:
        h1 = False

    try:
        prod = (x_val - x_val * y_val) * (y_val - x_val * y_val)
        neg_q = not is_zero_element(prod)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of R",
    "¬Q: The product (x - x y)(y - x y) is not equal to 0"
]

N_HYP = 1
NEG_Q_INDEX = 1