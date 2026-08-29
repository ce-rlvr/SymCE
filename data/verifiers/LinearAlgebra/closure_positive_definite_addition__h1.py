import sympy
from sympy.matrices import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        A, B = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = A.is_positive_definite
        h1_ok = False if h1 is None else bool(h1)
    except Exception:
        h1_ok = False

    try:
        h2 = B.is_positive_definite
        h2_ok = False if h2 is None else bool(h2)
    except Exception:
        h2_ok = False

    try:
        C = A + B
        q = C.is_positive_definite
        neg_q_ok = False if q is None else not bool(q)
    except Exception:
        # If addition fails (e.g., due to shape mismatch), A + B is undefined,
        # hence it is not a positive definite matrix.
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is positive definite",
    "H_2: B is positive definite",
    "¬Q: A + B is not a positive definite matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2