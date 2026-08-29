import sympy
from sympy import Matrix, eye, zeros, simplify
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Let F be a field
    # In the context of sympy, we verify that the witness is a matrix-like object
    # which implicitly represents a matrix over a field (like Q, R, C, or a rational function field).
    try:
        h1_ok = hasattr(witness, 'is_diagonalizable') and hasattr(witness, 'eigenvals')
    except Exception:
        h1_ok = False

    # H_2: Suppose A is idempotent, meaning A^2 = A
    try:
        h2_ok = bool(witness**2 == witness)
    except Exception:
        h2_ok = False

    # Q: The matrix A is diagonalizable over F, and its only possible eigenvalues are 0 and 1.
    # neg_Q must be True if the conclusion FAILS.
    try:
        if not witness.is_diagonalizable():
            q_ok = False
        else:
            eigenvals = witness.eigenvals()
            q_ok = True
            for val in eigenvals.keys():
                s_val = simplify(val)
                if s_val != 0 and s_val != 1:
                    q_ok = False
                    break
        neg_q_ok = not q_ok
    except Exception:
        # If we cannot evaluate the conclusion, we cannot definitively say it fails.
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A is idempotent (A^2 = A)",
    "¬Q: A is not diagonalizable over F, or it has an eigenvalue other than 0 and 1"
]

N_HYP = 2
NEG_Q_INDEX = 2