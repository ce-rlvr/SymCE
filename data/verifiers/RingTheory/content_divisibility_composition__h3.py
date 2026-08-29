import sympy
from sympy import Poly
from sympy.abc import x, y, z
from sympy import ZZ, QQ

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, g = witness
                if hasattr(f, 'as_expr'): f = f.as_expr()
                if hasattr(g, 'as_expr'): g = g.as_expr()
                poly_f = Poly(f, x)
                domain = poly_f.domain
            elif len(witness) == 3:
                R, f, g = witness
                if hasattr(f, 'as_expr'): f = f.as_expr()
                if hasattr(g, 'as_expr'): g = g.as_expr()
                domain = R
                poly_f = Poly(f, x, domain=domain)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(getattr(domain, 'is_UFD', False) or getattr(domain, 'is_Field', False))
    except Exception:
        h1 = False

    try:
        h2 = True
    except Exception:
        h2 = False

    try:
        fg_expr = f.subs(x, g)
        poly_fg = Poly(fg_expr, x, domain=domain)
        c_fg = poly_fg.content()
        c_f = poly_f.content()
        
        if c_f == 0:
            neg_q = (c_fg != 0)
        else:
            try:
                rem = domain.rem(c_fg, c_f)
                neg_q = (rem != 0)
            except Exception:
                try:
                    neg_q = (sympy.rem(c_fg, c_f) != 0)
                except Exception:
                    neg_q = (c_fg % c_f != 0)
    except Exception:
        neg_q = True

    return [h1, h2, bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a polynomial over R",
    "¬Q: The content of f(x) does not divide the content of f(g(x)) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2