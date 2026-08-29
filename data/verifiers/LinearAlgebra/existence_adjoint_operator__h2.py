import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, Matrix):
            B = witness
            T = eye(B.shape[0])
        elif isinstance(witness, dict):
            B = witness.get('B')
            T = witness.get('T')
            if T is None and isinstance(B, Matrix):
                T = eye(B.shape[0])
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            B, T = witness
        else:
            return [False, False, False]
            
        if not (isinstance(B, Matrix) and isinstance(T, Matrix)):
            return [False, False, False]
            
        if B.shape[0] != B.shape[1] or T.shape[0] != T.shape[1]:
            return [False, False, False]
            
        if B.shape != T.shape:
            return [False, False, False]
            
        n = B.shape[0]
        
        # H_1: V is a finite-dimensional vector space
        # Represented by the matrices being n x n
        h1 = True
        
        # H_2: T is a linear operator on V
        # Represented by T being an n x n matrix
        h2 = True
        
        # ¬Q: There does not exist a unique adjoint operator T*
        # The equation for T* is T^T * B = B * T*
        # This has a unique solution for T* if and only if B is invertible.
        # If B is not invertible, it either has no solution or infinitely many solutions.
        # Thus, the conclusion fails (neg_q is True) iff B is not invertible.
        neg_q = bool(B.det() == 0) and (n > 0)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "H_2: T is a linear operator on V",
    "¬Q: There does not exist a unique adjoint operator T*"
]

N_HYP = 2
NEG_Q_INDEX = 2