import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    H1 = False
    H2 = False
    neg_Q = False
    
    try:
        A, B = witness
        if hasattr(A, 'is_Matrix') and A.is_Matrix and hasattr(B, 'is_Matrix') and B.is_Matrix:
            if A.shape == B.shape and A.rows == A.cols:
                if A.is_symmetric() and B.is_symmetric():
                    if all(x.is_real for x in A) and all(x.is_real for x in B):
                        H1 = True
    except Exception:
        pass

    try:
        if H1:
            A, B = witness
            res = B.is_positive_definite
            if res is not None:
                H2 = bool(res)
            else:
                evs = B.eigenvals().keys()
                is_pd = True
                for e in evs:
                    try:
                        if not bool(e > 0):
                            is_pd = False
                            break
                    except TypeError:
                        is_pd = False
                        break
                H2 = is_pd
    except Exception:
        pass

    try:
        if H1:
            A, B = witness
            A_inv = A.inv()
            B_inv = B.inv()
            M = B_inv - A_inv
            
            res = M.is_positive_semidefinite
            if res is not None:
                neg_Q = not bool(res)
            else:
                evs = M.eigenvals().keys()
                has_negative = False
                for e in evs:
                    try:
                        if bool(e < 0):
                            has_negative = True
                            break
                    except TypeError:
                        pass
                neg_Q = has_negative
    except Exception:
        pass

    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: A and B are n x n real symmetric matrices",
    "H_2: B is positive definite",
    "¬Q: B^{-1} - A^{-1} is not positive semidefinite"
]

N_HYP = 2
NEG_Q_INDEX = 2