import sympy
from sympy import QQ, ZZ

# Setup
RR = sympy.S.Reals
CC = sympy.S.Complexes

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            R = witness
            M = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a right Artinian ring
    try:
        h1 = False
        if hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        elif hasattr(R, 'is_finite') and R.is_finite:
            h1 = True
        elif hasattr(R, 'order') and R.order < float('inf'):
            h1 = True
        elif hasattr(R, 'is_finite_ring') and R.is_finite_ring:
            h1 = True
    except Exception:
        h1 = False

    # H_2: M is a right R-module
    try:
        h2 = False
        if isinstance(M, int) and M >= 0:
            h2 = True
        elif M == R:
            h2 = True
        elif hasattr(M, 'domain') and M.domain == R:
            h2 = True
        elif hasattr(M, 'shape'):
            h2 = True
        elif isinstance(M, (list, tuple)):
            h2 = True
        elif hasattr(M, 'is_Module') and M.is_Module:
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: M is not the zero module
    try:
        neg_q = False
        if isinstance(M, int):
            neg_q = (M > 0)
        elif M == R:
            neg_q = True
        elif hasattr(M, 'is_zero') and M.is_zero is not None:
            neg_q = not M.is_zero
        elif hasattr(M, 'shape'):
            if len(M.shape) == 2:
                neg_q = (M.shape[0] * M.shape[1] > 0)
            else:
                neg_q = True
        elif isinstance(M, (list, tuple)):
            neg_q = any(x != 0 for x in M)
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "H_2: M is a right R-module",
    "¬Q: M is not the zero module"
]

N_HYP = 2
NEG_Q_INDEX = 2