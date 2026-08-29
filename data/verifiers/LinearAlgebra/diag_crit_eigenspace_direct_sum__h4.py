import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            T, W_list = witness
        elif isinstance(witness, sp.Matrix):
            T = witness
            n = T.shape[0]
            eigenvals = T.eigenvals()
            W_list = []
            for lam in eigenvals.keys():
                mat = (T - lam * sp.eye(n))**n
                W_list.append(mat.nullspace())
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: V is a finite-dimensional vector space over a field F
    try:
        h1 = isinstance(T, sp.Matrix) and T.is_square
    except Exception:
        h1 = False

    # H_2: T is a linear operator on V
    try:
        h2 = h1
    except Exception:
        h2 = False

    # H_3: lambda_1, ..., lambda_k are the distinct eigenvalues of T
    try:
        if h1:
            eigenvals = T.eigenvals()
            h3 = len(W_list) == len(eigenvals)
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: T is diagonalizable if and only if V is the direct sum of W_1, W_2, ..., W_k
    try:
        if not h1:
            neg_q = False
        else:
            n = T.shape[0]
            is_diag = T.is_diagonalizable()

            all_vectors = []
            total_dim = 0
            for W in W_list:
                total_dim += len(W)
                all_vectors.extend(W)

            if total_dim == n and len(all_vectors) == n:
                if n == 0:
                    is_direct_sum = True
                else:
                    M = sp.Matrix.hstack(*all_vectors)
                    is_direct_sum = (M.rank() == n)
            else:
                is_direct_sum = False

            # The conclusion Q is: is_diag == is_direct_sum
            # We want the negation of Q, which is: is_diag != is_direct_sum
            neg_q = bool(is_diag != is_direct_sum)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: T is a linear operator on V",
    "H_3: lambda_1, ..., lambda_k are the distinct eigenvalues of T",
    "¬Q: T is not (diagonalizable if and only if V is the direct sum of W_1, W_2, ..., W_k)"
]

N_HYP = 3
NEG_Q_INDEX = 3