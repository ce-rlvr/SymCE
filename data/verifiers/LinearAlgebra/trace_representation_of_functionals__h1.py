import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Witness can be (V_basis, f_or_F) or (n, V_basis, f_or_F)
        if isinstance(witness, tuple):
            if len(witness) == 2:
                V_basis, f_or_F = witness
            elif len(witness) == 3:
                _, V_basis, f_or_F = witness
            else:
                return [False, False]
        else:
            return [False, False]
            
        if not isinstance(V_basis, list) or len(V_basis) == 0:
            return [False, False]
            
        if not hasattr(V_basis[0], 'shape') or len(V_basis[0].shape) != 2:
            return [False, False]
            
        n = V_basis[0].shape[0]
        if V_basis[0].shape[1] != n:
            return [False, False]
            
        h1_ok = True
        for M in V_basis:
            if not hasattr(M, 'shape') or M.shape != (n, n):
                h1_ok = False
                break
                
        if callable(f_or_F):
            f = f_or_F
        elif hasattr(f_or_F, 'shape') and f_or_F.shape == (n, n):
            f = lambda A, F_mat=f_or_F: sympy.trace(F_mat * A)
        else:
            h1_ok = False
            
        if h1_ok:
            # Check linearity of f on V
            for A in V_basis:
                for B in V_basis:
                    val1 = f(2*A + 3*B)
                    val2 = 2*f(A) + 3*f(B)
                    if sympy.simplify(val1 - val2) != 0:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    if not h1_ok:
        return [False, False]
        
    try:
        # Find a linearly independent basis for V
        vecs = [sympy.Matrix(1, n*n, list(M)) for M in V_basis]
        BasisMat = sympy.Matrix(vecs)
        _, pivot_cols = BasisMat.T.rref()
        
        indep_basis = [V_basis[i] for i in pivot_cols]
        dim = len(indep_basis)
        
        # Construct the Gram matrix for the trace inner product on V
        M_gram = sympy.zeros(dim, dim)
        for i in range(dim):
            for j in range(dim):
                M_gram[i, j] = sympy.trace(indep_basis[i] * indep_basis[j])
                
        # The conclusion states there exists a UNIQUE matrix B in V such that f(A) = tr(BA).
        # This holds if and only if the Gram matrix is invertible.
        # Therefore, the conclusion fails (neg_Q is True) iff the determinant is 0.
        det_val = sympy.simplify(M_gram.det())
        neg_q_ok = (det_val == 0)
        
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: f is a linear functional on V",
    "¬Q: There does not exist a unique matrix B in V such that f(A) = tr(BA) for all A in V"
]

N_HYP = 1
NEG_Q_INDEX = 1