import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Attempt to parse the witness as a SymPy Matrix
    try:
        if not isinstance(witness, sympy.MatrixBase):
            A = Matrix(witness)
        else:
            A = witness
    except Exception:
        A = None

    # H_1: A is an n by n matrix
    try:
        h1 = (A is not None) and A.is_square
    except Exception:
        h1 = False

    # neg_Q: A is NOT diagonalizable over its field
    try:
        # We explicitly check for False to avoid false positives if is_diagonalizable() returns None
        neg_q = (A is not None) and (A.is_diagonalizable() == False)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: A is not diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1