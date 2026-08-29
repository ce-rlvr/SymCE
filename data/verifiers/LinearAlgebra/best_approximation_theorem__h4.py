import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is that P_W(v) is the ORTHOGONAL projection.
    Without it, P_W(v) can be any valid projection of v onto W, which may not minimize distance.
    
    Expected witness structure: (W_basis, v, w, P_W_v)
    where:
      - W_basis is a list of basis vectors for W (or a matrix whose columns span W)
      - v is a vector in V
      - w is a vector in W
      - P_W_v is the projection of v onto W
    """
    try:
        if isinstance(witness, dict):
            W_basis = witness.get('W_basis', [])
            v = witness['v']
            w = witness['w']
            P_W_v = witness['P_W_v']
        else:
            W_basis, v, w, P_W_v = witness
            
        # Ensure v, w, P_W_v are column matrices
        v = Matrix(v)
        if v.shape[0] == 1:
            v = v.T
        w = Matrix(w)
        if w.shape[0] == 1:
            w = w.T
        P_W_v = Matrix(P_W_v)
        if P_W_v.shape[0] == 1:
            P_W_v = P_W_v.T
            
        n = v.shape[0]
        
        # Construct the matrix W_mat whose columns span W
        if isinstance(W_basis, Matrix):
            W_mat = W_basis
        elif len(W_basis) > 0:
            if isinstance(W_basis[0], (list, tuple, Matrix)):
                cols = []
                for b in W_basis:
                    mb = Matrix(b)
                    if mb.shape[0] == 1:
                        mb = mb.T
                    cols.append(mb)
                W_mat = Matrix.hstack(*cols)
            else:
                W_mat = Matrix(W_basis)
                if W_mat.shape[0] == 1:
                    W_mat = W_mat.T
        else:
            W_mat = Matrix.zeros(n, 1)
            
        # H_1: V is an inner product space
        # We model V as R^n (or C^n) with the standard inner product.
        # We just verify that all vectors belong to the same space.
        h1 = (n >= 1) and (W_mat.shape[0] == n) and (w.shape == (n, 1)) and (P_W_v.shape == (n, 1))
        
        # H_2: W is a finite-dimensional subspace of V
        # True by construction (span of finite vectors in R^n).
        h2 = True
        
        # H_3: v is a vector in V
        # True by construction.
        h3 = True
        
        # H_4: w is a vector in W such that w != P_W(v)
        # Check if w is in W
        w_in_W = W_mat.rank() == Matrix.hstack(W_mat, w).rank()
        
        # Check if P_W_v is a valid projection of v onto W
        # 1. P_W_v must be in W
        p_in_W = W_mat.rank() == Matrix.hstack(W_mat, P_W_v).rank()
        # 2. If v is already in W, its projection onto W must be itself
        v_in_W = W_mat.rank() == Matrix.hstack(W_mat, v).rank()
        valid_proj = p_in_W and (not v_in_W or P_W_v == v)
        
        w_neq_p = (w != P_W_v)
        
        h4 = w_in_W and valid_proj and w_neq_p
        
        # ¬Q: ||v - P_W(v)|| >= ||v - w||
        diff_p = v - P_W_v
        diff_w = v - w
        
        # Compute squared norms (handling potential complex numbers safely)
        norm_p_sq = sum(x * sympy.conjugate(x) for x in diff_p)
        norm_w_sq = sum(x * sympy.conjugate(x) for x in diff_w)
        
        try:
            val_p = complex(norm_p_sq).real
            val_w = complex(norm_w_sq).real
            neg_q = val_p >= val_w
        except TypeError:
            # Fallback for symbolic expressions
            neg_q = bool(sympy.simplify(norm_p_sq - norm_w_sq) >= 0)
            
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: V is an inner product space",
    "H_2: W is a finite-dimensional subspace of V",
    "H_3: v is a vector in V",
    "H_4: w is a vector in W such that w != P_W(v)",
    "¬Q: ||v - P_W(v)|| >= ||v - w||"
]

N_HYP = 4
NEG_Q_INDEX = 4