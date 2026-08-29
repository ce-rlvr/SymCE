import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a square matrix representing a pairing 
    between V* and V.
    """
    try:
        # H_1: V is a finite-dimensional vector space over a field F.
        # In our representation, this means the witness is a square matrix.
        h1 = isinstance(witness, sp.MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        # ¬Q: The conclusion fails, meaning the pairing is degenerate.
        # This occurs if and only if the matrix determinant is zero.
        if h1:
            neg_q = bool(witness.det() == 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F (witness is a square matrix representing a pairing)",
    "¬Q: The pairing is degenerate (determinant is zero)"
]

N_HYP = 1
NEG_Q_INDEX = 1