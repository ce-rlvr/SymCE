import sympy as sp

x = sp.Symbol('x')

def conditions(witness):
    try:
        f, g = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        if (hasattr(f, 'free_symbols') and f.free_symbols - {x}) or \
           (hasattr(g, 'free_symbols') and g.free_symbols - {x}):
            h1 = False
        else:
            f_poly = sp.Poly(f, x)
            g_poly = sp.Poly(g, x)
            h1 = True
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            h2 = bool(f_poly.is_irreducible)
    except Exception:
        h2 = False

    try:
        h3 = False
        if h1 and h2:
            degree = f_poly.degree()
            for i in range(degree):
                try:
                    alpha = sp.RootOf(f_poly.as_expr(), x, i)
                    if alpha.is_rational:
                        g_minus_alpha = sp.Poly(g - alpha, x, domain='QQ')
                    else:
                        g_minus_alpha = sp.Poly(g - alpha, x, extension=alpha)
                    
                    deg = g_minus_alpha.degree()
                    if deg == 1:
                        h3 = True
                        break
                    elif deg > 1:
                        if g_minus_alpha.is_irreducible:
                            h3 = True
                            break
                except Exception:
                    continue
    except Exception:
        h3 = False

    try:
        neg_q = False
        if h1:
            fg_expr = f_poly.as_expr().subs(x, g_poly.as_expr())
            fg_poly = sp.Poly(fg_expr, x)
            neg_q = not bool(fg_poly.is_irreducible)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f and g are polynomials over K",
    "H_2: f is irreducible over K",
    "H_3: There exists a root alpha of f such that g minus alpha is irreducible over K(alpha)",
    "¬Q: The composed polynomial f(g) is not irreducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3