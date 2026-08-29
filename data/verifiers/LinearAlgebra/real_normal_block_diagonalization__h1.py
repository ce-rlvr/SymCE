import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A = witness
        if not isinstance(A, sp.MatrixBase):
            return [False, False]
        if not A.is_square:
            return [False, False]
            
        diff = (A * A.T) - (A.T * A)
        H1 = all(sp.simplify(elem) == 0 for elem in diff)
    except Exception:
        H1 = False

    try:
        if not isinstance(A, sp.MatrixBase) or not A.is_square:
            neg_Q = False
        else:
            # The conclusion states that A can be block-diagonalized into real 1x1 blocks 
            # and real 2x2 normal blocks by a real orthogonal matrix.
            # This is exactly the Spectral Theorem for Real Normal Matrices.
            # Thus, the conclusion holds if and only if A is a real normal matrix.
            is_real = True
            for elem in A:
                if sp.simplify(sp.im(elem)) != 0:
                    is_real = False
                    break
                    
            diff = (A * A.T) - (A.T * A)
            is_normal = all(sp.simplify(elem) == 0 for elem in diff)
            
            conclusion = is_real and is_normal
            neg_Q = not conclusion
    except Exception:
        neg_Q = False
        
    return [bool(H1), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: A is normal (A A^T = A^T A)",
    "¬Q: A cannot be block-diagonalized into real 1x1 or 2x2 normal blocks by a real orthogonal matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1