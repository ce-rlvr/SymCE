import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        u, x = witness
    except Exception:
        return [False, False, False]
    
    # H_1: u is a unit
    try:
        if hasattr(u, 'is_Matrix') and u.is_Matrix:
            h1 = u.is_square and u.det() != 0
        else:
            h1 = (u != 0)
    except Exception:
        h1 = False

    # H_2: x is nilpotent
    try:
        if hasattr(x, 'is_Matrix') and x.is_Matrix:
            h2 = False
            if x.is_square:
                n = x.shape[0]
                h2 = (x**n).is_zero_matrix
        else:
            h2 = (x == 0)
    except Exception:
        h2 = False

    # ¬Q: u + x is not a unit
    try:
        ux = u + x
        if hasattr(ux, 'is_Matrix') and ux.is_Matrix:
            neg_q = ux.is_square and ux.det() == 0
        else:
            neg_q = (ux == 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: u is a unit",
    "H_2: x is nilpotent",
    "¬Q: u + x is not a unit"
]

N_HYP = 2
NEG_Q_INDEX = 2