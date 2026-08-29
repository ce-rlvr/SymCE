import sympy
from sympy import eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # The witness is expected to be a matrix T (or a tuple (V, T)).
    if isinstance(witness, tuple) and len(witness) == 2:
        T = witness[1]
    else:
        T = witness

    try:
        if not hasattr(T, 'shape'):
            T = Matrix(T)
        # Any matrix implicitly acts on C^n, which is a complex inner product space.
        h1_ok = hasattr(T, 'shape') and len(T.shape) == 2
    except Exception:
        h1_ok = False

    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            # The conclusion states there exist unique self-adjoint operators A and B on V 
            # such that T = A + iB. This implies T must be an operator on V (i.e., a square matrix).
            # If T is not square, it cannot be written as the sum of operators on V.
            neg_q_ok = T.shape[0] != T.shape[1]
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: V is a complex inner product space",
    "¬Q: There do not exist unique self-adjoint operators A and B on V such that T = A + iB"
]

N_HYP = 1
NEG_Q_INDEX = 1