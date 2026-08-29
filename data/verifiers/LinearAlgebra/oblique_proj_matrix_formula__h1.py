import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for linear algebra
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Witness should be a tuple of two matrices: (U, W)
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        U, W = witness
    except Exception:
        return [False, False, False]
        
    try:
        if not isinstance(U, Matrix) or not isinstance(W, Matrix):
            return [False, False, False]
            
        n, k = U.shape
        if W.shape != (n, k):
            return [False, False, False]
            
        if n < 1 or k < 1:
            return [False, False, False]
            
        # H_1: U is an n x k matrix whose columns form a basis for M
        # This means U must have full column rank (rank == k)
        try:
            h1 = bool(U.rank() == k)
        except Exception:
            h1 = False
            
        # H_2: W is an n x k matrix whose columns form a basis for N^\perp
        # This means W must have full column rank (rank == k)
        try:
            h2 = bool(W.rank() == k)
        except Exception:
            h2 = False
            
        # ¬Q: The conclusion fails if the formula U(W^T U)^{-1} W^T is undefined.
        # This occurs exactly when W^T U is not invertible (determinant is zero).
        try:
            WT_U = W.T * U
            det_val = WT_U.det()
            if hasattr(det_val, 'is_zero') and det_val.is_zero is not None:
                neg_q = bool(det_val.is_zero)
            else:
                neg_q = bool(sympy.simplify(det_val) == 0)
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: U is an n x k matrix with full column rank (basis for M)",
    "H_2: W is an n x k matrix with full column rank (basis for N^perp)",
    "¬Q: The formula U(W^T U)^{-1} W^T is undefined (W^T U is not invertible)"
]

N_HYP = 2
NEG_Q_INDEX = 2