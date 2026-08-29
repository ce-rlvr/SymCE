import sympy
from sympy import I, Matrix, eye, zeros, conjugate, simplify

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        U, lam, x = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: U is an n x n unitary matrix
    try:
        if not getattr(U, 'is_Matrix', False) or not U.is_square or U.shape[0] < 1:
            h1 = False
        else:
            n = U.shape[0]
            diff = simplify(U * U.H - eye(n))
            h1 = bool(diff == zeros(n, n))
    except Exception:
        h1 = False

    # H2: lambda is a complex number
    try:
        lam = sympy.sympify(lam)
        h2 = not getattr(lam, 'is_Matrix', False)
    except Exception:
        h2 = False

    # H3: x is a non-zero vector in C^n
    try:
        if not getattr(x, 'is_Matrix', False):
            h3 = False
        else:
            is_col_vec = (x.shape[1] == 1)
            is_non_zero = (x != zeros(x.shape[0], 1))
            if getattr(U, 'is_Matrix', False) and U.is_square:
                dim_match = (x.shape[0] == U.shape[0])
            else:
                dim_match = True
            h3 = bool(is_col_vec and is_non_zero and dim_match)
    except Exception:
        h3 = False

    # neg_Q: U^* x != conjugate(lambda) * x
    try:
        lhs = U.H * x
        rhs = conjugate(lam) * x
        diff = simplify(lhs - rhs)
        neg_q = bool(diff != zeros(x.shape[0], 1))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: U is an n x n unitary matrix",
    "H_2: lambda is a complex number",
    "H_3: x is a non-zero vector in C^n",
    "¬Q: U^* x != conjugate(lambda) * x"
]

N_HYP = 3
NEG_Q_INDEX = 3