import sympy
from sympy import eye, zeros, Matrix
from sympy.matrices.matrixbase import MatrixBase

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: witness is a matrix
    try:
        h1_ok = isinstance(witness, MatrixBase)
    except Exception:
        h1_ok = False

    # ¬Q: ||Q||_2 != 1
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            # The spectral norm (induced 2-norm) is the square root of the 
            # maximum eigenvalue of Q^H * Q.
            M = witness.H * witness
            evals = M.eigenvals()
            if not evals:
                neg_q_ok = False
            else:
                max_eval = max([abs(complex(e.evalf())) for e in evals.keys()])
                norm_2 = max_eval ** 0.5
                # Check if the spectral norm is NOT equal to 1
                neg_q_ok = abs(norm_2 - 1.0) > 1e-9
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: witness is a matrix",
    "¬Q: ||Q||_2 != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1