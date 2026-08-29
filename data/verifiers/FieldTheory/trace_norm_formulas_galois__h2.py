import sympy
from sympy import Poly, zeros, sympify
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: E/F is a finite Galois extension",
    "H_2: alpha is an element of E",
    "¬Q: Trace is not sum over G, or Norm is not product over G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # The witness is expected to be a dictionary containing:
        # - 'E_poly': minimal polynomial of E over Q (defining the extension E/Q)
        # - 'Gal_maps': list of polynomials representing the full Galois group Gal(E/Q)
        # - 'G_maps': list of polynomials representing the subgroup G
        # - 'alpha_poly': polynomial representing the element alpha in E
        E_poly = witness.get('E_poly')
        Gal_maps = witness.get('Gal_maps')
        G_maps = witness.get('G_maps')
        alpha_poly = witness.get('alpha_poly')
        
        if E_poly is None or Gal_maps is None or G_maps is None or alpha_poly is None:
            return [False, False, False]
            
        try:
            p_E = Poly(E_poly, x, domain='QQ')
        except Exception:
            return [False, False, False]
            
        n = p_E.degree()
        if n < 1:
            return [False, False, False]
            
        # H1: E/F is a finite Galois extension
        # We verify this by checking if E_poly is irreducible and if Gal_maps provides n distinct roots.
        h1_ok = False
        if p_E.is_irreducible:
            if len(Gal_maps) == n:
                roots_ok = True
                for g in Gal_maps:
                    try:
                        rem = Poly(E_poly.subs(x, g), x, domain='QQ') % p_E
                        if not rem.is_zero:
                            roots_ok = False
                            break
                    except Exception:
                        roots_ok = False
                        break
                if roots_ok:
                    gal_exprs = set()
                    try:
                        for g in Gal_maps:
                            rem = Poly(g, x, domain='QQ') % p_E
                            gal_exprs.add(rem.as_expr())
                        if len(gal_exprs) == n:
                            h1_ok = True
                    except Exception:
                        pass
                        
        # Check if G_maps is a valid subgroup of Gal_maps
        if h1_ok:
            g_exprs = set()
            for g in G_maps:
                try:
                    rem = Poly(g, x, domain='QQ') % p_E
                    g_exprs.add(rem.as_expr())
                except Exception:
                    h1_ok = False
                    break
            
            if h1_ok:
                if len(g_exprs) != len(G_maps):
                    h1_ok = False
                elif not g_exprs.issubset(gal_exprs):
                    h1_ok = False
                else:
                    try:
                        id_expr = (Poly(x, x, domain='QQ') % p_E).as_expr()
                        if id_expr not in g_exprs:
                            h1_ok = False
                        else:
                            for g1 in g_exprs:
                                for g2 in g_exprs:
                                    comp = Poly(g1.subs(x, g2), x, domain='QQ') % p_E
                                    if comp.as_expr() not in g_exprs:
                                        h1_ok = False
                                        break
                                if not h1_ok:
                                    break
                    except Exception:
                        h1_ok = False

        # H2: alpha is an element of E
        h2_ok = False
        alpha_expr = None
        try:
            alpha_expr = sympify(alpha_poly)
            if hasattr(alpha_expr, 'as_expr'):
                alpha_expr = alpha_expr.as_expr()
            if alpha_expr.free_symbols.issubset({x}):
                Poly(alpha_expr, x, domain='QQ')
                h2_ok = True
        except Exception:
            pass

        # Evaluate conclusion
        neg_q = False
        if h1_ok and h2_ok:
            try:
                # Compute the multiplication matrix of alpha to find Trace and Norm
                M = zeros(n, n)
                for j in range(n):
                    basis_el = x**j
                    prod = Poly(alpha_expr * basis_el, x, domain='QQ')
                    rem = prod % p_E
                    coeffs = rem.all_coeffs()
                    coeffs = [0]*(n - len(coeffs)) + coeffs
                    coeffs = coeffs[::-1]
                    for i in range(n):
                        M[i, j] = coeffs[i]
                        
                trace_val = M.trace()
                norm_val = M.det()
                
                # Compute sum and product of alpha over the subgroup G
                sum_poly = Poly(0, x, domain='QQ')
                prod_poly = Poly(1, x, domain='QQ')
                for g in G_maps:
                    subbed = Poly(alpha_expr.subs(x, g), x, domain='QQ') % p_E
                    sum_poly = (sum_poly + subbed) % p_E
                    prod_poly = (prod_poly * subbed) % p_E
                    
                sum_expr = sum_poly.as_expr().expand()
                prod_expr = prod_poly.as_expr().expand()
                
                trace_expr = sympify(trace_val).expand()
                norm_expr = sympify(norm_val).expand()
                
                # The conclusion fails if either the trace or norm formula does not hold
                if (trace_expr - sum_expr).expand() != 0 or (norm_expr - prod_expr).expand() != 0:
                    neg_q = True
            except Exception:
                pass

        return [h1_ok, h2_ok, neg_q]
    except Exception:
        return [False, False, False]