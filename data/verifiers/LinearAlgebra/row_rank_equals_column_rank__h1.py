import sympy
from sympy import Matrix, MatrixBase, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # H_1: The entries of A are elements of a field F
        # A field is commutative, so we check that the witness is a matrix with commutative entries.
        h1 = isinstance(witness, MatrixBase) and all(getattr(e, 'is_commutative', True) for e in witness)
    except Exception:
        h1 = False

    try:
        # ¬Q: The dimension of the row space of A is not equal to the dimension of the column space of A
        row_dim = len(witness.rowspace())
        col_dim = len(witness.columnspace())
        neg_q = bool(row_dim != col_dim)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The entries of A are elements of a field F",
    "¬Q: The dimension of the row space of A is not equal to the dimension of the column space of A"
]

N_HYP = 1
NEG_Q_INDEX = 1