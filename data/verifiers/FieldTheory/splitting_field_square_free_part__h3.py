import sympy
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        f, g = witness
    except Exception:
        return [False, False, False, False]

    # H1: F is a field (implicitly QQ)
    h1 = True

    # H2: f(x) is a non-constant polynomial
    try:
        poly_f = sympy.Poly(f, x, domain='QQ')
        h2 = poly_f.degree() >= 1
    except Exception:
        h2 = False

    # H3: E is the splitting field of f(x) over F (implicitly defined)
    h3 = True

    # neg_Q: E is NOT the splitting field of g(x) over F
    try:
        poly_g = sympy.Poly(g, x, domain='QQ')
        
        r_f = sympy.roots(poly_f)
        r_g = sympy.roots(poly_g)
        
        if sum(r_f.values()) != poly_f.degree() or sum(r_g.values()) != poly_g.degree():
            neg_q = False
        else:
            ext_f = list({r for r in r_f.keys() if not r.is_rational})
            ext_g = list({r for r in r_g.keys() if not r.is_rational})
            
            if not ext_f and not ext_g:
                neg_q = False
            elif not ext_f or not ext_g:
                neg_q = True
            else:
                from sympy.polys.numberfields import primitive_element
                minp_f, _ = primitive_element(ext_f, x, ex=True)
                minp_g, _ = primitive_element(ext_g, x, ex=True)
                
                deg_f = sympy.degree(minp_f, x)
                deg_g = sympy.degree(minp_g, x)
                
                if deg_f != deg_g:
                    neg_q = True
                elif deg_f <= 2 and deg_g <= 2:
                    if deg_f == 1:
                        neg_q = False
                    else:
                        coeffs_f = sympy.Poly(minp_f, x).all_coeffs()
                        d_f = coeffs_f[1]**2 - 4 * coeffs_f[0] * coeffs_f[2]
                        
                        coeffs_g = sympy.Poly(minp_g, x).all_coeffs()
                        d_g = coeffs_g[1]**2 - 4 * coeffs_g[0] * coeffs_g[2]
                        
                        neg_q = not sympy.sqrt(d_f / d_g).is_rational
                else:
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a non-constant polynomial over F",
    "H_3: E is the splitting field of f(x) over F",
    "¬Q: E is NOT the splitting field of g(x) over F"
]

N_HYP = 3
NEG_Q_INDEX = 3