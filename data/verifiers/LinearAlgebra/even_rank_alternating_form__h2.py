import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, sympy.MatrixBase):
            mat = sympy.Matrix(witness)
        else:
            mat = witness
        h1 = mat.is_square
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, sympy.MatrixBase):
            mat = sympy.Matrix(witness)
        else:
            mat = witness
        neg_q = mat.rank() % 2 != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F (witness is a square matrix)",
    "¬Q: The rank of B is not an even integer"
]

N_HYP = 1
NEG_Q_INDEX = 1