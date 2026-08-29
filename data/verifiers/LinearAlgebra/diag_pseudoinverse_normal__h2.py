import sympy
from sympy import Matrix, eye, zeros, simplify, I, Rational
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_normal(M):
    diff = M * M.H - M.H * M
    if diff == zeros(M.rows, M.cols):
        return True
    diff_simp = simplify(diff)
    return diff_simp == zeros(M.rows, M.cols)

def conditions(witness):
    try:
        if not hasattr(witness, 'rows') or not hasattr(witness, 'cols') or witness.rows != witness.cols:
            h1 = False
        else:
            h1 = is_normal(witness)
    except Exception:
        h1 = False

    try:
        if not hasattr(witness, 'rows') or not hasattr(witness, 'cols') or witness.rows != witness.cols:
            neg_q = False
        else:
            A_pinv = witness.pinv()
            neg_q = not is_normal(A_pinv)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n normal matrix over the complex numbers",
    "¬Q: The pseudoinverse A^+ is not unitarily diagonalizable over the complex numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1