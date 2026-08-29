import sympy
from sympy import MatrixBase, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: F is a field
    # In the context of sympy, we assume the matrix entries belong to a field (e.g., Q, R, C).
    try:
        h1_ok = isinstance(witness, MatrixBase)
    except Exception:
        h1_ok = False

    # H_2: A is an n x n matrix over F
    try:
        h2_ok = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h2_ok = False

    # ¬Q: The trace of A is not zero
    try:
        if isinstance(witness, MatrixBase) and witness.is_square:
            tr = sympy.simplify(witness.trace())
            neg_q_ok = bool(tr != 0)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A is an n x n matrix over F",
    "¬Q: The trace of A is not zero"
]

N_HYP = 2
NEG_Q_INDEX = 2