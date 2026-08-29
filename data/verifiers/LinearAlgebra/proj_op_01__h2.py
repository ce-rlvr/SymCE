import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of two matrices (P, Q).
    """
    try:
        P_raw, Q_raw = witness
        P = Matrix(P_raw)
        Q = Matrix(Q_raw)
    except Exception:
        return [False, False, False, False]

    # H_1: V is a vector space (P and Q are square matrices of the same size, representing operators on V)
    try:
        h1 = bool(P.is_square and Q.is_square and P.shape == Q.shape)
    except Exception:
        h1 = False

    # H_2: The range of P is equal to the range of Q
    # The range (column space) is equal iff rank(P) == rank(Q) == rank([P | Q])
    try:
        if h1:
            r_P = P.rank()
            r_Q = Q.rank()
            h2 = bool((r_P == r_Q) and (r_P == P.row_join(Q).rank()))
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: The kernel of P is equal to the kernel of Q
    # The kernel (null space) is equal iff the row spaces are equal,
    # which is true iff rank(P) == rank(Q) == rank([P^T | Q^T]^T) = rank(vstack(P, Q))
    try:
        if h1:
            r_P = P.rank()
            r_Q = Q.rank()
            h3 = bool((r_P == r_Q) and (r_P == P.col_join(Q).rank()))
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: P != Q
    try:
        if h1:
            neg_q = bool(P != Q)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space (P and Q are square matrices of same size)",
    "H_2: The range of P is equal to the range of Q",
    "H_3: The kernel of P is equal to the kernel of Q",
    "¬Q: P != Q"
]

N_HYP = 3
NEG_Q_INDEX = 3