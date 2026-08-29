import sympy
from sympy import Matrix, MatrixBase, eye, zeros
from sympy.abc import x, y, z

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: F is a field of characteristic zero
    # In SymPy, standard matrices are over fields of characteristic zero (QQ, RR, CC, or expressions).
    try:
        h1 = isinstance(witness, MatrixBase)
    except Exception:
        h1 = False

    # H_2: A is an n x n matrix over F
    try:
        h2 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h2 = False

    # ¬Q: A is not a nilpotent matrix
    try:
        if isinstance(witness, MatrixBase) and witness.is_square:
            n = witness.rows
            if n == 0:
                neg_q = False
            else:
                neg_q = bool(witness**n != zeros(n, n))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic zero",
    "H_2: A is an n x n matrix over F",
    "¬Q: A is not a nilpotent matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2