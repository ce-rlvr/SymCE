import sympy
from sympy import Poly, expand, simplify, roots, degree, QQ, I, sqrt, Rational, Integer
from sympy.abc import x

def conditions(witness):
    try:
        F, f, g, K_gens = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    try:
        f_expr = f.as_expr() if hasattr(f, 'as_expr') else f
        poly_f = Poly(f_expr, x, domain=F)
        n = poly_f.degree()
        h2 = bool((n >= 1) and (poly_f.eval(0) != 0))
    except Exception:
        h2 = False
        
    try:
        g_expr = g.as_expr() if hasattr(g, 'as_expr') else g
        expected_g = expand(x**n * f_expr.subs(x, 1/x))
        h3 = bool(simplify(g_expr - expected_g) == 0)
    except Exception:
        h3 = False
        
    try:
        if F != QQ:
            h4 = False
        else:
            if not isinstance(K_gens, (list, tuple, set)):
                K_gens = [K_gens]
            
            g_expr = g.as_expr() if hasattr(g, 'as_expr') else g
            rts = roots(g_expr, x)
            if sum(rts.values()) < degree(g_expr, x):
                h4 = False
            else:
                g_roots = list(rts.keys())
                g_roots_alg = [r for r in g_roots if not getattr(r, 'is_Rational', False)]
                K_gens_alg = [k for k in K_gens if not getattr(k, 'is_Rational', False)]
                
                try:
                    F_g = QQ.algebraic_field(*g_roots_alg) if g_roots_alg else QQ
                except Exception:
                    F_g = None
                    
                try:
                    F_K = QQ.algebraic_field(*K_gens_alg) if K_gens_alg else QQ
                except Exception:
                    F_K = None
                
                if F_g is None:
                    h4 = False
                elif F_K is None:
                    h4 = True
                else:
                    is_split = True
                    for k in K_gens:
                        try:
                            F_g.from_expr(simplify(k))
                        except Exception:
                            is_split = False
                            break
                    if is_split:
                        for r in g_roots:
                            try:
                                F_K.from_expr(simplify(r))
                            except Exception:
                                is_split = False
                                break
                    h4 = not is_split
    except Exception:
        h4 = False
        
    return [h1, h2, h3, h4]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a polynomial over F of degree n >= 1 such that f(0) != 0",
    "H_3: g(x) = x^n f(1/x) is the reciprocal polynomial of f(x)",
    "¬Q: K is not the splitting field of g(x) over F"
]

N_HYP = 3
NEG_Q_INDEX = 3