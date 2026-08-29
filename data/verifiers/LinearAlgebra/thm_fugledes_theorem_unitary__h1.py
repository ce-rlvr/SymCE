import sympy
from sympy import Matrix, eye, zeros, I

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # The witness is expected to be a tuple or list of two matrices: (A, U)
        if len(witness) != 2:
            return [False, False, False]
        A_raw, U_raw = witness
    except Exception:
        return [False, False, False]

    # H_1: A and U are n x n complex matrices
    try:
        A = Matrix(A_raw)
        U = Matrix(U_raw)
        h1 = A.is_square and U.is_square and A.shape == U.shape
    except Exception:
        h1 = False

    # H_2: A U = U A
    try:
        diff_h2 = (A * U - U * A).expand()
        h2 = bool(diff_h2 == zeros(*A.shape))
    except Exception:
        h2 = False

    # ¬Q: A U^* != U^* A
    try:
        diff_q = (A * U.H - U.H * A).expand()
        neg_q = bool(diff_q != zeros(*A.shape))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and U are n x n complex matrices",
    "H_2: A U = U A",
    "¬Q: A U^* != U^* A"
]

N_HYP = 2
NEG_Q_INDEX = 2