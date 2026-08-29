import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        A, P = witness
    except Exception:
        return [False, False, False]

    def is_pos_def(X):
        if not getattr(X, 'is_square', False):
            return False
        if not getattr(X, 'is_symmetric', lambda: False)():
            return False
        for i in range(1, X.rows + 1):
            det_val = X[:i, :i].det()
            try:
                if float(det_val) <= 0:
                    return False
            except TypeError:
                if det_val.is_positive is not True:
                    return False
        return True

    # H1: A is an n x n real symmetric matrix and P is a compatible real matrix
    try:
        h1 = (hasattr(A, 'is_square') and hasattr(P, 'rows') and
              A.is_square and A.is_symmetric() and
              A.rows == P.rows and
              all(getattr(x, 'is_real', False) for x in A) and
              all(getattr(x, 'is_real', False) for x in P))
    except Exception:
        h1 = False

    # H2: A is positive definite
    try:
        h2 = is_pos_def(A)
    except Exception:
        h2 = False

    # ¬Q: P^T A P is not positive definite
    try:
        M = P.T * A * P
        neg_q = not is_pos_def(M)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n real symmetric matrix and P is a compatible real matrix",
    "H_2: A is positive definite",
    "¬Q: P^T A P is not positive definite"
]

N_HYP = 2
NEG_Q_INDEX = 2