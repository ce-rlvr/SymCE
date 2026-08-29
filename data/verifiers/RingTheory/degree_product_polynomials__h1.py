import sympy
from sympy import Poly
from sympy.abc import x, y, z

def conditions(witness):
    try:
        f, g = witness
    except Exception:
        return [False, False]
        
    try:
        def check_zero(p):
            if hasattr(p, 'is_zero') and p.is_zero is not None:
                return bool(p.is_zero)
            return bool(p == 0)

        h1 = not check_zero(f) and not check_zero(g)
    except Exception:
        h1 = False

    try:
        def get_degree(p):
            if hasattr(p, 'degree'):
                if callable(p.degree):
                    return p.degree()
                else:
                    return p.degree
            return sympy.degree(p)

        deg_f = get_degree(f)
        deg_g = get_degree(g)
        fg = f * g
        deg_fg = get_degree(fg)
        
        neg_q = bool(deg_fg != deg_f + deg_g)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f and g are non-zero polynomials",
    "¬Q: deg(f*g) != deg(f) + deg(g)"
]

N_HYP = 1
NEG_Q_INDEX = 1