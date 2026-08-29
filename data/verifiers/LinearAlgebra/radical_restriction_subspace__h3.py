import sympy
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is "W is a subspace of V".
    The witness should be a tuple (B, W) where B is a symmetric matrix representing
    the bilinear form, and W is a list of vectors representing a subset of V.
    """
    try:
        B, W = witness
    except Exception:
        return [False, False, False]
        
    # H_1: V is a vector space over a field F
    try:
        n = B.shape[0]
        if isinstance(W, (list, tuple)):
            h1 = B.shape[0] == B.shape[1] and all(w.shape == (n, 1) for w in W)
        elif isinstance(W, sympy.Matrix):
            h1 = B.shape[0] == B.shape[1] and W.shape[0] == n
        else:
            h1 = False
    except Exception:
        h1 = False
        
    # H_2: B is a symmetric bilinear form on V
    try:
        h2 = B.is_symmetric()
    except Exception:
        h2 = False
        
    # ¬Q: The radical of the restriction of B to W is not equal to W \cap W^\perp
    try:
        if isinstance(W, sympy.Matrix):
            # If W is provided as a matrix, it represents a subspace (its column space).
            # The theorem is true for any subspace, so the conclusion holds (not a counterexample).
            neg_q = False
        elif isinstance(W, (list, tuple)):
            # W is a subset (list of vectors).
            if not W:
                W_mat = sympy.zeros(n, 1)
            else:
                W_mat = sympy.Matrix.hstack(*W)
                
            # LHS: radical of B restricted to span(W)
            null_basis = (W_mat.T * B * W_mat).nullspace()
            LHS_basis = [W_mat * x for x in null_basis]
            
            # RHS: W \cap W^\perp
            RHS = []
            for w in W:
                is_in_perp = True
                for y in W:
                    if (w.T * B * y)[0, 0] != 0:
                        is_in_perp = False
                        break
                if is_in_perp:
                    RHS.append(w)
                    
            # Check equality between LHS (a subspace) and RHS (a finite subset)
            lhs_is_zero = all(v.is_zero_matrix for v in LHS_basis)
            rhs_has_zero = any(v.is_zero_matrix for v in RHS)
            rhs_has_nonzero = any(not v.is_zero_matrix for v in RHS)
            
            if lhs_is_zero:
                # LHS is {0}. It equals RHS iff RHS is exactly {0}.
                if rhs_has_zero and not rhs_has_nonzero:
                    is_equal = True
                else:
                    is_equal = False
            else:
                # LHS has dimension > 0, so it is infinite (over fields like QQ or RR).
                # RHS is a finite subset, so they cannot be equal.
                is_equal = False
                
            neg_q = not is_equal
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: B is a symmetric bilinear form on V",
    "¬Q: The radical of the restriction of B to W is not equal to W \\cap W^\\perp"
]

N_HYP = 2
NEG_Q_INDEX = 2