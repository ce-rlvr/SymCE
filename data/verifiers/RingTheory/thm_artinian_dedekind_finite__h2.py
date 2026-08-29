import sympy
from sympy import Matrix, eye, zeros, Rational
import sympy.abc

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                R, a, b = witness
            elif len(witness) == 2:
                a, b = witness
            else:
                return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    h1 = False
    ident = None
    try:
        if isinstance(a, Matrix) and isinstance(b, Matrix):
            if a.is_square and b.is_square and a.shape == b.shape:
                h1 = True
                ident = eye(a.shape[0])
        else:
            _ = a * b
            h1 = True
            ident = 1
    except Exception:
        h1 = False

    neg_q = False
    try:
        if h1:
            if isinstance(a, Matrix) and isinstance(b, Matrix):
                neg_q = bool(b * a != ident)
            else:
                diff = sympy.simplify(b * a - ident)
                neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: ba != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1