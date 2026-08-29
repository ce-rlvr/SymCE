import sympy
from sympy import degree, expand
from sympy.abc import x

# Standard algebra objects relevant to Ring Theory
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        f, g = witness
    except Exception:
        return [False, False, False]
    
    # H_1: R is a ring
    try:
        # Check if the witness elements support ring operations (addition and multiplication)
        _ = f + g
        _ = f * g
        h1 = True
    except Exception:
        h1 = False

    # H_2: f(x) + g(x) is not the zero polynomial
    try:
        sum_fg = f + g
        if hasattr(sum_fg, 'is_zero') and sum_fg.is_zero is not None:
            h2 = not sum_fg.is_zero
        else:
            h2 = bool(expand(sum_fg) != 0)
    except Exception:
        h2 = False

    # ¬Q: The degree of f(x) + g(x) is strictly greater than the maximum of the degree of f(x) and the degree of g(x)
    try:
        def get_deg(p):
            if hasattr(p, 'degree') and callable(p.degree):
                try:
                    return p.degree()
                except Exception:
                    pass
            return degree(p, x)
        
        deg_f = get_deg(f)
        deg_g = get_deg(g)
        deg_fg = get_deg(sum_fg)
        
        neg_q = bool(deg_fg > max(deg_f, deg_g))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: f(x) + g(x) is not the zero polynomial",
    "¬Q: The degree of f(x) + g(x) is strictly greater than the maximum of the degree of f(x) and the degree of g(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2