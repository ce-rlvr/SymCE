import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: n >= 1",
    "¬Q: uv^* does not have an eigenvalue equal to v^*u, or 0 does not have algebraic multiplicity at least n-1"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    if not isinstance(witness, (tuple, list)):
        return [False, False]
        
    try:
        if len(witness) == 3:
            n, u, v = witness
        elif len(witness) == 2:
            u, v = witness
            u_mat = sympy.Matrix(u)
            n = max(u_mat.shape)
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        if float(n) != int(n):
            h1 = False
        else:
            n = int(n)
            h1 = (n >= 1)
    except Exception:
        h1 = False
        
    try:
        u_mat = sympy.Matrix(u)
        v_mat = sympy.Matrix(v)
        
        uv_star = u_mat * v_mat.H
        v_star_u = v_mat.H * u_mat
        
        if v_star_u.shape == (1, 1):
            val = v_star_u[0, 0]
            Id = sympy.eye(uv_star.shape[0])
            char_matrix = uv_star - val * Id
            c1 = (sympy.simplify(char_matrix.det()) == 0)
        else:
            c1 = False
            
        lam = sympy.Symbol('lambda')
        cp = uv_star.charpoly(lam)
        coeffs = cp.all_coeffs()
        
        trailing_zeros = 0
        for c in reversed(coeffs):
            if sympy.simplify(c) == 0:
                trailing_zeros += 1
            else:
                break
                
        c2 = (trailing_zeros >= n - 1)
        
        q = c1 and c2
        neg_q = not q
    except Exception:
        neg_q = True
        
    return [h1, neg_q]