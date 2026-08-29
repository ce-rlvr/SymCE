import sympy
from sympy import MatrixBase, simplify, eye, zeros, I
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase)
    except Exception:
        h1 = False

    try:
        h2 = h1 and witness.is_square
    except Exception:
        h2 = False

    try:
        tr_T = witness.trace()
        tr_T_star = witness.H.trace()
        neg_q = bool(simplify(tr_T - tr_T_star) != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: T: V \\to V is a linear operator",
    "¬Q: tr(T^*) != tr(T)"
]

N_HYP = 2
NEG_Q_INDEX = 2