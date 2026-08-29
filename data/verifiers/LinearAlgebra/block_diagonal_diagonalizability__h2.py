import sympy
from sympy import Matrix, diag, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: M is a block diagonal matrix composed of square blocks A_1, A_2, ..., A_k.
    # We accept either a single square matrix (1 block) or a list/tuple of square matrices.
    try:
        if isinstance(witness, Matrix):
            blocks = [witness]
        elif isinstance(witness, (list, tuple)):
            blocks = witness
        else:
            blocks = []
            
        h1 = len(blocks) > 0 and all(isinstance(b, Matrix) and b.is_square for b in blocks)
    except Exception:
        h1 = False

    # ¬Q: The block diagonal matrix M is NOT diagonalizable over F.
    try:
        if h1:
            M = diag(*blocks)
            # is_diagonalizable() returns False if it is not diagonalizable
            res = M.is_diagonalizable()
            neg_q = (res is False)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a block diagonal matrix composed of square blocks",
    "¬Q: M is not diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1