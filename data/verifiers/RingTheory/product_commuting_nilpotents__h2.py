import sympy
from sympy import eye, zeros, Matrix

# Standard bindings for potential matrix witnesses
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "If R is a ring and x, y are commuting elements, then xy is nilpotent."
    """
    try:
        x, y = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a ring
    # We verify this by checking if x and y support ring operations
    # (addition, subtraction, multiplication) without error.
    try:
        _ = x + y
        _ = x - y
        _ = x * y
        h1 = True
    except Exception:
        h1 = False

    # H_2: x and y commute
    try:
        h2 = bool(x * y == y * x)
    except Exception:
        h2 = False

    # ¬Q: xy is NOT nilpotent
    try:
        xy = x * y
        if hasattr(xy, 'is_Matrix') and xy.is_Matrix:
            if xy.shape[0] != xy.shape[1]:
                is_nilp = False
            else:
                n = xy.shape[0]
                is_nilp = bool(xy**n == xy.zeros(n, n))
        else:
            try:
                is_nilp = bool(sympy.expand(xy) == 0)
            except Exception:
                is_nilp = bool(xy == 0)
        neg_q = not is_nilp
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: x and y commute",
    "¬Q: The product xy is not nilpotent"
]

N_HYP = 2
NEG_Q_INDEX = 2