import sympy
from sympy import Symbol, Poly, QQ, ZZ, Rational, Integer

x = Symbol('x')

def conditions(witness):
    try:
        domain, f_val, g_val = witness
        f_expr = sympy.sympify(f_val)
        g_expr = sympy.sympify(g_val)
    except Exception:
        return [False, False, False, False]
        
    # H1: F is a field
    try:
        h1 = bool(domain.is_Field)
    except Exception:
        h1 = False
        
    # H2: f(x) and g(x) are polynomials in F[x]
    try:
        if not (f_expr.free_symbols.issubset({x}) and g_expr.free_symbols.issubset({x})):
            h2 = False
        else:
            f_poly = Poly(f_expr, x, domain=domain)
            g_poly = Poly(g_expr, x, domain=domain)
            h2 = True
    except Exception:
        h2 = False
        
    # H3: Both f(x) and g(x) are non-constant polynomials
    try:
        f_poly = Poly(f_expr, x, domain=domain)
        g_poly = Poly(g_expr, x, domain=domain)
        h3 = bool(f_poly.degree() >= 1) and bool(g_poly.degree() >= 1)
    except Exception:
        h3 = False
        
    # neg_Q: f(x) is NOT irreducible in F[x]
    try:
        f_poly = Poly(f_expr, x, domain=domain)
        if f_poly.degree() < 1:
            neg_q = True
        else:
            factors = sympy.factor_list(f_poly)[1]
            num_factors = sum(mult for f, mult in factors if f.degree() >= 1)
            neg_q = bool(num_factors > 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f and g are polynomials over F",
    "H_3: Both f and g are non-constant polynomials",
    "¬Q: The polynomial f is not irreducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3