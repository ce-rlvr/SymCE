import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        T, v, lam = witness
        T = Matrix(T)
        v = Matrix(v)
        if v.shape[0] == 1 and v.shape[1] > 1:
            v = v.T
    except Exception:
        return [False, False, False]

    # H1: V is an inner product space
    try:
        h1 = T.is_square and v.shape == (T.shape[0], 1)
    except Exception:
        h1 = False

    # H2: v is an eigenvector of T corresponding to the eigenvalue lambda
    try:
        if not h1:
            h2 = False
        else:
            is_zero = True
            for x in v:
                if sympy.simplify(x) != 0:
                    is_zero = False
                    break
            if is_zero:
                h2 = False
            else:
                diff = T * v - lam * v
                h2 = all(sympy.simplify(x) == 0 for x in diff)
    except Exception:
        h2 = False

    # neg_Q: v is not an eigenvector of T^* corresponding to the eigenvalue conjugate(lambda)
    try:
        if not h1:
            neg_q = False
        else:
            diff2 = T.H * v - sympy.conjugate(lam) * v
            neg_q = not all(sympy.simplify(x) == 0 for x in diff2)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is an inner product space",
    "H_2: v is an eigenvector of T corresponding to the eigenvalue lambda",
    "¬Q: v is not an eigenvector of T^* corresponding to the eigenvalue conjugate(lambda)"
]

N_HYP = 2
NEG_Q_INDEX = 2