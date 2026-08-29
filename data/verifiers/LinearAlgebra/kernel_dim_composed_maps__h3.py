import sympy as sp

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: U, V, and W are finite-dimensional vector spaces",
    "H_2: T: U -> V is a linear map",
    "¬Q: dim(ker(S ∘ T)) != dim(ker(T)) + dim(im(T) ∩ ker(S))"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Expects witness to be a tuple (T, S) where:
      - T is a sympy Matrix representing a linear map from U to V.
      - S is an affine map from V to W, represented either as a callable, 
        a sympy Matrix (for linear maps), or a tuple (A, b) for S(y) = A*y + b.
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
            
        T, S = witness
        
        if not hasattr(T, 'is_Matrix'):
            return [False, False, False]
            
        n = T.shape[1]
        m = T.shape[0]
        
        if isinstance(S, tuple) and len(S) == 2:
            A, b = S
            if not (hasattr(A, 'is_Matrix') and hasattr(b, 'is_Matrix')):
                return [False, False, False]
            S_func = lambda y: A * y + b
        elif callable(S):
            S_func = S
        elif hasattr(S, 'is_Matrix'):
            S_func = lambda y: S * y
        else:
            return [False, False, False]
            
        # H1 and H2 are trivially satisfied by the matrix representation over a field
        H1 = True
        H2 = True
        
        ker_T_basis = T.nullspace()
        dim_ker_T = len(ker_T_basis)
        
        y_vars = sp.symbols(f'y1:{m+1}')
        y_vec = sp.Matrix(y_vars)
        
        S_y = S_func(y_vec)
        if not hasattr(S_y, 'is_Matrix'):
            if isinstance(S_y, (list, tuple)):
                S_y = sp.Matrix(S_y)
            else:
                S_y = sp.Matrix([S_y])
                
        if S_y.shape[1] != 1:
            S_y = sp.Matrix(list(S_y))
            
        x_vars = sp.symbols(f'x1:{n+1}')
        x_vec = sp.Matrix(x_vars)
        y_in_im = T * x_vec
        
        S_T_x = S_y.subs(dict(zip(y_vars, y_in_im)))
        
        if n == 0:
            M = sp.zeros(S_T_x.shape[0], 0)
        else:
            M = S_T_x.jacobian(x_vec)
            
        c = -S_T_x.subs({x: 0 for x in x_vars})
        
        # Verify that S is indeed an affine map
        diff = sp.simplify(M * x_vec - c - S_T_x)
        if not diff.is_zero_matrix and not all(e == 0 for e in diff):
            return [False, False, False]
            
        M_aug = M.row_join(c)
        
        # Compute the span dimension of the affine solution spaces
        if M.rank() < M_aug.rank():
            # No solution, intersection is empty, span dimension is 0
            dim_ker_ST = 0
            dim_im_T_cap_ker_S = 0
        else:
            sol, params = M.gauss_jordan_solve(c)
            x_p = sol.subs({p: 0 for p in params})
            null_basis = M.nullspace()
            
            if not null_basis:
                dim_ker_ST = x_p.rank()
                dim_im_T_cap_ker_S = (T * x_p).rank()
            else:
                vectors = [x_p] + null_basis
                span_matrix = vectors[0].row_join(*vectors[1:])
                dim_ker_ST = span_matrix.rank()
                
                vectors_T = [T * x_p] + [T * nb for nb in null_basis]
                span_matrix_T = vectors_T[0].row_join(*vectors_T[1:])
                dim_im_T_cap_ker_S = span_matrix_T.rank()
                
        LHS = dim_ker_ST
        RHS = dim_ker_T + dim_im_T_cap_ker_S
        
        neg_Q = bool(LHS != RHS)
        
        return [H1, H2, neg_Q]
        
    except Exception:
        return [False, False, False]