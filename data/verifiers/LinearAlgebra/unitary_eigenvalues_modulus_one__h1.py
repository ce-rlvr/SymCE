import sympy
from sympy import eye, simplify, Abs, Matrix, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        U, lam = witness
    except Exception:
        return [False, False, False]
    
    # H_1: U is a unitary matrix
    try:
        if not hasattr(U, 'shape') or len(U.shape) != 2:
            h1 = False
        else:
            n = U.shape[0]
            if U.shape[0] != U.shape[1]:
                h1 = False
            else:
                diff = U.H * U - eye(n)
                h1 = bool(all(sympy.expand(diff[i, j]) == 0 or simplify(diff[i, j]) == 0 for i in range(n) for j in range(n)))
    except Exception:
        h1 = False

    # H_2: lambda is an eigenvalue of U
    try:
        n = U.shape[0]
        det_val = (U - lam * eye(n)).det()
        h2 = bool(sympy.expand(det_val) == 0 or simplify(det_val) == 0)
    except Exception:
        h2 = False

    # ¬Q: The absolute value of lambda is not equal to 1
    try:
        mag = simplify(Abs(lam))
        neg_q = bool(mag != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "H_2: lambda is an eigenvalue of U",
    "¬Q: The absolute value of lambda is not equal to 1"
]

N_HYP = 2
NEG_Q_INDEX = 2