import sympy as sp

z = sp.Symbol('z')

def count_automorphisms(P_expr, z):
    x = sp.Symbol('x')
    P_x = P_expr.subs(z, x)
    alpha = sp.CRootOf(P_expr, 0)
    factored = sp.factor(P_x, extension=alpha)
    if isinstance(factored, sp.Mul):
        factors = factored.args
    else:
        factors = [factored]
    
    linear_count = 0
    for f in factors:
        if isinstance(f, sp.Pow):
            base = f.base
        else:
            base = f
        if x in base.free_symbols and sp.Poly(base, x).degree() == 1:
            linear_count += 1
    return linear_count

def conditions(witness):
    try:
        P_expr = witness['min_poly']
        sigma_img = witness['sigma_img']
        x_expr = witness['x_poly']
    except Exception:
        return [False, False, False]
        
    # H_1: sigma is a generator of the Galois group Gal(L/K)
    try:
        h1_ok = False
        P_poly = sp.Poly(P_expr, z)
        if P_poly.is_irreducible:
            rem_poly = sp.rem(P_expr.subs(z, sigma_img), P_expr, z)
            if sp.Poly(rem_poly, z).is_zero:
                num_aut = count_automorphisms(P_expr, z)
                curr = z
                order = 0
                n = P_poly.degree()
                for i in range(1, n + 2):
                    curr = sp.rem(curr.subs(z, sigma_img), P_expr, z)
                    if sp.Poly(curr - z, z).is_zero:
                        order = i
                        break
                if order > 0 and order == num_aut:
                    h1_ok = True
    except Exception:
        h1_ok = False
        
    # H_2: x is an element of L
    try:
        sp.Poly(x_expr, z)
        h2_ok = True
    except Exception:
        h2_ok = False
        
    # ¬Q: Tr_{L/K}(x) == 0 is not equivalent to the existence of y in L such that x = y - sigma(y)
    try:
        n = sp.Poly(P_expr, z).degree()
        
        # Compute Tr_{L/K}(x)
        trace = 0
        x_z_j = sp.rem(x_expr, P_expr, z)
        for j in range(n):
            coeff = sp.Poly(x_z_j, z).nth(j)
            trace += coeff
            x_z_j = sp.rem(x_z_j * z, P_expr, z)
            
        trace_is_zero = (trace == 0)
        
        # Check existence of y such that x = y - sigma(y)
        T_cols = []
        sigma_y_basis = 1
        for j in range(n):
            y_basis = z**j
            T_basis = sp.rem(y_basis - sigma_y_basis, P_expr, z)
            col = [sp.Poly(T_basis, z).nth(i) for i in range(n)]
            T_cols.append(col)
            sigma_y_basis = sp.rem(sigma_y_basis * sigma_img, P_expr, z)
        T_matrix = sp.Matrix(T_cols).T
        
        x_poly_reduced = sp.rem(x_expr, P_expr, z)
        x_vec = sp.Matrix([sp.Poly(x_poly_reduced, z).nth(i) for i in range(n)])
        
        exists_y = (T_matrix.rank() == T_matrix.row_join(x_vec).rank())
        
        neg_q_ok = (trace_is_zero != exists_y)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: sigma is a generator of the Galois group Gal(L/K)",
    "H_2: x is an element of L",
    "¬Q: Tr_{L/K}(x) == 0 is not equivalent to the existence of y in L such that x = y - sigma(y)"
]

N_HYP = 2
NEG_Q_INDEX = 2