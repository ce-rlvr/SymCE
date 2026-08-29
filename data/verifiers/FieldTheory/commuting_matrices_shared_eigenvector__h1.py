import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Witness should be a pair of matrices (A, B)
        if not (isinstance(witness, (tuple, list)) and len(witness) == 2):
            return [False, False, False, False]
        
        A, B = witness
        if not isinstance(A, Matrix):
            A = Matrix(A)
        if not isinstance(B, Matrix):
            B = Matrix(B)
            
        # H_1: V is a vector space over K of finite dimension n >= 1
        # H_2: A and B are linear operators on V
        h1 = (A.shape[0] == A.shape[1] and A.shape[0] >= 1 and 
              B.shape[0] == B.shape[1] and A.shape == B.shape)
        h2 = h1
        
        if not h1:
            return [False, False, False, False]
            
        n = A.shape[0]
        
        # H_3: A and B commute (AB = BA)
        h3 = (A * B == B * A)
        
        # Determine the base field K from the entries of A and B.
        # If all entries are rational, K = Q. If all are real, K = R.
        is_Q = all(e.is_rational == True for e in A) and all(e.is_rational == True for e in B)
        is_R = all(e.is_real == True for e in A) and all(e.is_real == True for e in B)
        
        def in_K(val):
            if is_Q:
                return val.is_rational == True
            if is_R:
                return val.is_real == True
            return True
            
        shared_eigenvector = False
        evs_A = A.eigenvects()
        evs_B = B.eigenvects()
        
        # Check if they share an eigenvector over K
        for val_A, mult_A, vecs_A in evs_A:
            if not in_K(val_A):
                continue
            for val_B, mult_B, vecs_B in evs_B:
                if not in_K(val_B):
                    continue
                
                # An eigenvector v shared by A and B for eigenvalues val_A and val_B
                # must be in the nullspace of both (A - val_A*I) and (B - val_B*I).
                M1 = A - val_A * eye(n)
                M2 = B - val_B * eye(n)
                M_stacked = M1.col_join(M2)
                
                if len(M_stacked.nullspace()) > 0:
                    shared_eigenvector = True
                    break
            if shared_eigenvector:
                break
                
        # ¬Q: There does NOT exist a non-zero shared eigenvector in V
        neg_Q = not shared_eigenvector
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_Q)]
        
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over K of finite dimension n >= 1",
    "H_2: A and B are linear operators on V",
    "H_3: A and B commute (AB = BA)",
    "¬Q: A and B do not share a non-zero eigenvector in V"
]

N_HYP = 3
NEG_Q_INDEX = 3