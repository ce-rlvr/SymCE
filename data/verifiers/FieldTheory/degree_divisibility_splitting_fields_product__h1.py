import sympy
from sympy import Poly, lcm, roots, expand
from sympy.polys.numberfields import primitive_element
from sympy.abc import x, y

def conditions(witness):
    try:
        f = witness[0]
        g = witness[1]
        h = witness[2]
    except Exception:
        return [False, False, False]
        
    try:
        f_poly = Poly(f, x)
        f_diff = f_poly.diff(x)
        gcd_poly = f_poly.gcd(f_diff)
        h1 = bool(gcd_poly.degree() == 0)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(Poly(f, x) == Poly(g, x) * Poly(h, x))
    except Exception:
        try:
            h2 = bool(expand(f - g*h) == 0)
        except Exception:
            h2 = False
            
    try:
        if len(witness) >= 6:
            df = int(witness[3])
            dg = int(witness[4])
            dh = int(witness[5])
        else:
            def get_sf_deg(p):
                p_poly = Poly(p, x)
                if p_poly.degree() <= 0:
                    return 1
                if p_poly.domain.is_FiniteField:
                    factors = p_poly.factor_list()[1]
                    deg = 1
                    for factor, mult in factors:
                        deg = lcm(deg, factor.degree())
                    return deg
                else:
                    r_dict = roots(p_poly)
                    if sum(r_dict.values()) < p_poly.degree():
                        raise ValueError()
                    r = list(r_dict.keys())
                    if not r:
                        return 1
                    _, minpoly = primitive_element(r, y, ex=True)
                    return Poly(minpoly, y).degree()
                    
            df = get_sf_deg(f)
            dg = get_sf_deg(g)
            dh = get_sf_deg(h)
            
        neg_q = bool(df % (dg * dh) != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a separable polynomial",
    "H_2: f = g * h",
    "¬Q: The degree of K_f over F does not divide the product of degrees of K_g and K_h"
]

N_HYP = 2
NEG_Q_INDEX = 2