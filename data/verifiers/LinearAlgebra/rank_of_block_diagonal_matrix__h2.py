import sympy
from sympy.matrices import MatrixBase, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A is a matrix over a field F",
    "H_2: M is a block diagonal matrix formed by placing A and B on the diagonal and zeros elsewhere",
    "¬Q: rank(M) != rank(A) + rank(B)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            A, B, M = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            A, B = witness
            try:
                M = sympy.diag(A, B)
            except Exception:
                M = None
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: A is a matrix over a field F
    try:
        h1 = isinstance(A, MatrixBase)
    except Exception:
        h1 = False

    # H_2: M is a block diagonal matrix formed by placing A and B on the diagonal and zeros elsewhere
    try:
        h2 = (M is not None) and bool(M == sympy.diag(A, B))
    except Exception:
        h2 = False

    # ¬Q: rank(M) != rank(A) + rank(B)
    try:
        q = (M.rank() == A.rank() + B.rank())
    except Exception:
        # If rank() is undefined for B (e.g., B is not a matrix), the conclusion equation is invalid/false.
        q = False
    neg_q = not q

    return [bool(h1), bool(h2), bool(neg_q)]