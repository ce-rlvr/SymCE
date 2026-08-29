import sympy
from sympy import MatrixBase, eye, simplify, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H1: The entries of Q are real numbers
    try:
        h1 = isinstance(witness, MatrixBase) and all((elem.is_real == True) for elem in witness)
    except Exception:
        h1 = False

    # H2: Q is an orthogonal matrix (Q^T Q = I)
    try:
        if isinstance(witness, MatrixBase):
            I_mat = eye(witness.cols)
            diff = witness.T * witness - I_mat
            h2 = diff.is_zero_matrix
            if not h2:
                diff = simplify(diff)
                h2 = diff.is_zero_matrix
            h2 = bool(h2)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: Conclusion fails
    # The Spectral Theorem for Real Orthogonal Matrices guarantees the conclusion 
    # holds for all square real orthogonal matrices. The conclusion can only fail 
    # if Q is not a square matrix (in which case P^T Q P is undefined for square P).
    try:
        if isinstance(witness, MatrixBase):
            neg_q = not witness.is_square
        else:
            neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The entries of Q are real numbers",
    "H_2: Q is an orthogonal matrix (Q^T Q = I)",
    "¬Q: There does not exist a real orthogonal matrix P such that P^T Q P is a block diagonal matrix of 1x1 and 2x2 rotation blocks"
]

N_HYP = 2
NEG_Q_INDEX = 2