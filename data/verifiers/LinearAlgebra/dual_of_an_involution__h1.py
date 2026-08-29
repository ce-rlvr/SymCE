import sympy
from sympy import eye, zeros, simplify
from sympy.matrices import MatrixBase

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: T is a linear operator
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    # H_2: T o T = I_V
    try:
        if h1:
            n = witness.rows
            I = eye(n)
            diff = witness * witness - I
            h2 = (diff == zeros(n, n))
            if not h2:
                h2 = (simplify(diff) == zeros(n, n))
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: T^* o T^* != I_{V^*}
    try:
        if h1:
            n = witness.rows
            I = eye(n)
            # The dual operator corresponds to the transpose matrix
            T_star = witness.T
            diff = T_star * T_star - I
            is_I = (diff == zeros(n, n))
            if not is_I:
                is_I = (simplify(diff) == zeros(n, n))
            neg_q = not is_I
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: T is a linear operator",
    "H_2: T o T = I_V",
    "¬Q: T^* o T^* != I_{V^*}"
]

N_HYP = 2
NEG_Q_INDEX = 2