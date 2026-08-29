import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H1: A is Hermitian
    try:
        h1 = bool(witness == witness.H)
    except Exception:
        h1 = False

    # H2: A is positive definite
    try:
        h2 = (witness.is_positive_definite == True)
    except Exception:
        h2 = False

    # neg_Q: not (exists unique L ...)
    try:
        if not hasattr(witness, 'is_Matrix') or not witness.is_Matrix:
            neg_q = True
        else:
            try:
                L = witness.cholesky()
                is_lower = L.is_lower
                diag_positive = True
                for i in range(L.rows):
                    val = L[i, i]
                    if val.is_real == True and val.is_positive == True:
                        pass
                    else:
                        diag_positive = False
                        break
                
                diff = witness - L * L.H
                reconstructs = True
                for v in diff:
                    if v == 0:
                        continue
                    if sympy.expand(v) == 0:
                        continue
                    if sympy.simplify(v) == 0:
                        continue
                    reconstructs = False
                    break
                
                q = is_lower and diag_positive and reconstructs
                neg_q = not q
            except Exception:
                neg_q = True
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is Hermitian",
    "H_2: A is positive definite",
    "¬Q: A does not have a unique lower triangular Cholesky decomposition with strictly positive real diagonal entries"
]

N_HYP = 2
NEG_Q_INDEX = 2