import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: Q_2 is an n \times n real orthogonal matrix
    try:
        Q1, Q2 = witness
        if not isinstance(Q1, sympy.MatrixBase):
            Q1 = sympy.Matrix(Q1)
        if not isinstance(Q2, sympy.MatrixBase):
            Q2 = sympy.Matrix(Q2)
            
        n = Q2.rows
        if Q2.cols != n or Q1.rows != n or Q1.cols != n:
            h1 = False
        else:
            is_real = all(v.is_real is not False for v in Q2)
            if not is_real:
                h1 = False
            else:
                diff = Q2.T * Q2 - sympy.eye(n)
                if diff.is_zero_matrix:
                    h1 = True
                else:
                    h1 = all(sympy.simplify(diff[i, j]) == 0 for i in range(n) for j in range(n))
    except Exception:
        h1 = False

    # ¬Q: The absolute value of the Frobenius inner product <Q_1, Q_2>_F is > n
    try:
        Q1, Q2 = witness
        if not isinstance(Q1, sympy.MatrixBase):
            Q1 = sympy.Matrix(Q1)
        if not isinstance(Q2, sympy.MatrixBase):
            Q2 = sympy.Matrix(Q2)
            
        if Q1.shape != Q2.shape:
            neg_q = False
        else:
            n = Q2.rows
            frob_inner = sum(sympy.conjugate(Q1[i, j]) * Q2[i, j] for i in range(n) for j in range(n))
            try:
                neg_q = bool(abs(frob_inner) > n)
            except TypeError:
                neg_q = bool(abs(sympy.simplify(frob_inner)) > n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Q_2 is an n x n real orthogonal matrix",
    "¬Q: The absolute value of the Frobenius inner product <Q_1, Q_2>_F is strictly greater than n"
]

N_HYP = 1
NEG_Q_INDEX = 1