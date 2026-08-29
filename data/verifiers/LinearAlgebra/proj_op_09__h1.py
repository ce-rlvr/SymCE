import sympy
from sympy import eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            P, r = witness
        else:
            P = witness
            r = P.rank()
    except Exception:
        return [False, False]

    try:
        if not getattr(P, "is_square", False):
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1 = bool(sympy.Eq(P.rank(), r))
    except Exception:
        h1 = False

    try:
        I = eye(P.shape[0])
        det_val = (I + P).det()
        diff = sympy.simplify(det_val - 2**r)
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The rank of P is r",
    "¬Q: The determinant of the matrix I + P is not equal to 2^r"
]

N_HYP = 1
NEG_Q_INDEX = 1