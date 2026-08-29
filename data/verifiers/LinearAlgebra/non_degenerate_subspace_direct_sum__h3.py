import sympy
from sympy import Matrix, zeros, eye

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        Q, W_basis = witness
    except Exception:
        return [False, False, False]
    
    # H1: V is a finite-dimensional quadratic space
    try:
        if isinstance(Q, (list, tuple)):
            Q = Matrix(Q)
        # We assume a quadratic space is equipped with a symmetric bilinear form.
        # We also require it to be non-degenerate (det != 0) as is standard for the ambient space in this theorem.
        h1 = isinstance(Q, Matrix) and Q.is_square and Q == Q.T and Q.det() != 0
        n = Q.shape[0]
    except Exception:
        h1 = False
        n = 0

    # H2: W is a subspace of V
    try:
        h2 = isinstance(W_basis, (list, tuple))
        W_mats = []
        if h2:
            for v in W_basis:
                if isinstance(v, (list, tuple)):
                    v = Matrix(v)
                if isinstance(v, Matrix) and v.shape == (1, n):
                    v = v.T
                if not (isinstance(v, Matrix) and v.shape == (n, 1)):
                    h2 = False
                    break
                W_mats.append(v)
        if h2:
            W_basis = W_mats
    except Exception:
        h2 = False

    # neg_Q: V is NOT the orthogonal direct sum of W and W^\perp
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            if len(W_basis) > 0:
                M = Matrix.hstack(*W_basis)
            else:
                M = zeros(n, 0)
            
            # W^\perp is the nullspace of M^T * Q
            eq_matrix = M.T * Q
            W_perp_basis = eq_matrix.nullspace()
            
            if len(W_basis) > 0 and len(W_perp_basis) > 0:
                combined = Matrix.hstack(M, *W_perp_basis)
            elif len(W_basis) > 0:
                combined = M
            elif len(W_perp_basis) > 0:
                combined = Matrix.hstack(*W_perp_basis)
            else:
                combined = zeros(n, 0)
                
            dim_W = M.rank()
            dim_W_perp = len(W_perp_basis)
            dim_sum = combined.rank()
            
            # V is the direct sum of W and W^\perp iff dim(W + W^\perp) == n and dim(W) + dim(W^\perp) == n
            is_direct_sum = (dim_sum == n) and (dim_W + dim_W_perp == n)
            neg_q = not is_direct_sum
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional quadratic space",
    "H_2: W is a subspace of V",
    "¬Q: V is not the orthogonal direct sum of W and W^\\perp"
]

N_HYP = 2
NEG_Q_INDEX = 2