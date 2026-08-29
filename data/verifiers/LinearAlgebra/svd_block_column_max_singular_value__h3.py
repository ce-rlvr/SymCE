import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z
import math

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def max_sv_sq(M):
    """
    Computes the square of the maximum singular value of a matrix M.
    This is the maximum eigenvalue of M^* M.
    """
    if M.rows == 0 or M.cols == 0:
        return 0.0
    MtM = M.H * M
    evs = MtM.eigenvals()
    max_val = 0.0
    for ev in evs.keys():
        try:
            val = float(ev.evalf())
        except TypeError:
            val = complex(ev.evalf()).real
        if val > max_val:
            max_val = val
    return max_val

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            C = witness.get('C')
        else:
            A, B, C = witness
    except Exception:
        return [False, False, False, False]

    # H_1: A is a complex matrix
    try:
        h1 = hasattr(A, 'is_Matrix') and A.is_Matrix
    except Exception:
        h1 = False

    # H_2: B is a complex matrix
    try:
        h2 = hasattr(B, 'is_Matrix') and B.is_Matrix
    except Exception:
        h2 = False

    # H_3: A and B have the same number of columns
    try:
        h3 = bool(h1 and h2 and (A.cols == B.cols))
    except Exception:
        h3 = False

    # ¬Q: The conclusion FAILS, meaning sigma_max(C)^2 > sigma_max(A)^2 + sigma_max(B)^2
    try:
        if not (hasattr(C, 'is_Matrix') and C.is_Matrix):
            neg_q = False
        else:
            s_A = max_sv_sq(A)
            s_B = max_sv_sq(B)
            s_C = max_sv_sq(C)
            # We use a small tolerance to avoid floating point issues
            neg_q = bool(s_C > s_A + s_B + 1e-9)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is a complex matrix",
    "H_2: B is a complex matrix",
    "H_3: A and B have the same number of columns",
    "¬Q: sigma_max(C)^2 > sigma_max(A)^2 + sigma_max(B)^2"
]

N_HYP = 3
NEG_Q_INDEX = 3