import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            X = witness.get('X')
        else:
            A, X = witness
            # Auto-swap if the tuple order is (X, A) instead of (A, X)
            if isinstance(A, MatrixBase) and isinstance(X, MatrixBase):
                if A.shape[0] != A.shape[1] and X.shape[0] == X.shape[1]:
                    A, X = X, A
    except Exception:
        return [False, False, False]

    # H_1: X is an n x m real matrix and A is an n x n real matrix
    try:
        h1 = False
        if isinstance(A, MatrixBase) and isinstance(X, MatrixBase):
            n, m = X.shape
            if n >= 1 and m >= 1 and A.shape == (n, n):
                if all(e.is_real is not False for e in A) and all(e.is_real is not False for e in X):
                    h1 = True
    except Exception:
        h1 = False

    # H_2: X has full column rank
    try:
        h2 = False
        if h1:
            if X.rank() == X.shape[1]:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: X^T A X is not positive definite
    try:
        neg_q = False
        if h1:
            M = X.T * A * X
            if not M.is_symmetric():
                neg_q = True
            else:
                is_pd = True
                # Sylvester's criterion: all leading principal minors must be strictly positive
                for i in range(1, M.shape[0] + 1):
                    det_val = M[:i, :i].det()
                    try:
                        if float(det_val) <= 0:
                            is_pd = False
                            break
                    except TypeError:
                        # Fallback for symbolic determinants
                        if det_val.is_positive is False or det_val.is_nonpositive is True:
                            is_pd = False
                            break
                neg_q = not is_pd
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X is an n x m real matrix and A is an n x n real matrix",
    "H_2: X has full column rank",
    "¬Q: X^T A X is not positive definite"
]

N_HYP = 2
NEG_Q_INDEX = 2