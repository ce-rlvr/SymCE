import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: B is a bilinear form on W",
    "H_3: T has a non-trivial kernel",
    "¬Q: The pullback bilinear form B_T is non-degenerate on V"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Given a witness, checks if it satisfies the hypotheses and falsifies the conclusion.
    The witness is expected to provide a matrix T (representing the linear map V -> W)
    and a matrix B (representing the bilinear form on W).
    """
    try:
        if isinstance(witness, dict):
            T = Matrix(witness['T'])
            B = Matrix(witness['B'])
        elif isinstance(witness, (list, tuple)):
            T = Matrix(witness[0])
            B = Matrix(witness[1])
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: V and W are vector spaces over a field F
    # Represented by the fact that T and B are valid matrices with scalar entries
    try:
        h1 = True
    except Exception:
        h1 = False

    # H_2: B is a bilinear form on W
    # B must be a square matrix and its dimension must match the codomain of T (rows of T)
    try:
        h2 = bool(B.is_square and B.rows == T.rows)
    except Exception:
        h2 = False

    # H_3: T has a non-trivial kernel
    # T is an m x n matrix. Non-trivial kernel means rank(T) < n (where n is T.cols)
    try:
        h3 = bool(T.rank() < T.cols)
    except Exception:
        h3 = False

    # ¬Q: The pullback bilinear form B_T is non-degenerate on V
    # B_T = T^T * B * T
    # Non-degenerate means rank(B_T) == n (where n is the dimension of V, i.e., T.cols)
    try:
        if h2:
            B_T = T.T * B * T
            neg_q = bool(B_T.rank() == T.cols)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]