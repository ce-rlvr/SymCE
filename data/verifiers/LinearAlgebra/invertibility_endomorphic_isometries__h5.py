import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a tuple (B, T) of two matrices
        if not (isinstance(witness, (list, tuple)) and len(witness) == 2):
            return [False, False, False, False, False]
        B, T = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: V is a finite-dimensional vector space over a field F
    try:
        h1 = hasattr(B, 'shape') and hasattr(T, 'shape')
    except Exception:
        h1 = False

    # H_2: B is a bilinear form on V
    try:
        h2 = h1 and getattr(B, 'is_square', False) and B.shape[0] > 0
    except Exception:
        h2 = False

    # H_3: B is non-degenerate
    try:
        h3 = h2 and (sympy.expand(B.det()) != 0)
    except Exception:
        h3 = False

    # H_4: T is a linear operator from V to V
    try:
        h4 = h1 and h2 and getattr(T, 'is_square', False) and T.shape == B.shape
    except Exception:
        h4 = False

    # ¬Q: T is not an invertible linear operator
    try:
        neg_q = h4 and (sympy.expand(T.det()) == 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: B is a bilinear form on V",
    "H_3: B is non-degenerate",
    "H_4: T is a linear operator from V to V",
    "¬Q: T is not an invertible linear operator"
]

N_HYP = 4
NEG_Q_INDEX = 4