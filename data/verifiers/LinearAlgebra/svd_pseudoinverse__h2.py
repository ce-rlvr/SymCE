import sympy
from sympy import Matrix, zeros, eye, simplify
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, U, Sigma, V = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(A, MatrixBase)
        m, n = A.shape
    except Exception:
        h1 = False

    try:
        h2 = (isinstance(Sigma, MatrixBase) and Sigma.shape == (m, n) and
              all(Sigma[i, j] == 0 for i in range(m) for j in range(n) if i != j) and
              isinstance(U, MatrixBase) and U.shape == (m, m) and
              isinstance(V, MatrixBase) and V.shape == (n, n))
    except Exception:
        h2 = False

    try:
        Sigma_plus = zeros(n, m)
        for i in range(min(m, n)):
            if Sigma[i, i] != 0:
                Sigma_plus[i, i] = 1 / Sigma[i, i]
                
        A_plus = A.pinv()
        rhs = V * Sigma_plus * U.H
        
        diff = A_plus - rhs
        is_zero = True
        for i in range(n):
            for j in range(m):
                if simplify(diff[i, j]) != 0:
                    is_zero = False
                    break
            if not is_zero:
                break
        neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "H_2: Sigma^+ is the n x m diagonal matrix formed by replacing non-zero diagonal entries of Sigma with reciprocals and transposing",
    "¬Q: The Moore-Penrose pseudoinverse of A is NOT given by A^+ = V Sigma^+ U^*"
]

N_HYP = 2
NEG_Q_INDEX = 2