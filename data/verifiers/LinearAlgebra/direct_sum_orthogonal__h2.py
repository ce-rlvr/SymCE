import sympy
from sympy import Matrix, eye, diag, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        A, B = witness
    except Exception:
        return [False, False]
    
    # H1: A is a real n x n orthogonal matrix
    try:
        if not isinstance(A, Matrix):
            h1_ok = False
        elif A.rows != A.cols:
            h1_ok = False
        elif not all(x.is_real for x in A):
            h1_ok = False
        else:
            n = A.rows
            h1_ok = bool(A.T * A == eye(n))
    except Exception:
        h1_ok = False

    # neg_Q: A \oplus B is NOT a real (n+m) x (n+m) orthogonal matrix
    try:
        if not isinstance(A, Matrix) or not isinstance(B, Matrix):
            neg_q_ok = False
        else:
            M = diag(A, B)
            if M.rows != M.cols:
                neg_q_ok = True
            elif not all(x.is_real for x in M):
                neg_q_ok = True
            else:
                k = M.rows
                neg_q_ok = not bool(M.T * M == eye(k))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is a real n x n orthogonal matrix",
    "¬Q: The direct sum A \\oplus B is not a real (n+m) x (n+m) orthogonal matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1