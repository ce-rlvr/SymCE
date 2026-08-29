import sympy as sp
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            T = witness.get('T')
            S = witness.get('S')
            c = witness.get('c')
        else:
            T, S, c = witness
    except Exception:
        return [False, False, False, False]

    # H_1: V and W are vector spaces over a field F
    # Representing transformations as matrices implies domain and codomain are vector spaces.
    try:
        h1 = isinstance(T, sp.MatrixBase)
    except Exception:
        h1 = False

    # H_2: T: V -> W is a linear transformation
    try:
        h2 = isinstance(T, sp.MatrixBase)
    except Exception:
        h2 = False

    # H_3: c is a scalar in the field F
    try:
        h3 = isinstance(c, (int, float, complex, sp.Expr, sp.Basic)) and not isinstance(c, sp.MatrixBase)
    except Exception:
        h3 = False

    # neg_Q: The dual transformation of the linear combination cT + S is equal to cT* + S*
    try:
        lhs = (c * T + S).transpose()
        rhs = c * T.transpose() + S.transpose()
        q = (lhs == rhs)
        neg_q = not q
    except Exception:
        # If the operations are undefined (e.g., S is not a linear transformation from V to W),
        # the equality fails, so the negation is True.
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V and W are vector spaces over a field F",
    "H_2: T: V -> W is a linear transformation",
    "H_3: c is a scalar in the field F",
    "¬Q: The dual transformation of cT + S is not equal to cT* + S* (or is undefined)"
]

N_HYP = 3
NEG_Q_INDEX = 3