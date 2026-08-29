import sympy
from sympy import Matrix, eye, zeros, Expr
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    a = witness
    if isinstance(witness, (tuple, list)) and len(witness) > 0:
        a = witness[-1]

    try:
        h1 = False
        if isinstance(a, MatrixBase) and a.is_square:
            h1 = True
        elif isinstance(a, Expr):
            h1 = True
        elif isinstance(a, (int, float, complex)):
            h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = False
        if h1:
            if isinstance(a, MatrixBase):
                n = a.shape[0]
                is_scalar = True
                for i in range(n):
                    for j in range(n):
                        if i == j:
                            if sympy.expand(a[i, j] - a[0, 0]) != 0:
                                is_scalar = False
                        else:
                            if sympy.expand(a[i, j]) != 0:
                                is_scalar = False
                neg_q = not is_scalar
            elif isinstance(a, Expr):
                if a.is_commutative is False:
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a is an element of R",
    "not_Q: The factor ring is not isomorphic to R"
]

N_HYP = 1
NEG_Q_INDEX = 1