import sympy
from sympy import Matrix, zeros, eye
from sympy.abc import x, y, z

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero(val):
    if val == 0:
        return True
    if hasattr(val, 'is_zero') and val.is_zero:
        return True
    try:
        if sympy.expand(val) == 0:
            return True
    except Exception:
        pass
    return False

def conditions(witness):
    try:
        A = witness
        # Ensure the witness is a square matrix
        if not hasattr(A, 'shape') or len(A.shape) != 2 or A.shape[0] != A.shape[1]:
            return [False]
        
        n = A.shape[0]
        if n == 0:
            return [False]
            
        # Check if A is nilpotent (A^n == 0)
        A_n = A**n
        is_nilp = True
        for i in range(n):
            for j in range(n):
                if not is_zero(A_n[i, j]):
                    is_nilp = False
                    break
            if not is_nilp:
                break
                
        # Check if Tr(A^k) == 0 for all k=1..n
        traces_zero = True
        A_k = A
        for k in range(1, n + 1):
            if not is_zero(A_k.trace()):
                traces_zero = False
                break
            if k < n:
                A_k = A_k * A
                
        # The conclusion is the equivalence: A is nilpotent <=> Tr(A^k) = 0 for all k=1..n
        # The negated conclusion means the equivalence fails.
        neg_Q = (is_nilp != traces_zero)
        
        return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence (A is nilpotent <=> Tr(A^k) = 0 for all k=1..n) fails"
]
N_HYP = 0
NEG_Q_INDEX = 0