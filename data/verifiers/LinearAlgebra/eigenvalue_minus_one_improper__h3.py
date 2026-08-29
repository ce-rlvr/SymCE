import sympy
from sympy.matrices import MatrixBase, eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: Q is a real n \times n matrix
    try:
        if isinstance(witness, MatrixBase) and witness.is_square and witness.shape[0] > 0:
            # Check that all entries are real numbers
            h1_ok = all(bool(e.is_real) for e in witness)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: Q is an orthogonal matrix
    try:
        if h1_ok:
            n = witness.shape[0]
            # Q is orthogonal if Q^T * Q = I
            diff = witness.transpose() * witness - eye(n)
            h2_ok = diff.is_zero_matrix or diff == zeros(n, n)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: The matrix Q does NOT have an eigenvalue equal to -1
    try:
        if h1_ok:
            n = witness.shape[0]
            # -1 is an eigenvalue iff det(Q - (-1)*I) == 0, which is det(Q + I) == 0.
            # Therefore, Q does NOT have -1 as an eigenvalue iff det(Q + I) != 0.
            neg_q_ok = (witness + eye(n)).det() != 0
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: Q is a real n x n matrix",
    "H_2: Q is an orthogonal matrix",
    "¬Q: Q does not have an eigenvalue equal to -1"
]

N_HYP = 2
NEG_Q_INDEX = 2