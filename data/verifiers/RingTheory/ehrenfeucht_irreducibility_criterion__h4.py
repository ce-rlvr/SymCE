import sympy
from sympy import degree
import math

x, y = sympy.symbols('x y')

def conditions(witness):
    try:
        f, g = witness
        f = sympy.sympify(f)
        g = sympy.sympify(g)
    except Exception:
        return [False] * 6
        
    try:
        h1 = True
    except Exception:
        h1 = False
        
    try:
        h2 = bool(f.free_symbols.issubset({x}) and f.is_polynomial(x))
        if f.is_number:
            h2 = True
    except Exception:
        h2 = False
        
    try:
        h3 = bool(g.free_symbols.issubset({y}) and g.is_polynomial(y))
        if g.is_number:
            h3 = True
    except Exception:
        h3 = False
        
    try:
        deg_g = degree(g, y)
        h4 = bool(deg_g >= 1)
    except Exception:
        h4 = False
        
    try:
        deg_f = degree(f, x)
        deg_g = degree(g, y)
        deg_f_val = -1 if deg_f == sympy.S.NegativeInfinity else int(deg_f)
        deg_g_val = -1 if deg_g == sympy.S.NegativeInfinity else int(deg_g)
        h5 = bool(math.gcd(deg_f_val, deg_g_val) == 1)
    except Exception:
        h5 = False
        
    try:
        poly_diff = f - g
        factors = sympy.factor_list(poly_diff)
        num_factors = sum(mult for factor, mult in factors[1])
        neg_q = bool(num_factors > 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f is a polynomial in x",
    "H_3: g is a polynomial in y",
    "H_4: degree of g is at least 1",
    "H_5: degrees of f and g are coprime",
    "not Q: f minus g is reducible"
]

N_HYP = 5
NEG_Q_INDEX = 5