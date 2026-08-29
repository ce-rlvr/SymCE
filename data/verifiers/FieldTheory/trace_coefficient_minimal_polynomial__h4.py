import sympy
from sympy import Poly, simplify, minpoly
from sympy.abc import x

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    try:
        alpha, p_expr = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = True
    except Exception:
        h1 = False
        
    try:
        mp = minpoly(alpha, x)
        h2 = True
    except Exception:
        h2 = False
        
    try:
        poly_p = Poly(p_expr, x, domain='QQ')
        poly_mp = Poly(mp, x, domain='QQ')
        _, rem = poly_p.div(poly_mp)
        h3 = bool(rem.is_zero and poly_p.degree() == poly_mp.degree() and poly_p.degree() >= 1)
    except Exception:
        h3 = False
        
    try:
        n = poly_p.degree()
        coeffs = poly_p.all_coeffs()
        if n >= 1:
            c_n_minus_1 = coeffs[1]
            c_n = coeffs[0]
        else:
            c_n_minus_1 = 0
            c_n = 1
            
        trace = - (c_n_minus_1 / c_n)
        diff = simplify(c_n_minus_1 - (-trace))
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: E over F is a field extension",
    "H_2: alpha in E is an algebraic element over F such that E = F(alpha)",
    "H_3: p(x) is the minimal polynomial of alpha over F",
    "neg_Q: The coefficient of x^{n-1} in p(x) is NOT equal to -Tr_{E/F}(alpha)"
]

N_HYP = 3
NEG_Q_INDEX = 3