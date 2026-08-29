import sympy
from sympy import Matrix, Abs, simplify, eye, zeros, I
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: U is an n x n complex matrix
    try:
        U = Matrix(witness)
        h1 = bool(U.is_square and U.rows > 0)
    except Exception:
        h1 = False

    # neg_Q: S is not doubly stochastic
    try:
        if not h1:
            neg_q = False
        else:
            n = U.rows
            S = zeros(n, n)
            for i in range(n):
                for j in range(n):
                    S[i, j] = simplify(Abs(U[i, j])**2)
            
            is_doubly_stochastic = True
            for i in range(n):
                row_sum = simplify(sum(S[i, j] for j in range(n)))
                diff = simplify(row_sum - 1)
                try:
                    if abs(float(diff)) > 1e-9:
                        is_doubly_stochastic = False
                        break
                except TypeError:
                    if diff != 0:
                        is_doubly_stochastic = False
                        break
            
            if is_doubly_stochastic:
                for j in range(n):
                    col_sum = simplify(sum(S[i, j] for i in range(n)))
                    diff = simplify(col_sum - 1)
                    try:
                        if abs(float(diff)) > 1e-9:
                            is_doubly_stochastic = False
                            break
                    except TypeError:
                        if diff != 0:
                            is_doubly_stochastic = False
                            break
            
            neg_q = not is_doubly_stochastic
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is a square matrix",
    "¬Q: S is not doubly stochastic"
]

N_HYP = 1
NEG_Q_INDEX = 1