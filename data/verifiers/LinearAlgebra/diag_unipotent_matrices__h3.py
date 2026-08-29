import sympy
from sympy.matrices import MatrixBase, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Check if witness is a matrix with numeric entries (characteristic 0 field like Q, R, C)
        h1 = isinstance(witness, MatrixBase) and all(getattr(e, 'is_number', False) for e in witness)
    except Exception:
        h1 = False

    try:
        # Check if witness is a square matrix
        h2 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h2 = False

    try:
        if isinstance(witness, MatrixBase) and witness.is_square:
            n = witness.shape[0]
            is_diag = witness.is_diagonalizable()
            is_I = (witness == eye(n))
            # The conclusion is "U is diagonalizable iff U is the identity matrix I"
            # The negation is that the equivalence fails (one is true and the other is false)
            neg_q = bool(is_diag != is_I)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic 0",
    "H_2: U is an n \\times n matrix over F",
    "¬Q: It is not the case that U is diagonalizable if and only if U is the identity matrix I"
]

N_HYP = 2
NEG_Q_INDEX = 2