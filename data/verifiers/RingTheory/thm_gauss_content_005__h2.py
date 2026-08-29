import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import x, y, z

def elements_are_associates(c1, c2, R):
    if c1 == R.zero and c2 == R.zero:
        return True
    if c1 == R.zero or c2 == R.zero:
        return False
    try:
        q1 = R.exquo(c1, c2)
        q2 = R.exquo(c2, c1)
        return bool(R.is_unit(q1)) and bool(R.is_unit(q2))
    except Exception:
        return False

def polys_are_associates(f, g, R):
    if f.is_zero and g.is_zero:
        return True
    if f.is_zero or g.is_zero:
        return False
    try:
        q1, r1 = f.div(g)
        q2, r2 = g.div(f)
        if r1.is_zero and r2.is_zero:
            if q1.degree() <= 0 and q2.degree() <= 0:
                u1 = q1.LC()
                u2 = q2.LC()
                return bool(R.is_unit(u1)) and bool(R.is_unit(u2))
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) == 3:
            R_wit, f_expr, g_expr = witness
            if isinstance(f_expr, Poly):
                f = f_expr
            else:
                f = Poly(f_expr, x, domain=R_wit)
            if isinstance(g_expr, Poly):
                g = g_expr
            else:
                g = Poly(g_expr, x, domain=R_wit)
            R = R_wit
        elif len(witness) == 2:
            f_expr, g_expr = witness
            if isinstance(f_expr, Poly):
                f = f_expr
            else:
                f = Poly(f_expr, x)
            if isinstance(g_expr, Poly):
                g = g_expr
            else:
                g = Poly(g_expr, x)
            R = f.domain
        else:
            return [False, False, False, False]
            
        if f.domain != R:
            f = f.set_domain(R)
        if g.domain != R:
            g = g.set_domain(R)
    except Exception:
        return [False, False, False, False]
        
    # H1: R is a Unique Factorization Domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False
        
    # H2: The contents of f and g are associates in R
    try:
        cf, pf = f.primitive()
        cg, pg = g.primitive()
        h2 = elements_are_associates(cf, cg, R)
    except Exception:
        h2 = False
        
    # H3: The primitive parts of f and g are associates in R[X]
    try:
        h3 = polys_are_associates(pf, pg, R)
    except Exception:
        h3 = False
        
    # neg_Q: The polynomials f and g are NOT associates in R[X]
    try:
        neg_q = not polys_are_associates(f, g, R)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: The contents of f and g are associates in R",
    "H_3: The primitive parts of f and g are associates in the polynomial ring",
    "not_Q: The polynomials f and g are not associates in the polynomial ring"
]

N_HYP = 3
NEG_Q_INDEX = 3