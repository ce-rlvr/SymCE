import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Let V be an n-dimensional vector space over a field F, and T be a linear operator on V
    # We interpret this as the witness being a square matrix of dimension n >= 1.
    try:
        if isinstance(witness, list):
            matrix_witness = Matrix(witness)
        else:
            matrix_witness = witness
        h1 = isinstance(matrix_witness, MatrixBase) and matrix_witness.is_square and matrix_witness.shape[0] >= 1
    except Exception:
        h1 = False

    # neg_Q: T is NOT diagonalizable over F
    try:
        if isinstance(witness, list):
            matrix_witness = Matrix(witness)
        else:
            matrix_witness = witness
        neg_q = not matrix_witness.is_diagonalizable()
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: T is a linear operator on an n-dimensional vector space (square matrix)",
    "¬Q: T is not diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1