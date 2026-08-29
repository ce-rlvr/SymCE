import sympy
from sympy import Matrix, eye, zeros, I

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, Matrix) and witness.is_square
    except Exception:
        h1 = False

    try:
        if h1:
            h2 = (witness * witness.H == witness.H * witness)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1:
            neg_q = (witness != witness.H)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional complex inner product space",
    "H_2: T is a normal operator on V",
    "¬Q: T is not a self-adjoint operator"
]

N_HYP = 2
NEG_Q_INDEX = 2