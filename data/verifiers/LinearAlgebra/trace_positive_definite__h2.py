import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is an n x n matrix with real entries
    try:
        h1_ok = isinstance(witness, sympy.MatrixBase) and witness.is_square
        if h1_ok:
            for e in witness:
                if not e.is_real:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # H_2: A is positive definite
    try:
        h2_ok = False
        if h1_ok:
            if witness.rows == 0 and witness.cols == 0:
                h2_ok = True
            else:
                h2_ok = (witness.is_positive_definite == True)
    except Exception:
        h2_ok = False

    # ¬Q: The trace of A is not strictly greater than zero
    try:
        neg_q_ok = False
        if h1_ok:
            tr = witness.trace()
            try:
                neg_q_ok = bool(tr <= 0)
            except TypeError:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with real entries",
    "H_2: A is positive definite",
    "¬Q: The trace of A is not strictly greater than zero"
]

N_HYP = 2
NEG_Q_INDEX = 2