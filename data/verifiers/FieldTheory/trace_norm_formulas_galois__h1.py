import sympy as sp

x = sp.Symbol('x')

CONDITION_LABELS = [
    "H_1: G = Gal(E/F) is the Galois group of the extension",
    "H_2: alpha is an element of E",
    "¬Q: The trace or norm of alpha does not match the sum or product over the Galois group"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        p_expr, alpha_expr, G_exprs = witness
    except Exception:
        return [False, False, False]

    # H1: G is the Galois group of the extension E/Q
    h1 = False
    try:
        if not isinstance(G_exprs, (list, tuple)):
            h1 = False
        else:
            p_expr = sp.sympify(p_expr)
            if not p_expr.free_symbols.issubset({x}):
                h1 = False
            else:
                poly_p = sp.Poly(p_expr, x, domain='QQ')
                # Restrict degree to ensure fast evaluation and non-trivial extensions
                if poly_p.degree() < 2 or poly_p.degree() > 10:
                    h1 = False
                elif not poly_p.is_irreducible:
                    h1 = False
                else:
                    real_roots = sp.real_roots(poly_p)
                    # We require at least one real root so that the number of roots in E 
                    # is bounded by the number of real roots, making our size check rigorous.
                    if len(real_roots) == 0:
                        h1 = False
                    elif len(G_exprs) != len(real_roots):
                        h1 = False
                    else:
                        h1 = True
                        seen = []
                        for r in G_exprs:
                            r_expr = sp.sympify(r)
                            if not r_expr.free_symbols.issubset({x}):
                                h1 = False
                                break
                            
                            # Check that r(x) is a valid automorphism: p(r(x)) == 0 mod p(x)
                            p_r = p_expr.subs(x, r_expr)
                            poly_p_r = sp.Poly(p_r, x, domain='QQ')
                            _, rem = poly_p_r.div(poly_p)
                            if not rem.is_zero:
                                h1 = False
                                break
                                
                            # Check that all provided automorphisms are distinct mod p(x)
                            poly_r = sp.Poly(r_expr, x, domain='QQ')
                            _, rem_r = poly_r.div(poly_p)
                            rem_r_expr = rem_r.as_expr()
                            if rem_r_expr in seen:
                                h1 = False
                                break
                            seen.append(rem_r_expr)
    except Exception:
        h1 = False

    # H2: alpha is an element of E
    h2 = False
    try:
        alpha_expr = sp.sympify(alpha_expr)
        if not alpha_expr.free_symbols.issubset({x}):
            h2 = False
        else:
            poly_alpha = sp.Poly(alpha_expr, x, domain='QQ')
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The trace or norm of alpha does not match the sum or product over the Galois group
    neg_q = False
    try:
        if h1 and h2:
            n = poly_p.degree()
            M = sp.zeros(n, n)
            x_poly = sp.Poly(x, x, domain='QQ')
            
            # Construct the matrix of the linear map (multiplication by alpha) in basis 1, x, ..., x^{n-1}
            for i in range(n):
                term = poly_alpha * (x_poly ** i)
                _, rem = term.div(poly_p)
                coeffs = rem.all_coeffs()
                # Pad with leading zeros to match degree n-1
                coeffs = [0] * (n - len(coeffs)) + coeffs
                for j in range(n):
                    M[j, i] = coeffs[n - 1 - j]
            
            Tr_alpha = M.trace()
            N_alpha = M.det()
            
            # Compute sum and product of alpha over the Galois group
            Sum_alpha = sp.S(0)
            Prod_alpha = sp.S(1)
            
            for r in G_exprs:
                r_expr = sp.sympify(r)
                alpha_r = alpha_expr.subs(x, r_expr)
                Sum_alpha += alpha_r
                Prod_alpha *= alpha_r
                
            poly_Sum = sp.Poly(Sum_alpha, x, domain='QQ')
            _, rem_Sum = poly_Sum.div(poly_p)
            
            poly_Prod = sp.Poly(Prod_alpha, x, domain='QQ')
            _, rem_Prod = poly_Prod.div(poly_p)
            
            Tr_poly = sp.Poly(Tr_alpha, x, domain='QQ')
            N_poly = sp.Poly(N_alpha, x, domain='QQ')
            
            Tr_eq = (rem_Sum - Tr_poly).is_zero
            N_eq = (rem_Prod - N_poly).is_zero
            
            # The conclusion fails if either the trace or the norm does not match
            neg_q = not (Tr_eq and N_eq)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]