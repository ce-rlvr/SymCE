import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, list):
            matrix_witness = Matrix(witness)
        else:
            matrix_witness = witness
            
        h1 = isinstance(matrix_witness, MatrixBase) and matrix_witness.is_square and len(matrix_witness.free_symbols) == 0
    except Exception:
        h1 = False

    try:
        if isinstance(witness, list):
            matrix_witness = Matrix(witness)
        else:
            matrix_witness = witness
            
        A_star = matrix_witness.H
        neg_q = (A_star.is_diagonalizable() == False)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over the field of complex numbers",
    "¬Q: The conjugate transpose A^* is not diagonalizable over the complex numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1