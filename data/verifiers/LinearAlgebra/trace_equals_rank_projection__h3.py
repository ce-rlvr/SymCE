import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # H_1: V is a finite-dimensional vector space over a field of characteristic zero
        # We verify this by checking that the witness is a concrete numeric matrix (no free symbols).
        # SymPy matrices with numeric entries are over characteristic zero by default.
        h1 = isinstance(witness, sympy.MatrixBase) and len(witness.free_symbols) == 0
    except Exception:
        h1 = False

    try:
        # H_2: P: V \to V is a linear operator
        # This means the matrix representing P must be square.
        h2 = isinstance(witness, sympy.MatrixBase) and witness.is_square
    except Exception:
        h2 = False

    try:
        # ¬Q: tr(P) != rank(P)
        # The conclusion is tr(P) = rank(P), so its negation is that they are not equal.
        neg_q = bool(witness.trace() != witness.rank())
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field of characteristic zero",
    "H_2: P: V \\to V is a linear operator",
    "¬Q: tr(P) != rank(P)"
]

N_HYP = 2
NEG_Q_INDEX = 2