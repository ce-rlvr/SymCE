import sympy
from sympy import Matrix, expand, symbols, eye, zeros

# Top-level setup for standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: \mathcal{B} is a basis for V",
    "H_2: B is a bilinear form on V",
    "H_3: M is the Gram matrix of B with respect to the basis \mathcal{B}",
    "¬Q: The bilinear form B is symmetric if and only if the matrix M is a symmetric matrix fails"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    basis = witness.get('basis')
    B_input = witness.get('B')
    M = witness.get('M')
    u = witness.get('u')
    v = witness.get('v')
    
    # H1: \mathcal{B} is a basis for V
    try:
        n = len(basis)
        if n == 0:
            h1 = False
        else:
            mat = Matrix(basis[0])
            for b in basis[1:]:
                mat = mat.row_join(Matrix(b))
            # Check if the vectors are linearly independent
            h1 = (mat.rank() == n)
    except Exception:
        h1 = False
        
    # H2: B is a bilinear form on V
    try:
        if callable(B_input):
            def B(x, y):
                res = B_input(x, y)
                if hasattr(res, 'shape') and res.shape == (1, 1):
                    return res[0]
                elif isinstance(res, list) and len(res) == 1:
                    if isinstance(res[0], list):
                        return res[0][0]
                    return res[0]
                return res
        else:
            B = lambda x, y: (Matrix(x).T * Matrix(B_input) * Matrix(y))[0]
            
        b1 = Matrix(basis[0])
        b2 = Matrix(basis[1]) if n > 1 else Matrix(basis[0])
        
        c = symbols('c')
        
        h2 = True
        # Check additivity
        if expand(B(b1 + b2, b1) - (B(b1, b1) + B(b2, b1))) != 0: h2 = False
        if expand(B(b1, b1 + b2) - (B(b1, b1) + B(b1, b2))) != 0: h2 = False
        # Check scalar multiplication (using a symbolic scalar to rule out sesquilinear forms)
        if expand(B(c*b1, b2) - c*B(b1, b2)) != 0: h2 = False
        if expand(B(b1, c*b2) - c*B(b1, b2)) != 0: h2 = False
    except Exception:
        h2 = False
        
    # H3: M is the Gram matrix of B with respect to the basis \mathcal{B}
    try:
        M_mat = Matrix(M)
        h3 = True
        for i in range(n):
            for j in range(n):
                if expand(M_mat[i, j] - B(Matrix(basis[i]), Matrix(basis[j]))) != 0:
                    h3 = False
    except Exception:
        h3 = False
        
    # ¬Q: The bilinear form B is symmetric if and only if the matrix M is a symmetric matrix FAILS
    try:
        M_mat = Matrix(M)
        M_sym = True
        for i in range(n):
            for j in range(n):
                if expand(M_mat[i, j] - M_mat[j, i]) != 0:
                    M_sym = False
        
        if u is not None and v is not None:
            diff = B(u, v) - B(v, u)
            B_sym = (expand(diff) == 0)
        else:
            # Fallback to symbolic vectors if specific counterexample vectors are not provided
            u_syms = symbols(f'u1:{n+1}')
            v_syms = symbols(f'v1:{n+1}')
            u_vec = sum((sym * Matrix(b) for sym, b in zip(u_syms, basis)), Matrix(basis[0])*0)
            v_vec = sum((sym * Matrix(b) for sym, b in zip(v_syms, basis)), Matrix(basis[0])*0)
            diff = B(u_vec, v_vec) - B(v_vec, u_vec)
            B_sym = (expand(diff) == 0)
            
        conclusion = (B_sym == M_sym)
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]