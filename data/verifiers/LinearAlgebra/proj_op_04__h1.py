import sympy
from sympy import Matrix, MatrixBase, eye, zeros, simplify

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            P = witness['P']
            x = witness['x']
        else:
            P, x = witness
    except Exception:
        return [False, False]

    # H_1: x is a column vector of compatible dimension
    try:
        h1 = False
        if isinstance(P, MatrixBase) and isinstance(x, MatrixBase):
            if x.cols == 1 and P.is_square and P.cols == x.rows:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: Px and x - Px are NOT orthogonal
    try:
        Px = P * x
        x_minus_Px = x - Px
        dot_prod = (Px.T * x_minus_Px)[0, 0]
        neg_q = bool(simplify(dot_prod) != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a column vector of compatible dimension",
    "¬Q: Px and x - Px are not orthogonal"
]

N_HYP = 1
NEG_Q_INDEX = 1