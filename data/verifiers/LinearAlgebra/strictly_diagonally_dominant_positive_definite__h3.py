import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H1: A is an n x n real symmetric matrix
    try:
        if not isinstance(witness, Matrix):
            h1 = False
        elif not witness.is_square:
            h1 = False
        elif witness != witness.T:
            h1 = False
        else:
            h1 = True
            for entry in witness:
                if entry.is_real is not True:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: A is strictly diagonally dominant
    try:
        if not isinstance(witness, Matrix) or not witness.is_square:
            h2 = False
        else:
            n = witness.shape[0]
            h2 = True
            for i in range(n):
                diag = sp.Abs(witness[i, i])
                off_diag_sum = sum([sp.Abs(witness[i, j]) for j in range(n) if j != i], sp.S.Zero)
                if bool(diag <= off_diag_sum):
                    h2 = False
                    break
    except Exception:
        h2 = False

    # neg_Q: A is NOT positive definite
    try:
        if not isinstance(witness, Matrix) or not witness.is_square:
            neg_q = False
        else:
            n = witness.shape[0]
            is_pd = True
            for i in range(1, n + 1):
                if bool(witness[:i, :i].det() <= 0):
                    is_pd = False
                    break
            neg_q = not is_pd
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n real symmetric matrix",
    "H_2: A is strictly diagonally dominant",
    "¬Q: A is not positive definite"
]

N_HYP = 2
NEG_Q_INDEX = 2