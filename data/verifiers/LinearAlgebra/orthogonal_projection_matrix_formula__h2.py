import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H1: A is an n by k real matrix
    try:
        h1 = False
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            h1 = True
            for x in witness:
                if hasattr(x, 'is_real') and x.is_real:
                    continue
                if isinstance(x, (int, float)):
                    continue
                h1 = False
                break
    except Exception:
        h1 = False

    # neg_Q: The matrix P = A(A^T A)^{-1} A^T is NOT the orthogonal projection operator onto the column space of A
    try:
        neg_q = False
        if not (hasattr(witness, 'is_Matrix') and witness.is_Matrix):
            neg_q = True
        else:
            A = witness
            ATA = A.T * A
            
            try:
                ATA_inv = ATA.inv()
            except Exception:
                # If A^T A is not invertible, the formula is undefined and thus fails to be the projection matrix
                neg_q = True
            else:
                P = A * ATA_inv * A.T
                is_proj = True
                
                # P must be symmetric
                if P != P.T:
                    is_proj = False
                # P must be idempotent
                elif P * P != P:
                    is_proj = False
                # Col(P) must be Col(A), which implies P * A == A
                elif P * A != A:
                    is_proj = False
                
                neg_q = not is_proj
    except Exception:
        # Any failure in computation means the formula does not yield the valid projection matrix
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n by k real matrix",
    "¬Q: The matrix P = A(A^T A)^{-1} A^T is not the orthogonal projection operator onto the column space of A"
]

N_HYP = 1
NEG_Q_INDEX = 1