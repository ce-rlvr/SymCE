import sympy
from sympy import eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an n x n matrix with real entries.
    try:
        if not isinstance(witness, sympy.MatrixBase):
            h1 = False
        elif not witness.is_square:
            h1 = False
        else:
            # Check that all entries are real numbers
            h1 = bool(all(e.is_real for e in witness))
    except Exception:
        h1 = False

    # ¬Q: A is not orthogonally diagonalizable over the real numbers.
    # A real square matrix is orthogonally diagonalizable over the reals
    # if and only if it is symmetric (A = A^T).
    try:
        if not isinstance(witness, sympy.MatrixBase):
            neg_q = False
        else:
            neg_q = not witness.is_symmetric()
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with real entries",
    "¬Q: A is not orthogonally diagonalizable over the real numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1