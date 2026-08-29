import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import a, b, c, x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        x_val, y_val = witness
    except Exception:
        return [False, False]
    
    try:
        _ = x_val + y_val
        _ = x_val * y_val
        h1 = True
    except Exception:
        h1 = False
        
    try:
        res = x_val * y_val * (x_val + y_val)
        if hasattr(res, 'is_zero_matrix'):
            neg_q = not res.is_zero_matrix
        elif hasattr(res, 'is_zero') and res.is_zero is not None:
            neg_q = not res.is_zero
        else:
            try:
                neg_q = bool(sympy.simplify(res) != 0)
            except Exception:
                neg_q = bool(res != 0)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of R",
    "¬Q: x y (x + y) != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1