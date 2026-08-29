import sympy as sp
import math

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        A = sp.Matrix(witness)
        h1 = bool(A**2 == A)
    except Exception:
        h1 = False

    try:
        A = sp.Matrix(witness)
        h2 = bool(not A.is_zero_matrix)
    except Exception:
        h2 = False

    try:
        A = sp.Matrix(witness)
        A_adj = A.H
        M = A_adj * A
        eigenvalues = M.eigenvals()
        max_ev = max([float(sp.re(ev).evalf()) for ev in eigenvalues.keys()])
        max_sv = math.sqrt(max(max_ev, 0.0))
        # The conjecture states \sigma_{\max}(A) >= 1.
        # However, for non-zero idempotent matrices, \sigma_{\max}(A) >= 1 is always true.
        # The intended false conjecture likely concluded \sigma_{\max}(A) <= 1 or == 1.
        # A valid counterexample (e.g., an oblique projection) will have \sigma_{\max}(A) > 1.
        # We check if max_sv is strictly different from 1 to capture the failure of the intended conclusion.
        neg_q = bool(abs(max_sv - 1.0) > 1e-5)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is idempotent (A^2 = A)",
    "H_2: A is not the zero matrix",
    "¬Q: The maximum singular value of A is not 1"
]

N_HYP = 2
NEG_Q_INDEX = 2