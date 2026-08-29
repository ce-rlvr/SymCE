import sympy
from sympy import eye, zeros, Matrix, I, simplify, Integer
import math

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            U = witness.get('U')
            k = witness.get('k')
            V = witness.get('V')
        else:
            U, k, V = witness
    except Exception:
        return [False, False, False]

    # H_1: U is an n x n unitary matrix
    try:
        if not isinstance(U, Matrix) or U.shape[0] != U.shape[1]:
            h1_ok = False
        else:
            n = U.shape[0]
            diff = U * U.H - eye(n)
            if diff.is_zero_matrix:
                h1_ok = True
            else:
                diff_simp = diff.expand()
                if diff_simp.is_zero_matrix:
                    h1_ok = True
                else:
                    h1_ok = bool(sympy.simplify(diff).is_zero_matrix)
    except Exception:
        h1_ok = False

    # H_2: k is an integer such that 1 <= k <= n
    try:
        if not isinstance(U, Matrix):
            h2_ok = False
        else:
            n = U.shape[0]
            h2_ok = isinstance(k, (int, Integer)) and 1 <= k <= n
    except Exception:
        h2_ok = False

    # ¬Q: The spectral norm of V is greater than 1
    try:
        if not isinstance(V, Matrix):
            neg_q_ok = False
        else:
            try:
                sv = V.singular_values()
                max_sv = max([float(abs(val.evalf())) for val in sv])
            except Exception:
                # Fallback if singular_values() fails
                M = V.H * V
                evs = M.eigenvals()
                max_sv = math.sqrt(max([float(abs(ev.evalf())) for ev in evs.keys()]))
            
            # Use a small epsilon to avoid floating point inaccuracies for norm exactly 1
            neg_q_ok = bool(max_sv > 1.0 + 1e-9)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: U is an n x n unitary matrix",
    "H_2: k is an integer such that 1 <= k <= n",
    "¬Q: The spectral norm of V is greater than 1"
]

N_HYP = 2
NEG_Q_INDEX = 2