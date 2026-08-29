import sympy as sp

# Top-level setup
x, t, u, v, y, z = sp.symbols('x t u v y z')

CONDITION_LABELS = [
    "H_1: E/F is an algebraic field extension",
    "¬Q: S is not a subfield, S/F is not separable, or E/S is not purely inseparable"
]
N_HYP = 1
NEG_Q_INDEX = 1

def parse_witness(witness):
    if not isinstance(witness, (tuple, list)):
        return witness, x, 0, [t]
    
    P = witness[0]
    S_poly = x
    p = 0
    base_vars = [t]
    
    if len(witness) == 2:
        if isinstance(witness[1], int):
            p = witness[1]
        else:
            S_poly = witness[1]
    elif len(witness) == 3:
        S_poly = witness[1]
        p = witness[2]
    elif len(witness) >= 4:
        S_poly = witness[1]
        p = witness[2]
        base_vars = witness[3]
        if not isinstance(base_vars, (list, tuple)):
            base_vars = [base_vars]
            
    return P, S_poly, p, base_vars

def poly_rem(A, P, x_var, p, base_vars):
    try:
        if p > 0:
            if base_vars:
                domain = sp.GF(p).frac_field(*base_vars)
            else:
                domain = sp.GF(p)
            return sp.rem(A, P, x_var, domain=domain)
        else:
            return sp.rem(A, P, x_var)
    except Exception:
        return sp.rem(A, P, x_var)

def matrix_rank(mat, p, base_vars):
    if not mat or not mat[0]: return 0
    rows = len(mat)
    cols = len(mat[0])
    
    max_rank = 0
    # Evaluate at a few points to compute rank over the fraction field
    for val in range(1, min(p + 10 if p > 0 else 10, 20)):
        try:
            subs_dict = {var: val + i for i, var in enumerate(base_vars)}
            num_mat = []
            for r in range(rows):
                row = []
                for c in range(cols):
                    expr = mat[r][c]
                    if hasattr(expr, 'subs'):
                        expr = expr.subs(subs_dict)
                    if p > 0:
                        num, den = sp.cancel(expr).as_numer_denom()
                        n_val = int(num) % p
                        d_val = int(den) % p
                        if d_val == 0:
                            raise ValueError
                        row.append((n_val * pow(d_val, p - 2, p)) % p)
                    else:
                        row.append(sp.Rational(expr))
                num_mat.append(row)
            
            if p > 0:
                rank = 0
                for c in range(cols):
                    pivot = -1
                    for r in range(rank, rows):
                        if num_mat[r][c] != 0:
                            pivot = r
                            break
                    if pivot == -1: continue
                    num_mat[rank], num_mat[pivot] = num_mat[pivot], num_mat[rank]
                    inv = pow(num_mat[rank][c], p - 2, p)
                    for r in range(rank + 1, rows):
                        if num_mat[r][c] != 0:
                            factor = (num_mat[r][c] * inv) % p
                            for k in range(c, cols):
                                num_mat[r][k] = (num_mat[r][k] - factor * num_mat[rank][k]) % p
                    rank += 1
            else:
                rank = sp.Matrix(num_mat).rank()
                
            if rank > max_rank:
                max_rank = rank
            if max_rank == min(rows, cols):
                break
        except Exception:
            continue
            
    return max_rank

def is_irreducible(P, x_var, p, base_vars):
    try:
        if p > 0:
            if base_vars:
                domain = sp.GF(p).frac_field(*base_vars)
            else:
                domain = sp.GF(p)
            poly = sp.Poly(P, x_var, domain=domain)
            return poly.is_irreducible
        else:
            return sp.Poly(P, x_var).is_irreducible
    except Exception:
        return True

def conditions(witness):
    try:
        P, S_poly, p, base_vars = parse_witness(witness)
    except Exception:
        return [False, False]
        
    try:
        P = sp.expand(P)
        S_poly = sp.expand(S_poly)
        poly_P = sp.Poly(P, x)
        n = poly_P.degree()
        if n < 1:
            h1_ok = False
        else:
            h1_ok = is_irreducible(P, x, p, base_vars)
    except Exception:
        h1_ok = False
        
    try:
        if not h1_ok:
            neg_q_ok = False
        else:
            beta = poly_rem(S_poly, P, x, p, base_vars)
            B = [sp.Integer(1)]
            curr = sp.Integer(1)
            for _ in range(1, n):
                curr = poly_rem(curr * beta, P, x, p, base_vars)
                B.append(curr)
                
            def poly_to_vec(poly_expr):
                poly = sp.Poly(poly_expr, x)
                return [poly.coeff_monomial(x**i) for i in range(n)]
                
            mat_B = [poly_to_vec(b) for b in B]
            d = matrix_rank(mat_B, p, base_vars)
            
            if p > 0:
                beta_p = poly_rem(beta**p, P, x, p, base_vars)
                B_p = [sp.Integer(1)]
                curr_p = sp.Integer(1)
                for _ in range(1, n):
                    curr_p = poly_rem(curr_p * beta_p, P, x, p, base_vars)
                    B_p.append(curr_p)
                mat_B_p = [poly_to_vec(b) for b in B_p]
                d_p = matrix_rank(mat_B_p, p, base_vars)
                S_sep = (d == d_p)
            else:
                S_sep = True
                
            E_S_pinsep = False
            if p > 0:
                curr_x_pk = x
                for k in range(n + 1):
                    v = poly_to_vec(curr_x_pk)
                    mat_check = mat_B[:d] + [v]
                    if matrix_rank(mat_check, p, base_vars) == d:
                        E_S_pinsep = True
                        break
                    curr_x_pk = poly_rem(curr_x_pk**p, P, x, p, base_vars)
            else:
                v = poly_to_vec(x)
                mat_check = mat_B[:d] + [v]
                E_S_pinsep = (matrix_rank(mat_check, p, base_vars) == d)
                
            neg_q_ok = not (S_sep and E_S_pinsep)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]