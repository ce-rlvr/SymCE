import sympy
from sympy import eye, zeros, Matrix

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def has_common_eigenvector(A, B):
    """
    Checks if matrices A and B share a common real eigenvector.
    Since the theorem fails specifically when the field is not algebraically closed,
    we look for eigenvectors over the reals.
    """
    n = A.shape[0]
    I = eye(n)
    
    evA = A.eigenvals()
    evB = B.eigenvals()
    
    real_evA = []
    for val in evA:
        if val.is_real:
            real_evA.append(val)
        elif val.is_real is None:
            try:
                if abs(sympy.im(val).evalf()) < 1e-9:
                    real_evA.append(val)
            except Exception:
                pass
                
    real_evB = []
    for val in evB:
        if val.is_real:
            real_evB.append(val)
        elif val.is_real is None:
            try:
                if abs(sympy.im(val).evalf()) < 1e-9:
                    real_evB.append(val)
            except Exception:
                pass
                
    for a in real_evA:
        for b in real_evB:
            # The intersection of the eigenspaces is the nullspace of the stacked matrix
            M = (A - a*I).col_join(B - b*I)
            if len(M.nullspace()) > 0:
                return True
    return False

def conditions(witness) -> list[bool]:
    try:
        A, B = witness
        if not hasattr(A, 'shape') or not hasattr(B, 'shape'):
            return [False, False]
        if A.shape[0] != A.shape[1] or B.shape[0] != B.shape[1] or A.shape != B.shape:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        h1_ok = bool(A * B == B * A)
    except Exception:
        h1_ok = False
        
    try:
        # neg_Q: There does NOT exist a common eigenvector (over the reals)
        neg_q_ok = not has_common_eigenvector(A, B)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: AB = BA",
    "¬Q: A and B do not share a common real eigenvector"
]

N_HYP = 1
NEG_Q_INDEX = 1