import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False]
        A, B = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = isinstance(A, Matrix) and isinstance(B, Matrix) and \
             A.shape == B.shape and A.shape[0] == A.shape[1] and A.shape[0] >= 1
    except Exception:
        h1 = False

    neg_q = False
    try:
        if h1:
            n = A.shape[0]
            eigs_A = A.eigenvects()
            eigs_B = B.eigenvects()
            
            sum_mult_A = sum(mult for val, mult, basis in eigs_A)
            sum_mult_B = sum(mult for val, mult, basis in eigs_B)
            
            if sum_mult_A == n and sum_mult_B == n:
                shared = False
                for valA, multA, basisA in eigs_A:
                    for valB, multB, basisB in eigs_B:
                        mat = Matrix.hstack(*(basisA + basisB))
                        if mat.rank() < len(basisA) + len(basisB):
                            shared = True
                            break
                    if shared:
                        break
                neg_q = not shared
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are square matrices of the same size n >= 1",
    "¬Q: A and B do not share an eigenvector"
]
N_HYP = 1
NEG_Q_INDEX = 1