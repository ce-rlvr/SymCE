import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "The kernel of T^* is equal to the orthogonal complement of the image of T"
    for a non-degenerate bilinear form B.
    
    Witness is expected to be a tuple (B_matrix, T_matrix).
    """
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        B_raw, T_raw = witness
        B = Matrix(B_raw)
        T = Matrix(T_raw)
    except Exception:
        return [False, False, False, False]
    
    # H_1: V is a finite-dimensional vector space over a field F
    # Represented by the fact that B and T are square matrices of the same dimension > 0.
    try:
        h1 = bool(B.is_square and T.is_square and B.shape == T.shape and B.shape[0] > 0)
    except Exception:
        h1 = False

    # H_2: B is a non-degenerate bilinear form on V
    try:
        h2 = bool(h1 and B.det() != 0)
    except Exception:
        h2 = False

    # H_3: T is a linear operator on V
    # Covered by T being a square matrix of the same size as B.
    try:
        h3 = bool(h1)
    except Exception:
        h3 = False

    # ¬Q: ker(T^*) != (im(T))^perp
    # The adjoint T^* satisfies B(Tx, y) = B(x, T^*y).
    # In matrix form, T^* = B^{-1} T^T B.
    # The kernel of T^* is the nullspace of T^T B.
    # The standard (left) orthogonal complement of im(T) is {x | B(x, Ty) = 0 for all y}.
    # In matrix form, this is the nullspace of T^T B^T.
    # The conjecture fails if these two nullspaces are different.
    # Two matrices of the same size have the same nullspace iff their row spaces are equal,
    # which is true iff their reduced row echelon forms are identical.
    try:
        if not h1:
            neg_q = False
        else:
            M1 = T.transpose() * B
            M2 = T.transpose() * B.transpose()
            neg_q = bool(M1.rref(simplify=True)[0] != M2.rref(simplify=True)[0])
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: B is a non-degenerate bilinear form on V",
    "H_3: T is a linear operator on V",
    "¬Q: ker(T^*) != (im(T))^perp"
]

N_HYP = 3
NEG_Q_INDEX = 3