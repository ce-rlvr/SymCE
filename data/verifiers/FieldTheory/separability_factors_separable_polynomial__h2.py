import sympy
from sympy import Symbol, diff, rem, gcd, degree, Poly

x = Symbol('x')
QQ = sympy.QQ
ZZ = sympy.ZZ
GF = sympy.GF

def conditions(witness):
    try:
        K, f, g = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(K.is_Field)
    except Exception:
        h1 = False
        
    try:
        f_expr = f.as_expr() if hasattr(f, 'as_expr') else f
        g_expr = g.as_expr() if hasattr(g, 'as_expr') else g
        
        poly_g = Poly(g_expr, x, domain=K)
        deg_g = poly_g.degree()
        is_non_constant = deg_g >= 1
        
        remainder = rem(f_expr, g_expr, x, domain=K)
        divides = (remainder == 0) or (sympy.simplify(remainder) == 0)
        
        h2 = bool(is_non_constant and divides)
    except Exception:
        h2 = False
        
    try:
        g_expr = g.as_expr() if hasattr(g, 'as_expr') else g
        g_prime = diff(g_expr, x)
        g_gcd = gcd(g_expr, g_prime, x, domain=K)
        deg_gcd = degree(g_gcd, x)
        
        neg_q = bool(deg_gcd > 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: g is a non-constant polynomial that divides f",
    "not Q: g is not a separable polynomial"
]

N_HYP = 2
NEG_Q_INDEX = 2