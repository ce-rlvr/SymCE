import sympy
from sympy import Poly, gcd_list, lcm_list, fraction, cancel
from sympy.abc import x, y, z

def get_content(p):
    poly = Poly(p, x)
    coeffs = poly.coeffs()
    nums = []
    dens = []
    for c in coeffs:
        n, d = fraction(cancel(c))
        nums.append(n)
        dens.append(d)
    num_gcd = gcd_list(nums)
    den_lcm = lcm_list(dens)
    return cancel(num_gcd / den_lcm)

def is_in_R(expr):
    try:
        if isinstance(expr, int) or (hasattr(expr, 'is_Integer') and expr.is_Integer):
            return True
        poly = Poly(expr)
        return all(c.is_integer for c in poly.coeffs())
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        f, g = witness
    except Exception:
        return [False, False, False]
        
    h1_ok = True
    
    try:
        poly_g = Poly(g, x)
        h2_ok = all(is_in_R(c) for c in poly_g.coeffs())
    except Exception:
        h2_ok = False
        
    try:
        c_f = get_content(f)
        fg = f.subs(x, g).expand()
        c_fg = get_content(fg)
        
        if c_f == 0:
            neg_q_ok = (c_fg != 0)
        else:
            ratio = cancel(c_fg / c_f)
            neg_q_ok = not is_in_R(ratio)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: R is a Unique Factorization Domain", "H_2: g is a polynomial over R", "not Q: The content of f does not divide the content of f composed with g"]
N_HYP = 2
NEG_Q_INDEX = 2