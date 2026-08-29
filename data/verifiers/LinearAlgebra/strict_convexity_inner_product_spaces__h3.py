import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        x, y = witness
    except Exception:
        return [False, False, False]

    # H_1: x and y are vectors in an inner product space
    # We represent vectors as column matrices of the same dimension.
    try:
        h1 = (isinstance(x, Matrix) and isinstance(y, Matrix) and 
              x.shape == y.shape and x.shape[1] == 1)
    except Exception:
        h1 = False

    # H_2: ||x|| = 1 and ||y|| = 1
    try:
        h2 = (sympy.simplify(x.norm() - 1) == 0 and 
              sympy.simplify(y.norm() - 1) == 0)
    except Exception:
        h2 = False

    # ¬Q: ||(x+y)/2|| >= 1
    try:
        norm_avg = ((x + y) / 2).norm()
        neg_q = bool(sympy.simplify(norm_avg) >= 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are vectors in an inner product space",
    "H_2: ||x|| = 1 and ||y|| = 1",
    "¬Q: ||(x+y)/2|| >= 1"
]

N_HYP = 2
NEG_Q_INDEX = 2