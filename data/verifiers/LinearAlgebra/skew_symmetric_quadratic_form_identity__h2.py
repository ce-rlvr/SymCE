import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, x = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(A, sympy.MatrixBase) and A.is_square
        if h1:
            for elem in A:
                if not sympy.sympify(elem).is_real:
                    h1 = False
                    break
    except Exception:
        h1 = False

    try:
        h2 = isinstance(x, sympy.MatrixBase) and x.shape == (A.shape[0], 1)
        if h2:
            for elem in x:
                if not sympy.sympify(elem).is_real:
                    h2 = False
                    break
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            quad_form = (x.T * A * x)[0, 0]
            neg_q = bool(sympy.simplify(quad_form) != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n real matrix",
    "H_2: x is a vector in R^n",
    "¬Q: x^T A x != 0"
]

N_HYP = 2
NEG_Q_INDEX = 2