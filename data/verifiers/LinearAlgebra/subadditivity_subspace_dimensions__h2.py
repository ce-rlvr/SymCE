import sympy
from sympy import Matrix

def conditions(witness):
    """
    Given a witness tuple (V, U, W), checks if it is a counterexample to the 
    false conjecture: "The dimension of U + W is less than or equal to dim(U) + dim(W)".
    
    The dropped hypothesis was "U is a finite-dimensional subspace of V".
    """
    try:
        V, U, W = witness
        
        # H1: V is a vector space over a field F
        # We represent V by its ambient dimension (an integer > 0)
        h1 = isinstance(V, int) and V > 0
        
        # H2: W is a finite-dimensional subspace of V
        # W is represented as a Matrix whose columns span the subspace
        h2 = isinstance(W, Matrix) and W.rows == V
        
        # Helper to compute dimension
        def get_dim(obj):
            if hasattr(obj, 'rank'):
                return obj.rank()
            if isinstance(obj, (int, float, sympy.Expr)):
                return 0
            if hasattr(obj, '__len__'):
                return len(obj)
            return 0
            
        dim_U = get_dim(U)
        dim_W = get_dim(W)
        
        # Compute U + W
        # If U is not a subspace (e.g., a scalar or an affine translation vector),
        # the standard addition might increase the rank beyond the sum of ranks.
        U_plus_W = U + W
        dim_U_plus_W = get_dim(U_plus_W)
        
        # ¬Q: The dimension of U + W is strictly greater than dim(U) + dim(W)
        neg_q = dim_U_plus_W > dim_U + dim_W
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: W is a finite-dimensional subspace of V",
    "¬Q: The dimension of U + W is strictly greater than dim(U) + dim(W)"
]

N_HYP = 2
NEG_Q_INDEX = 2

# Standard named objects for potential witness construction
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)