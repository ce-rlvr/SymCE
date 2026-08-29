import sympy
from sympy import degree, Poly, oo
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        f, g = witness
        f = sympy.sympify(f)
        g = sympy.sympify(g)
    except Exception:
        return [False, False, False]

    # H_1: R is a ring
    try:
        h1 = True
    except Exception:
        h1 = False

    # H_2: f(x) and g(x) are polynomials in R[x]
    try:
        sympy.Poly(f, x)
        sympy.Poly(g, x)
        h2 = True
    except Exception:
        h2 = False

    # neg_Q: The degree of f(x) + g(x) is greater than the maximum of the degree of f(x) and the degree of g(x)
    try:
        deg_f = degree(f, gen=x)
        deg_g = degree(g, gen=x)
        deg_fg = degree(f + g, gen=x)
        
        if deg_fg == -oo:
            neg_q = False
        else:
            max_deg = sympy.Max(deg_f, deg_g)
            neg_q = bool(deg_fg > max_deg)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: R is a ring", "H_2: f and g are polynomials", "neg_Q: degree of sum is greater than max degree"]

N_HYP = 2
NEG_Q_INDEX = 2