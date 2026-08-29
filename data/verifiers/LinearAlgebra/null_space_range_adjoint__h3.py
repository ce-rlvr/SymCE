import sympy as sp

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the hypotheses and FAILS the conclusion.
    The conjecture claims: null(T^*) = (range(T))^\perp
    """
    try:
        # A witness can be a single matrix T (assuming standard inner product)
        # or a tuple (T, G_V, G_W) where G_V and G_W are Gram matrices of the inner products.
        if isinstance(witness, tuple) and len(witness) == 3:
            T, G_V, G_W = witness
            if not (isinstance(T, sp.MatrixBase) and isinstance(G_V, sp.MatrixBase) and isinstance(G_W, sp.MatrixBase)):
                return [False, False, False]
            
            # Inner product matrices must be Hermitian and non-degenerate
            if not (G_V == G_V.H and G_W == G_W.H):
                return [False, False, False]
            if G_V.det() == 0 or G_W.det() == 0:
                return [False, False, False]
            
            h1 = True
            h2 = True
            
            # T^* = G_V^-1 T^H G_W
            T_star = G_V.inv() * T.H * G_W
            N = T_star.nullspace()
            
            # (range(T))^\perp = { x | x^H G_W y = 0 for all y in range(T) }
            # x^H G_W T = 0 => T^H G_W x = 0
            C_perp = (T.H * G_W).nullspace()
            
        elif isinstance(witness, sp.MatrixBase):
            T = witness
            h1 = True
            h2 = True
            
            # Standard inner product: T^* is the conjugate transpose
            N = T.H.nullspace()
            
            # Orthogonal complement of the column space
            C = T.columnspace()
            if len(C) == 0:
                C_perp = sp.eye(T.rows).columnspace()
            else:
                C_mat = sp.Matrix.hstack(*C)
                C_perp = C_mat.H.nullspace()
        else:
            return [False, False, False]
            
        # Helper to check if two lists of vectors span the same subspace
        def span_eq(U, V):
            if len(U) == 0 and len(V) == 0:
                return True
            if len(U) == 0:
                return sp.Matrix.hstack(*V).rank() == 0
            if len(V) == 0:
                return sp.Matrix.hstack(*U).rank() == 0
            M_U = sp.Matrix.hstack(*U)
            M_V = sp.Matrix.hstack(*V)
            M_UV = sp.Matrix.hstack(M_U, M_V)
            return M_U.rank() == M_V.rank() == M_UV.rank()
            
        # q is True if null(T^*) == (range(T))^\perp
        q = span_eq(N, C_perp)
        
        # We want the conclusion to FAIL
        neg_q = not q
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V and W are finite-dimensional inner product spaces",
    "H_2: T is a linear transformation from V to W",
    "¬Q: null(T^*) != (range(T))^\perp"
]

N_HYP = 2
NEG_Q_INDEX = 2