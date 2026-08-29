import sympy
from sympy import eye, zeros, simplify
from sympy.matrices import MatrixBase

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture.
    The witness is expected to be a tuple of three matrices: (A, U, V).
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        A, U, V = witness
    except Exception:
        return [False, False, False]

    # H_1: A is an m x n matrix, U is an m x m matrix, V is an n x n matrix
    try:
        h1 = isinstance(A, MatrixBase) and isinstance(U, MatrixBase) and isinstance(V, MatrixBase)
        if h1:
            m, n = A.shape
            h1 = (U.shape == (m, m)) and (V.shape == (n, n))
    except Exception:
        h1 = False

    # H_2: V is a unitary matrix
    try:
        if h1:
            n = V.cols
            diff = V.H * V - eye(n)
            # Check if V^H V - I is the zero matrix
            h2 = all(simplify(diff[i, j]) == 0 for i in range(n) for j in range(n))
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: UAV does NOT have the exact same singular values as A
    # We check this by comparing the characteristic polynomials of A^H A and (UAV)^H (UAV).
    # If the characteristic polynomials differ, the singular values differ.
    try:
        if h1:
            M1 = A.H * A
            M2 = (U * A * V).H * (U * A * V)
            cp1 = M1.charpoly().as_expr()
            cp2 = M2.charpoly().as_expr()
            diff_cp = simplify(cp1 - cp2)
            neg_q = (diff_cp != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix, U is an m x m matrix, V is an n x n matrix",
    "H_2: V is a unitary matrix",
    "¬Q: UAV does not have the exact same singular values as A"
]

N_HYP = 2
NEG_Q_INDEX = 2