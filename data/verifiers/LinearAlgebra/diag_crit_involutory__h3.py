import sympy
from sympy import Matrix
from sympy.matrices import MatrixBase, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, list):
            witness = Matrix(witness)
    except Exception:
        pass

    try:
        h1 = False
        if isinstance(witness, MatrixBase):
            h1 = True
            if hasattr(witness, 'domain') and hasattr(witness.domain, 'char'):
                if witness.domain.char == 2:
                    h1 = False
    except Exception:
        h1 = False

    try:
        h2 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h2 = False

    try:
        neg_q = False
        if isinstance(witness, MatrixBase) and witness.is_square:
            diag = witness.is_diagonalizable()
            if diag is False:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field with characteristic not equal to 2",
    "H_2: A is an n by n matrix over F",
    "¬Q: A is not diagonalizable over F"
]

N_HYP = 2
NEG_Q_INDEX = 2