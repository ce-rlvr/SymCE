import sympy
from sympy import MatrixBase, Matrix, eye, zeros, expand
from sympy.abc import x

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        h2 = h1 and witness.shape[0] >= 2
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = witness.shape[0]
            tr = witness.trace()
            expected = x**(n-1) * (x - tr)
            actual = witness.charpoly(x).as_expr()
            diff = actual - expected
            neg_q = bool(expand(diff) != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix",
    "H_2: n >= 2",
    "¬Q: The characteristic polynomial of A is not x^{n-1}(x - tr(A))"
]

N_HYP = 2
NEG_Q_INDEX = 2