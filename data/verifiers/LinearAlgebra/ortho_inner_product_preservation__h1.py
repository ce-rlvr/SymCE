import sympy
from sympy import Matrix, eye, zeros
import math
import itertools
import functools

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            Q = witness['Q']
            x = witness['x']
            y = witness['y']
        else:
            Q, x, y = witness
            
        if isinstance(Q, (list, tuple)):
            Q = Matrix(Q)
        if isinstance(x, (list, tuple)):
            x = Matrix(x)
        if isinstance(y, (list, tuple)):
            y = Matrix(y)
    except Exception:
        return [False, False, False]

    try:
        h1 = hasattr(x, 'shape') and len(x.shape) == 2 and x.shape[1] == 1
        if h1:
            for i in range(x.shape[0]):
                if x[i, 0].is_real is False:
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        h2 = hasattr(y, 'shape') and len(y.shape) == 2 and y.shape[1] == 1
        if h2 and hasattr(x, 'shape') and len(x.shape) == 2:
            if y.shape[0] != x.shape[0]:
                h2 = False
        if h2:
            for i in range(y.shape[0]):
                if y[i, 0].is_real is False:
                    h2 = False
                    break
    except Exception:
        h2 = False

    try:
        if not (hasattr(Q, 'shape') and len(Q.shape) == 2 and Q.shape[0] == Q.shape[1]):
            neg_q = False
        elif hasattr(x, 'shape') and len(x.shape) == 2 and Q.shape[1] != x.shape[0]:
            neg_q = False
        else:
            lhs = (Q * x).T * (Q * y)
            rhs = x.T * y
            diff = sympy.simplify(lhs[0, 0] - rhs[0, 0])
            neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is a column vector in R^n",
    "H_2: y is a column vector in R^n",
    "¬Q: (Qx)^T (Qy) is not equal to x^T y"
]

N_HYP = 2
NEG_Q_INDEX = 2