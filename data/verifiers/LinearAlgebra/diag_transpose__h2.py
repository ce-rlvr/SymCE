import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an n x n matrix over a field F
    try:
        if not isinstance(witness, Matrix):
            A = Matrix(witness)
        else:
            A = witness
        h1_ok = A.is_square
    except Exception:
        h1_ok = False

    # ¬Q: The transpose matrix A^T is NOT diagonalizable over F
    try:
        if not isinstance(witness, Matrix):
            A = Matrix(witness)
        else:
            A = witness
        
        # is_diagonalizable() returns True if diagonalizable, False if not.
        # We check explicitly for False to ensure it was decidable and failed.
        neg_q_ok = (A.transpose().is_diagonalizable() == False)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: A^T is not diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1