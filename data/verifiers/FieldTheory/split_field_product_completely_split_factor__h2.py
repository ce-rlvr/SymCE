import sympy
from sympy import QQ, Poly, sqrt, I, Rational
from sympy.abc import x

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is the splitting field of f(x) over F",
    "H_3: g(x) splits completely into linear factors over K",
    "not Q: K is not the splitting field of f(x)g(x) over F"
]

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, g = witness
            elif len(witness) >= 3:
                f, g = witness[-2], witness[-1]
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    h1 = True

    try:
        poly_f = Poly(f, x)
        h2 = all(c in QQ for c in poly_f.coeffs())
    except Exception:
        h2 = False

    h3 = False
    try:
        if h2:
            roots_f_dict = sympy.roots(f, x)
            if sum(roots_f_dict.values()) == poly_f.degree():
                roots_f = list(roots_f_dict.keys())
                if not roots_f:
                    K_field = QQ
                else:
                    K_field = QQ.algebraic_field(*roots_f)
                
                poly_g = Poly(g, x)
                roots_g_dict = sympy.roots(g, x)
                
                if sum(roots_g_dict.values()) == poly_g.degree():
                    h3_ok = True
                    for rg in roots_g_dict.keys():
                        try:
                            K_field.from_expr(rg)
                        except Exception:
                            h3_ok = False
                            break
                    
                    if h3_ok:
                        for c in poly_g.coeffs():
                            try:
                                K_field.from_expr(c)
                            except Exception:
                                h3_ok = False
                                break
                    h3 = h3_ok
    except Exception:
        h3 = False

    neg_q = False
    try:
        poly_fg = Poly(f * g, x)
        is_in_QQ = all(c in QQ for c in poly_fg.coeffs())
        neg_q = not is_in_QQ
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]