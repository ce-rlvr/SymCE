import sympy

x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        f, g = witness
    except Exception:
        return [False, False, False]
    
    try:
        f_poly = sympy.poly(f, x)
        g_poly = sympy.poly(g, x)
        h1 = bool(f_poly.domain == sympy.ZZ and g_poly.domain == sympy.ZZ)
    except Exception:
        h1 = False
        
    try:
        if h1:
            f_coeffs = f_poly.coeffs()
            g_coeffs = g_poly.coeffs()
            h2 = bool(sympy.gcd_list(f_coeffs) == 1 and sympy.gcd_list(g_coeffs) == 1)
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        if h1:
            are_associates = (f_poly == g_poly) or (f_poly == -g_poly)
            neg_q = not are_associates
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f and g are primitive polynomials",
    "not Q: f and g are not associate elements"
]

N_HYP = 2
NEG_Q_INDEX = 2