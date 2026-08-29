import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not hasattr(witness, 'shape') or len(witness.shape) != 2:
            return [False, False, False]
        n, m = witness.shape
        if n != m:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(witness.is_symmetric())
    except Exception:
        h1 = False

    try:
        h2 = witness.is_positive_definite
        if h2 is None:
            h2 = all((val.is_positive == True) for val in witness.eigenvals().keys())
        else:
            h2 = bool(h2)
    except Exception:
        h2 = False

    try:
        neg_q = bool(witness != eye(n))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q is symmetric",
    "H_2: Q is positive definite",
    "¬Q: Q is not the identity matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2