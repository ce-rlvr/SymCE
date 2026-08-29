import sympy
from sympy import eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, sympy.MatrixBase):
            Q = Matrix(witness)
        else:
            Q = witness
    except Exception:
        return [False, False]

    # H_1: Q is an n x n real matrix
    try:
        if Q.is_square and Q.shape[0] > 0:
            h1 = all(sympy.sympify(e).is_real == True for e in Q)
        else:
            h1 = False
    except Exception:
        h1 = False

    # ¬Q: The adjugate matrix of Q is NOT equal to det(Q) * Q^T
    try:
        adj = Q.adjugate()
        det = Q.det()
        trans = Q.transpose()
        diff = adj - det * trans
        neg_q = not all(e == 0 or sympy.simplify(e) == 0 for e in diff)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an n x n real matrix",
    "¬Q: The adjugate matrix of Q is not equal to det(Q) * Q^T"
]

N_HYP = 1
NEG_Q_INDEX = 1