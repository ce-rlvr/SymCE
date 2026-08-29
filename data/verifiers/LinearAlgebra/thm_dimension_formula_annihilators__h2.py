import sympy
from sympy import Matrix

# Top-level setup: named object bindings that the witness expression may reference.
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Expected witness format:
    A tuple (V_dim, W_basis, W_translation) representing an affine subspace W in V, where:
      - V_dim (int): dimension of the vector space V.
      - W_basis (list of sympy.Matrix): basis vectors for the parallel subspace of W.
      - W_translation (sympy.Matrix): translation vector for the affine subspace W.
      
    This counterexample exploits the dropped hypothesis "W is a subspace of V".
    When W is an affine subspace not containing the origin, the dimension formula fails.
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False]
            
        V_dim, W_basis, W_translation = witness
        
        # H1: V is a finite-dimensional vector space over a field F
        h1 = isinstance(V_dim, int) and V_dim >= 0
        
        # H2: W^0 is the annihilator of W in the dual space V^*
        # We verify that W is a valid affine subspace of V
        h2 = True
        if not isinstance(W_translation, Matrix) or W_translation.shape != (V_dim, 1):
            h2 = False
        if not isinstance(W_basis, list):
            h2 = False
        else:
            for b in W_basis:
                if not isinstance(b, Matrix) or b.shape != (V_dim, 1):
                    h2 = False
                    
        if not (h1 and h2):
            return [h1, h2, False]
            
        # Compute dim(W)
        # The dimension of an affine subspace is the dimension of its parallel vector subspace.
        if W_basis:
            W_mat = Matrix.hstack(*W_basis)
            dim_W = W_mat.rank()
        else:
            dim_W = 0
            
        # Compute dim(W^0)
        # W^0 is the annihilator of W.
        # A linear functional f annihilates W iff it annihilates span(W_basis) and W_translation.
        span_W = W_basis + [W_translation]
        span_mat = Matrix.hstack(*span_W)
        dim_span_W = span_mat.rank()
        
        dim_W0 = V_dim - dim_span_W
        
        # Conclusion: dim(W) + dim(W^0) == dim(V)
        # Negated conclusion: dim(W) + dim(W^0) != dim(V)
        neg_q = (dim_W + dim_W0) != V_dim
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: W^0 is the annihilator of W in the dual space V^*",
    "¬Q: dim(W) + dim(W^0) != dim(V)"
]

N_HYP = 2
NEG_Q_INDEX = 2