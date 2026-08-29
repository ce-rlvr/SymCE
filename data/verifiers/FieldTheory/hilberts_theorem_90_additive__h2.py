import sympy

x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    witness is a tuple: (min_poly, tau_img, sigma_img, alpha_poly)
    min_poly: irreducible polynomial over QQ defining L = QQ[x]/(min_poly)
    tau_img: generator of the Galois group Gal(L/QQ)
    sigma_img: the automorphism sigma in the conclusion
    alpha_poly: the element alpha in L
    """
    def eval_poly_mod(poly_expr, val_expr, mod_poly):
        poly = sympy.Poly(poly_expr, x, domain='QQ')
        coeffs = poly.all_coeffs()
        res = 0
        for c in coeffs:
            res = sympy.rem(res * val_expr + c, mod_poly, x, domain='QQ')
        return res

    try:
        min_poly, tau_img, sigma_img, alpha_poly = witness
        
        min_poly = sympy.sympify(min_poly)
        tau_img = sympy.sympify(tau_img)
        sigma_img = sympy.sympify(sigma_img)
        alpha_poly = sympy.sympify(alpha_poly)
        
        # H1: L/K is a finite cyclic Galois extension
        min_poly_poly = sympy.Poly(min_poly, x, domain='QQ')
        d = min_poly_poly.degree()
        if d < 2:
            h1_ok = False
        elif not min_poly_poly.is_irreducible:
            h1_ok = False
        else:
            curr = x
            tau_powers = []
            for _ in range(d):
                tau_powers.append(curr)
                curr = eval_poly_mod(tau_img, curr, min_poly)
            
            if sympy.simplify(curr - x) != 0:
                h1_ok = False
            elif len(set(tau_powers)) != d:
                h1_ok = False
            else:
                sigma_rem = sympy.rem(sigma_img, min_poly, x, domain='QQ')
                if sigma_rem not in tau_powers:
                    h1_ok = False
                else:
                    h1_ok = True
    except Exception:
        h1_ok = False

    try:
        # H2: alpha is an element of L
        sympy.Poly(alpha_poly, x, domain='QQ')
        h2_ok = True
    except Exception:
        h2_ok = False

    try:
        if not (h1_ok and h2_ok):
            neg_q_ok = False
        else:
            # Compute Tr_{L/K}(alpha)
            trace_alpha = 0
            for p in tau_powers:
                trace_alpha += eval_poly_mod(alpha_poly, p, min_poly)
            trace_alpha = sympy.rem(trace_alpha, min_poly, x, domain='QQ')
            
            P = sympy.Poly(trace_alpha, x, domain='QQ').is_zero
            
            # Check if there exists beta in L such that alpha = beta - sigma(beta)
            def get_coords(poly_expr):
                poly = sympy.Poly(sympy.rem(poly_expr, min_poly, x, domain='QQ'), x, domain='QQ')
                coeffs = poly.all_coeffs()
                coeffs = coeffs[::-1]
                coeffs += [0] * (d - len(coeffs))
                return coeffs

            M_cols = []
            curr_sigma = 1
            for i in range(d):
                basis_elem = x**i
                T_basis = basis_elem - curr_sigma
                M_cols.append(get_coords(T_basis))
                curr_sigma = sympy.rem(curr_sigma * sigma_rem, min_poly, x, domain='QQ')
            
            M = sympy.Matrix(M_cols).T
            
            alpha_coords = get_coords(alpha_poly)
            v = sympy.Matrix(alpha_coords)
            
            rank_M = M.rank()
            rank_aug = M.row_join(v).rank()
            
            Q = (rank_M == rank_aug)
            
            # The conclusion is P <-> Q. It fails if P != Q.
            neg_q_ok = (P != Q)
            
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: L/K is a finite cyclic Galois extension",
    "H_2: alpha is an element of L",
    "¬Q: Tr_{L/K}(alpha) = 0 is not equivalent to exists beta in L such that alpha = beta - sigma(beta)"
]

N_HYP = 2
NEG_Q_INDEX = 2