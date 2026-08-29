import sympy
from sympy import ZZ, QQ, Poly, expand
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: f is a monic polynomial over R",
    "H_3: g and h are monic polynomials over K",
    "H_4: f = gh",
    "¬Q: g and h are not both polynomials over R"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    try:
        R = witness['R']
        K = witness['K']
        f = witness['f']
        g = witness['g']
        h = witness['h']
        x_var = witness.get('x', x)
    except Exception:
        return [False] * 5

    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    try:
        f_poly = Poly(f, x_var)
        h2 = bool(f_poly.is_monic and all(c in R for c in f_poly.coeffs()))
    except Exception:
        h2 = False

    try:
        g_poly = Poly(g, x_var)
        h_poly = Poly(h, x_var)
        h3 = bool(g_poly.is_monic and all(c in K for c in g_poly.coeffs()) and
                  h_poly.is_monic and all(c in K for c in h_poly.coeffs()))
    except Exception:
        h3 = False

    try:
        h4 = bool(expand(f - g * h) == 0)
    except Exception:
        h4 = False

    try:
        g_poly = Poly(g, x_var)
        h_poly = Poly(h, x_var)
        g_in_R = all(c in R for c in g_poly.coeffs())
        h_in_R = all(c in R for c in h_poly.coeffs())
        neg_q = not (g_in_R and h_in_R)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]