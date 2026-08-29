import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # The witness is expected to be a tuple (V, W) representing the vector spaces.
        # They can be given as sympy Matrices (where columns or rows span the space)
        # or lists of vectors.
        V_input, W_input = witness
        
        if not isinstance(V_input, sympy.MatrixBase):
            V = Matrix(V_input)
        else:
            V = V_input
            
        if not isinstance(W_input, sympy.MatrixBase):
            W = Matrix(W_input)
        else:
            W = W_input
            
        # Determine how to join the matrices to find the dimension of V + W.
        # If they have the same number of columns but different rows, they are likely row vectors.
        if V.cols == W.cols and V.rows != W.rows:
            V_plus_W = V.col_join(W)
        # If they have the same number of rows, they are likely column vectors.
        elif V.rows == W.rows:
            V_plus_W = V.row_join(W)
        # If they have the same shape, row_join is safe.
        elif V.cols == W.cols and V.rows == W.rows:
            V_plus_W = V.row_join(W)
        else:
            return [False, False]
            
        # H_1: V is a finite-dimensional vector space over a field F.
        # Any matrix over a field represents a finite-dimensional vector space.
        h1 = True
        
        dim_V = V.rank()
        dim_W = W.rank()
        
        # Dimension of the sum space V + W
        dim_V_plus_W = V_plus_W.rank()
        
        # Dimension of the intersection V \cap W
        dim_V_cap_W = dim_V + dim_W - dim_V_plus_W
        
        # Dimension of the quotient space V / W
        # In the general case where W might not be a subspace of V, 
        # V / W is standardly interpreted as V / (V \cap W).
        dim_V_mod_W = dim_V - dim_V_cap_W
        
        # ¬Q: The dimension of the quotient space V/W is NOT equal to dim(V) - dim(W)
        neg_q = (dim_V_mod_W != dim_V - dim_W)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "¬Q: The dimension of the quotient space V/W is not equal to dim(V) - dim(W)"
]

N_HYP = 1
NEG_Q_INDEX = 1