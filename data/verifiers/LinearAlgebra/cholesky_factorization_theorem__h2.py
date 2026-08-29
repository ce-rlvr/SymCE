import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A is an n x n matrix with real entries
    try:
        h1 = False
        if hasattr(witness, 'is_square') and witness.is_square:
            is_real = True
            for e in witness:
                if not e.is_real:
                    is_real = False
                    break
            h1 = is_real
    except Exception:
        h1 = False

    # H_2: A is positive definite
    # For a general real matrix, this means x^T A x > 0 for all x != 0,
    # which is equivalent to its symmetric part (A + A^T)/2 being positive definite.
    try:
        h2 = False
        if hasattr(witness, 'is_square') and witness.is_square:
            A_sym = (witness + witness.T) / 2
            is_pd = True
            for i in range(1, witness.shape[0] + 1):
                det_val = A_sym[:i, :i].det()
                if not det_val.is_positive:
                    is_pd = False
                    break
            h2 = is_pd
    except Exception:
        h2 = False

    # ¬Q: There does not exist a unique lower triangular matrix L with strictly positive diagonal entries such that A = L L^T
    try:
        neg_q = False
        if hasattr(witness, 'is_square') and witness.is_square:
            # If A is not symmetric, A = L L^T is impossible since L L^T is always symmetric.
            if witness != witness.T:
                neg_q = True
            else:
                try:
                    L = witness.cholesky()
                    diag_positive = all(L[i, i].is_positive for i in range(L.shape[0]))
                    if diag_positive:
                        neg_q = False
                    else:
                        neg_q = True
                except Exception:
                    # cholesky() fails if the matrix is not positive definite
                    neg_q = True
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with real entries",
    "H_2: A is positive definite",
    "¬Q: There does not exist a unique lower triangular matrix L with strictly positive diagonal entries such that A = L L^T"
]

N_HYP = 2
NEG_Q_INDEX = 2