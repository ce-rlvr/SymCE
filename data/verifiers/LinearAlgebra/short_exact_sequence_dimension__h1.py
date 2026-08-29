import sympy
from sympy import oo, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_fin_dim(x):
    if x == oo:
        return False
    if hasattr(x, 'shape'):
        return True
    try:
        val = float(x)
        return val >= 0 and val != float('inf')
    except Exception:
        return False

def get_dim(x):
    if hasattr(x, 'columnspace'):
        return len(x.columnspace())
    if hasattr(x, 'shape'):
        return x.shape[1]
    return x

def conditions(witness):
    try:
        U, V, W = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = is_fin_dim(U)
    except Exception:
        h1 = False

    try:
        h2 = is_fin_dim(W)
    except Exception:
        h2 = False

    try:
        if not is_fin_dim(V):
            q = False
        else:
            q = (get_dim(V) == get_dim(U) + get_dim(W))
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: U is finite-dimensional",
    "H_2: W is finite-dimensional",
    "¬Q: V is not finite-dimensional or dim(V) != dim(U) + dim(W)"
]

N_HYP = 2
NEG_Q_INDEX = 2