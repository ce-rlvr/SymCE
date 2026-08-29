import sympy
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f, g are non-zero polynomials",
    "H_3: The contents of f and g are associates in R",
    "not Q: The polynomials f and g are NOT associates"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        f, g = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        f_poly = sympy.poly(f, x)
        g_poly = sympy.poly(g, x)
        domain = f_poly.domain.unify(g_poly.domain)
        f_poly = f_poly.set_domain(domain)
        g_poly = g_poly.set_domain(domain)
        h1 = bool(domain.is_UFD)
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        else:
            h2 = bool(not f_poly.is_zero and not g_poly.is_zero)
    except Exception:
        h2 = False

    try:
        if not h1 or not h2:
            h3 = False
        else:
            c_f = f_poly.content()
            c_g = g_poly.content()
            
            if c_f == domain.zero and c_g == domain.zero:
                h3 = True
            elif c_f == domain.zero or c_g == domain.zero:
                h3 = False
            else:
                try:
                    q1 = domain.exquo(c_f, c_g)
                    q2 = domain.exquo(c_g, c_f)
                    h3 = True
                except Exception:
                    h3 = False
    except Exception:
        h3 = False

    try:
        if not h1 or not h2:
            neg_q = False
        else:
            q1, r1 = f_poly.div(g_poly)
            q2, r2 = g_poly.div(f_poly)
            q_holds = bool(r1.is_zero and r2.is_zero)
            neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]