import sympy
from sympy import eye, zeros, MatrixBase, Abs, simplify, I, Matrix
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            U = witness.get('U')
            lam = witness.get('lambda', witness.get('lam'))
        else:
            U, lam = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(U, MatrixBase) and U.is_square and U.shape[0] > 0
    except Exception:
        h1 = False

    try:
        if h1:
            diff = U.H * U - eye(U.shape[0])
            h2 = all(simplify(diff[i, j]) == 0 for i in range(U.shape[0]) for j in range(U.shape[1]))
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if isinstance(lam, MatrixBase):
            neg_q = False
        else:
            val = simplify(Abs(lam))
            if hasattr(val, 'is_number') and val.is_number:
                neg_q = bool(val != 1)
            elif isinstance(val, (int, float, complex)):
                neg_q = bool(val != 1)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a complex inner product space",
    "H_2: U is a unitary operator on V",
    "¬Q: The absolute value of lambda is not equal to 1"
]

N_HYP = 2
NEG_Q_INDEX = 2