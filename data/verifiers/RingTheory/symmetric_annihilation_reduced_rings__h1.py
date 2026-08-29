import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
O2 = zeros(2)
I3 = eye(3)
O3 = zeros(3)

def is_zero_element(obj):
    if isinstance(obj, str):
        return False
    try:
        if hasattr(obj, 'is_zero_matrix'):
            return bool(obj.is_zero_matrix)
    except Exception:
        pass
    try:
        if hasattr(obj, 'is_zero') and obj.is_zero is not None:
            return bool(obj.is_zero)
    except Exception:
        pass
    try:
        if hasattr(obj, '__iter__'):
            return all(is_zero_element(e) for e in obj)
    except Exception:
        pass
    try:
        if sympy.simplify(obj) == 0:
            return True
    except Exception:
        pass
    return obj == 0

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
    except Exception:
        return [False, False, False]
    
    # H_1: a and b are elements of R
    try:
        _ = a + b
        _ = a * b
        _ = b * a
        if hasattr(a, 'shape') and hasattr(b, 'shape'):
            h1 = (a.shape == b.shape) and (len(a.shape) == 2) and (a.shape[0] == a.shape[1])
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: ab = 0
    try:
        prod_ab = a * b
        h2 = is_zero_element(prod_ab)
    except Exception:
        h2 = False

    # ¬Q: ba != 0
    try:
        prod_ba = b * a
        neg_q = not is_zero_element(prod_ba)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are elements of R",
    "H_2: ab = 0",
    "¬Q: ba != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2