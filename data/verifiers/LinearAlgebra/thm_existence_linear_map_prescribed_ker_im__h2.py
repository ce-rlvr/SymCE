import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # The witness can be provided as (n, U, W) where n is the dimension of V,
        # or as (V, U, W) where V, U, W are SymPy Matrices representing the spaces
        # (the column space of the matrix represents the vector space).
        if isinstance(witness[0], int):
            n = witness[0]
            if n < 0:
                return [False, False]
            V = eye(n)
            U = witness[1]
            W = witness[2]
        else:
            V, U, W = witness
            
        # Ensure V, U, W are matrix-like objects
        if not (hasattr(V, 'rank') and hasattr(V, 'rows') and hasattr(V, 'row_join')):
            return [False, False]
        if not (hasattr(U, 'rank') and hasattr(U, 'rows')):
            return [False, False]
        if not (hasattr(W, 'rank') and hasattr(W, 'rows')):
            return [False, False]
            
        # H1: V is a finite-dimensional vector space over a field F.
        # This is inherently true for finite SymPy matrices.
        h1 = True
        
        dim_V = V.rank()
        dim_U = U.rank()
        dim_W = W.rank()
        
        # Evaluate RHS of the conjecture: dim(U) + dim(W) == dim(V)
        rhs = (dim_U + dim_W == dim_V)
        
        # Evaluate LHS of the conjecture: 
        # "There exists a linear operator T in End(V) such that ker(T) = U and im(T) = W"
        # For such an operator to exist, U and W MUST be subspaces of V.
        # If they are subspaces of V, the operator exists iff dim(U) + dim(W) == dim(V).
        if U.rows != V.rows or W.rows != V.rows:
            # Ambient dimensions do not match, so U or W cannot be a subspace of V
            lhs = False
        else:
            # Check if the column spaces of U and W are contained within the column space of V
            U_in_V = (V.row_join(U).rank() == dim_V)
            W_in_V = (V.row_join(W).rank() == dim_V)
            lhs = U_in_V and W_in_V and (dim_U + dim_W == dim_V)
            
        # The conjecture claims LHS <-> RHS
        conclusion = (lhs == rhs)
        
        # The negated conclusion is True if the conjecture fails at the witness
        neg_q = not conclusion
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "¬Q: The equivalence fails (e.g., dim(U) + dim(W) = dim(V) but U or W is not a subspace of V)"
]

N_HYP = 1
NEG_Q_INDEX = 1