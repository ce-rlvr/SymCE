import sympy
from sympy import Matrix, eye, zeros, I, Abs, simplify, N

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        U, alpha = witness
    except Exception:
        return [False, False, False]

    # H_1: U is an n x n unitary matrix
    try:
        if not hasattr(U, 'rows') or not hasattr(U, 'cols') or not hasattr(U, 'H'):
            h1 = False
        elif U.rows != U.cols:
            h1 = False
        else:
            n = U.rows
            diff = simplify(U * U.H - eye(n))
            h1 = all(simplify(diff[i, j]) == 0 for i in range(n) for j in range(n))
    except Exception:
        h1 = False

    # H_2: alpha is a complex scalar
    try:
        if hasattr(alpha, 'is_Matrix') and alpha.is_Matrix:
            h2 = False
        elif hasattr(alpha, 'rows'):
            h2 = False
        else:
            try:
                complex(alpha)
                h2 = True
            except Exception:
                complex(N(alpha))
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: |alpha| != 1
    try:
        abs_val = simplify(Abs(alpha))
        if abs_val == 1:
            neg_q = False
        else:
            val = abs(complex(N(alpha)))
            if abs(val - 1.0) < 1e-12:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: U is an n x n unitary matrix",
    "H_2: alpha is a complex scalar",
    "¬Q: |alpha| != 1"
]

N_HYP = 2
NEG_Q_INDEX = 2