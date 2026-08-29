import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Let V be a finite-dimensional vector space over a field F
    # We verify this by checking if the witness is a square matrix.
    try:
        h1 = isinstance(witness, sympy.MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # H_2: Let P be idempotent, meaning P^2 = P
    try:
        h2 = bool(witness**2 == witness)
    except Exception:
        h2 = False

    # ¬Q: P is NOT a diagonalizable operator over F
    try:
        if not h1:
            neg_q = False
        else:
            diag = witness.is_diagonalizable()
            # We strictly check for False. If it's True or None (undecidable), we return False.
            neg_q = (diag is False)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space (witness is a square matrix)",
    "H_2: P is idempotent (P^2 = P)",
    "¬Q: P is not diagonalizable"
]

N_HYP = 2
NEG_Q_INDEX = 2