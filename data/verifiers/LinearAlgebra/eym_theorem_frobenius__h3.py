import sympy
from sympy import Matrix, eye, simplify, zeros
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_mat(M):
    for x in M:
        if x != 0 and simplify(x) != 0:
            return False
    return True

def conditions(witness):
    try:
        A, U, Sigma, V, k = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: A is an m x n complex matrix
    try:
        h1 = hasattr(A, 'is_Matrix') and A.is_Matrix
        m, n = A.shape
    except Exception:
        h1 = False

    # H2: A = U \Sigma V^* is the SVD of A
    try:
        h2 = False
        if (hasattr(U, 'is_Matrix') and U.is_Matrix and 
            hasattr(V, 'is_Matrix') and V.is_Matrix and 
            hasattr(Sigma, 'is_Matrix') and Sigma.is_Matrix):
            if U.shape == (m, m) and V.shape == (n, n) and Sigma.shape == (m, n):
                # Check unitary
                U_is_unitary = is_zero_mat(U * U.H - eye(m))
                V_is_unitary = is_zero_mat(V * V.H - eye(n))
                if U_is_unitary and V_is_unitary:
                    # Check diagonal and non-negative
                    is_diag = True
                    for i in range(m):
                        for j in range(n):
                            val = Sigma[i, j]
                            if i == j:
                                try:
                                    if not bool(val >= 0):
                                        is_diag = False
                                except Exception:
                                    is_diag = False
                            else:
                                if val != 0 and simplify(val) != 0:
                                    is_diag = False
                    if is_diag:
                        # Check A == U * Sigma * V.H
                        if is_zero_mat(A - U * Sigma * V.H):
                            h2 = True
    except Exception:
        h2 = False

    # H3: A_k is the truncated SVD (k is a valid integer)
    try:
        h3 = isinstance(k, int) and 1 <= k <= min(m, n)
    except Exception:
        h3 = False

    # neg_Q: A_k does NOT minimize the Frobenius norm
    try:
        S = [Sigma[i, i] for i in range(min(m, n))]
        error_Ak_sq = sum(s**2 for s in S[k:])
        sorted_S_sq = sorted([s**2 for s in S])
        true_min_error_sq = sum(sorted_S_sq[:min(m, n) - k]) if min(m, n) > k else 0
        
        diff = simplify(error_Ak_sq - true_min_error_sq)
        try:
            neg_q = bool(diff > 0)
        except TypeError:
            neg_q = float(diff) > 1e-9
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n complex matrix",
    "H_2: A = U Sigma V^* is the singular value decomposition of A",
    "H_3: A_k is the truncated SVD of A for some integer k",
    "¬Q: A_k does not minimize the Frobenius norm over rank k matrices"
]

N_HYP = 3
NEG_Q_INDEX = 3