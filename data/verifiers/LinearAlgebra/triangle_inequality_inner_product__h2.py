import sympy as sp
from sympy.matrices import eye, zeros, Matrix

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # The witness can be either (P, x, y) where P is the inner product matrix,
        # or just (x, y) in which case the standard dot product (identity matrix) is assumed.
        if isinstance(witness, tuple):
            if len(witness) == 3:
                P, x, y = witness
            elif len(witness) == 2:
                x, y = witness
                P = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        # Ensure x and y are column vectors (SymPy Matrices)
        if not (hasattr(x, 'shape') and hasattr(x, 'H')):
            if isinstance(x, (list, tuple)):
                x = sp.Matrix(x)
            else:
                x = sp.Matrix([x])
        if not (hasattr(y, 'shape') and hasattr(y, 'H')):
            if isinstance(y, (list, tuple)):
                y = sp.Matrix(y)
            else:
                y = sp.Matrix([y])
                
        # Default to standard inner product if P is not provided
        if P is None:
            P = sp.eye(x.shape[0])
            
        # Ensure P is a SymPy Matrix
        if not (hasattr(P, 'shape') and hasattr(P, 'H')):
            if isinstance(P, (list, tuple)):
                P = sp.Matrix(P)
            else:
                P = sp.Matrix([[P]])
                
    except Exception:
        return [False, False, False]
        
    # H_1: V is an inner product space over the real or complex numbers
    # This requires the inner product matrix P to be Hermitian and positive definite.
    try:
        is_hermitian = bool(P == P.H)
        is_pos_def = bool(P.is_positive_definite)
        h1 = is_hermitian and is_pos_def
    except Exception:
        h1 = False
        
    # H_2: ||.|| denotes the norm induced by the inner product on V
    # We enforce this by definition in our evaluation of Q.
    h2 = True
    
    # Conclusion: ||x + y|| <= ||x|| + ||y||
    try:
        s = x + y
        
        def norm(v):
            val = v.H * P * v
            # The result of the inner product must be a 1x1 scalar matrix
            if hasattr(val, 'shape') and val.shape == (1, 1):
                return sp.sqrt(val[0, 0])
            else:
                raise ValueError("Inner product did not return a scalar")
                
        norm_x = norm(x)
        norm_y = norm(y)
        norm_s = norm(s)
        
        diff = norm_x + norm_y - norm_s
        
        # Check if norm_s <= norm_x + norm_y (i.e., diff >= 0)
        if hasattr(diff, 'is_nonnegative') and diff.is_nonnegative is not None:
            q = bool(diff.is_nonnegative)
        else:
            try:
                q = bool(float(diff) >= -1e-12)
            except TypeError:
                q = False
    except Exception:
        # If any operation fails (e.g., shape mismatch because x and y are not in the same space),
        # the conclusion is undefined and therefore fails.
        q = False
        
    neg_q = not q
    
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is an inner product space over the real or complex numbers",
    "H_2: ||.|| denotes the norm induced by the inner product on V",
    "¬Q: ||x + y|| <= ||x|| + ||y|| fails"
]

N_HYP = 2
NEG_Q_INDEX = 2