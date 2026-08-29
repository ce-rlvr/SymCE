import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

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
        P, J = witness.jordan_form()
        is_diag = True
        for i in range(J.rows):
            for j in range(J.cols):
                if i != j and J[i, j] != 0:
                    is_diag = False
                    break
            if not is_diag:
                break
        
        entries_ok = all(J[i, i] == 1 or J[i, i] == -1 for i in range(J.rows))
        neg_q = not (is_diag and entries_ok)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: The Jordan canonical form of A is not a diagonal matrix with only 1 and -1 on the diagonal"
]

N_HYP = 1
NEG_Q_INDEX = 1