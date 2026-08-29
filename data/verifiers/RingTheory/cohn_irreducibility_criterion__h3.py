import sympy
from sympy import Symbol, isprime, factor_list
from sympy.polys.polytools import Poly
from sympy.ntheory import factorint

x = Symbol('x')

def conditions(witness):
    try:
        f, b = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        f_expr = sympy.sympify(f)
    except Exception:
        return [False, False, False, False]
        
    # H1: f(x) in Z[x]
    try:
        poly_f = Poly(f_expr, x)
        h1 = bool(poly_f.domain.is_ZZ and f_expr.free_symbols.issubset({x}))
    except Exception:
        h1 = False
        
    # H2: b >= 2 is an integer
    try:
        h2 = bool(int(b) == b and b >= 2)
    except Exception:
        h2 = False
        
    # H3: f(b) is prime
    try:
        val = f_expr.subs(x, b)
        h3 = bool(int(val) == val and isprime(int(val)))
    except Exception:
        h3 = False
        
    # neg_Q: f(x) is reducible in Z[x]
    try:
        coeff, factors = factor_list(f_expr, domain='ZZ')
        coeff_val = int(coeff)
        if coeff_val == 0:
            neg_q = True
        else:
            coeff_factors = sum(factorint(abs(coeff_val)).values()) if abs(coeff_val) > 1 else 0
            poly_factors = sum(m for f, m in factors)
            total_factors = coeff_factors + poly_factors
            neg_q = bool(total_factors > 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial over Z",
    "H_2: b >= 2 is an integer",
    "H_3: f(b) is a prime number",
    "not Q: f is reducible over Z"
]

N_HYP = 3
NEG_Q_INDEX = 3