import sympy
from sympy import Poly

x, y, z = sympy.symbols('x y z')
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness) -> list[bool]:
    try:
        R, K, f, g, h = witness
    except Exception:
        return [False] * 5

    # H_1: R is a unique factorization domain
    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    # H_2: K is the field of fractions of R
    try:
        h2 = bool(K == R.get_field())
    except Exception:
        h2 = False

    # Determine the variable for polynomials
    try:
        f_sym = sympy.sympify(f)
        g_sym = sympy.sympify(g)
        h_sym = sympy.sympify(h)
        symbols = f_sym.free_symbols | g_sym.free_symbols | h_sym.free_symbols
        var = list(symbols)[0] if len(symbols) == 1 else x
    except Exception:
        var = x
        f_sym, g_sym, h_sym = f, g, h

    # H_3: f is a monic polynomial over R
    try:
        poly_f = Poly(f_sym, var)
        h3 = bool(poly_f.LC() == 1 and all(c in R for c in poly_f.coeffs()))
    except Exception:
        h3 = False

    # H_4: g and h are monic polynomials over K
    try:
        poly_g = Poly(g_sym, var)
        poly_h = Poly(h_sym, var)
        h4 = bool(poly_g.LC() == 1 and poly_h.LC() == 1 and 
                  all(c in K for c in poly_g.coeffs()) and 
                  all(c in K for c in poly_h.coeffs()))
    except Exception:
        h4 = False

    # ¬Q: g and h do not both lie in R polynomials
    try:
        poly_g = Poly(g_sym, var)
        poly_h = Poly(h_sym, var)
        g_in_R = all(c in R for c in poly_g.coeffs())
        h_in_R = all(c in R for c in poly_h.coeffs())
        neg_q = not (g_in_R and h_in_R)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: K is the field of fractions of R",
    "H_3: f is a monic polynomial over R",
    "H_4: g and h are monic polynomials over K",
    "¬Q: g and h do not both have all coefficients in R"
]

N_HYP = 4
NEG_Q_INDEX = 4