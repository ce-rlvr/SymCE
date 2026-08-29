import sympy
from sympy import Matrix, eye, simplify, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, Matrix) and witness.is_square
    except Exception:
        h1 = False

    try:
        h2 = h1
    except Exception:
        h2 = False

    try:
        if h1:
            I = eye(witness.rows)
            P = (I + witness) / 2
            diff = P * P - P
            is_proj = all(simplify(e) == 0 for e in diff)
            neg_q = not is_proj
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field of characteristic not equal to 2",
    "H_2: I is the identity operator on V",
    "¬Q: P = 1/2(I + A) is not a projection operator"
]

N_HYP = 2
NEG_Q_INDEX = 2