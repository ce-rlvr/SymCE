import sympy
from sympy import Symbol, minpoly, degree, Poly, I, pi, E, Rational, sqrt
from sympy.abc import x

def conditions(witness):
    alpha = None
    p = None
    
    try:
        if isinstance(witness, dict):
            alpha = witness.get('alpha')
            p = witness.get('p')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 4:
                alpha, p = witness[2], witness[3]
            elif len(witness) == 3:
                alpha, p = witness[1], witness[2]
            elif len(witness) >= 2:
                alpha, p = witness[0], witness[1]
    except Exception:
        pass

    try:
        h1 = alpha is not None
    except Exception:
        h1 = False

    try:
        mp = minpoly(alpha, x)
        h2 = True
    except Exception:
        h2 = False

    try:
        deg_K_alpha = degree(mp, x)
        
        if isinstance(p, Poly):
            deg_p = p.degree()
        else:
            p_expr = sympy.sympify(p)
            free_syms = p_expr.free_symbols
            if len(free_syms) == 1:
                sym = list(free_syms)[0]
                deg_p = degree(p_expr, sym)
            else:
                deg_p = degree(p_expr, x)
                
        neg_q = bool(deg_K_alpha != deg_p)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a field extension",
    "H_2: alpha is an element of L that is algebraic over K",
    "¬Q: The degree of K(alpha) over K is not equal to the degree of p(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2