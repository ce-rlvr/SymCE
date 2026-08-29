import sympy
from sympy import MatrixBase, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square and witness.rows > 0
    except Exception:
        h1 = False

    try:
        tr = (witness * witness).trace()
        h2 = bool(sympy.simplify(tr) == 0)
    except Exception:
        h2 = False

    try:
        if witness.is_zero_matrix is not None:
            neg_q = not witness.is_zero_matrix
        else:
            neg_q = not all(sympy.simplify(x) == 0 for x in witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "H_2: The trace of the operator T*T is equal to zero",
    "¬Q: T is not the zero operator"
]

N_HYP = 2
NEG_Q_INDEX = 2