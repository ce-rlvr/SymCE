import sympy
from sympy.matrices import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A, P, Q = witness
    except Exception:
        return [False, False, False, False]

    # H_1: A, P, Q are matrices over a field
    try:
        h1 = (hasattr(A, 'is_Matrix') and A.is_Matrix and 
              hasattr(P, 'is_Matrix') and P.is_Matrix and 
              hasattr(Q, 'is_Matrix') and Q.is_Matrix)
    except Exception:
        h1 = False

    # H_2: A is an m x n matrix and Q is composable (n x k)
    try:
        h2 = A.shape[1] == Q.shape[0]
    except Exception:
        h2 = False

    # H_3: P is an invertible m x m matrix
    try:
        h3 = P.shape[0] == P.shape[1] and P.shape[1] == A.shape[0] and P.det() != 0
    except Exception:
        h3 = False

    # ¬Q: rank(PAQ) != rank(A)
    try:
        neg_q = (P * A * Q).rank() != A.rank()
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A, P, Q are matrices over a field",
    "H_2: A is an m x n matrix and Q is composable (n x k)",
    "H_3: P is an invertible m x m matrix",
    "¬Q: rank(PAQ) != rank(A)"
]

N_HYP = 3
NEG_Q_INDEX = 3