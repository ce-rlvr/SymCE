import sympy
from sympy import eye, zeros, MatrixBase, simplify

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, B = witness
    except Exception:
        return [False, False]
    
    # H1: A is an n x n real orthogonal matrix
    try:
        if not isinstance(A, MatrixBase):
            h1 = False
        elif not A.is_square or A.shape[0] < 1:
            h1 = False
        else:
            n = A.shape[0]
            is_real = all(e.is_real is True for e in A)
            prod = A.T * A
            is_ortho = (prod == eye(n))
            if not is_ortho:
                try:
                    is_ortho = simplify(prod - eye(n)).is_zero_matrix
                except Exception:
                    pass
            h1 = bool(is_real and is_ortho)
    except Exception:
        h1 = False

    # neg_Q: AB is NOT an orthogonal matrix
    try:
        AB = A * B
        if not isinstance(AB, MatrixBase) or not AB.is_square or AB.shape[0] < 1:
            neg_q = True
        else:
            n_ab = AB.shape[0]
            prod_ab = AB.T * AB
            is_ortho_ab = (prod_ab == eye(n_ab))
            if not is_ortho_ab:
                try:
                    is_ortho_ab = simplify(prod_ab - eye(n_ab)).is_zero_matrix
                except Exception:
                    pass
            neg_q = not is_ortho_ab
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n real orthogonal matrix",
    "¬Q: AB is not an orthogonal matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1