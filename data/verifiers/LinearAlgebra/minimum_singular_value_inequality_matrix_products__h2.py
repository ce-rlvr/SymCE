import sympy
from sympy import MatrixBase, Matrix, eye, zeros
from sympy.abc import x, y, z
import math

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_min_sv(M):
    """
    Helper function to compute the minimum singular value of a SymPy matrix.
    """
    try:
        svs = M.singular_values()
        if not svs:
            return 0.0
        return min([float(abs(complex(sv.evalf()))) for sv in svs])
    except Exception:
        # Fallback: compute square root of minimum eigenvalue of M^* M
        H = M.H * M
        evs = H.eigenvals(multiple=True)
        if not evs:
            return 0.0
        return math.sqrt(min([float(abs(complex(ev.evalf()))) for ev in evs]))

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        A, B = witness
    except Exception:
        return [False, False]
    
    # H_1: A and B are n x n complex matrices
    try:
        if not isinstance(A, MatrixBase) or not isinstance(B, MatrixBase):
            h1 = False
        elif A.rows != A.cols or B.rows != B.cols or A.rows != B.rows:
            h1 = False
        elif A.rows < 1:
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # ¬Q: The minimum singular value of the product AB satisfies \sigma_{\min}(AB) < \sigma_{\min}(A) \sigma_{\min}(B)
    try:
        AB = A * B
        sv_A = get_min_sv(A)
        sv_B = get_min_sv(B)
        sv_AB = get_min_sv(AB)
        
        # We use a small tolerance to account for potential floating-point inaccuracies
        # in the evaluation of symbolic expressions.
        neg_q = sv_AB < (sv_A * sv_B) - 1e-7
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are n x n complex matrices",
    "¬Q: sigma_min(AB) < sigma_min(A) * sigma_min(B)"
]

N_HYP = 1
NEG_Q_INDEX = 1