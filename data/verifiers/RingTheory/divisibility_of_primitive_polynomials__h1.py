import math
import functools
from sympy import Poly, expand, rem, simplify, Integer

# Top-level setup
# The witness is expected to be a tuple: (f, g, x, y, minpoly)
# where minpoly is a monic quadratic polynomial in y with integer coefficients,
# defining the imaginary quadratic order R = Z[y]/(minpoly).

def extract_B_C(minpoly, y):
    p = Poly(minpoly, y, domain='EX')
    coeffs = p.all_coeffs()
    if len(coeffs) != 3 or coeffs[0] != 1:
        raise ValueError("minpoly must be a monic quadratic in y")
    B = simplify(coeffs[1])
    C = simplify(coeffs[2])
    if not (B.is_Integer and C.is_Integer):
        raise ValueError("minpoly must have integer coefficients")
    return int(B), int(C)

def is_in_R(elem, y, B, C):
    elem = rem(expand(elem), y**2 + B*y + C, y)
    a = elem.subs(y, 0)
    b = elem.diff(y).subs(y, 0)
    
    def check_int(v):
        v = simplify(v)
        if v.is_Integer:
            return True
        if v.is_Rational and v.q == 1:
            return True
        return False
            
    return check_int(a) and check_int(b)

def is_poly_in_R(poly, x, y, B, C):
    try:
        p = Poly(poly, x, domain='EX')
        for c in p.all_coeffs():
            if not is_in_R(c, y, B, C):
                return False
        return True
    except Exception:
        return False

def is_primitive(f, x, y, B, C):
    p = Poly(f, x, domain='EX')
    coeffs = p.all_coeffs()
    
    norms = []
    for c in coeffs:
        c = rem(expand(c), y**2 + B*y + C, y)
        a = c.subs(y, 0)
        b = c.diff(y).subs(y, 0)
        norm = a**2 - a*b*B + b**2*C
        try:
            norms.append(abs(int(norm)))
        except TypeError:
            return False
            
    if not norms:
        return False
        
    G = functools.reduce(math.gcd, norms)
    if G == 0:
        return False
    if G == 1:
        return True
        
    det = 4*C - B**2
    if det <= 0:
        return False
        
    for d in range(2, G + 1):
        if G % d == 0:
            max_b = int(math.isqrt(4*d // det))
            for b_val in range(-max_b - 1, max_b + 2):
                rem_val = 4*d - b_val**2 * det
                if rem_val < 0:
                    continue
                sq = int(math.isqrt(rem_val))
                if sq * sq == rem_val:
                    for sign in (1, -1):
                        num = sign * sq + b_val * B
                        if num % 2 == 0:
                            a_val = num // 2
                            u = a_val + b_val * y
                            divides_all = True
                            for c in coeffs:
                                u_bar = a_val - b_val * B - b_val * y
                                quot = expand(c * u_bar) / d
                                if not is_in_R(quot, y, B, C):
                                    divides_all = False
                                    break
                            if divides_all:
                                return False
    return True

def invert_F(elem, y, B, C):
    elem = rem(expand(elem), y**2 + B*y + C, y)
    a = elem.subs(y, 0)
    b = elem.diff(y).subs(y, 0)
    norm = a**2 - a*b*B + b**2*C
    if simplify(norm) == 0:
        raise ValueError("Zero division")
    inv_a = (a - b*B) / norm
    inv_b = -b / norm
    return inv_a + inv_b * y

def mul_F(e1, e2, y, B, C):
    prod = expand(e1 * e2)
    return rem(prod, y**2 + B*y + C, y)

def poly_div_F(g, f, x, y, B, C):
    g_poly = Poly(g, x, domain='EX')
    f_poly = Poly(f, x, domain='EX')
    g_coeffs = g_poly.all_coeffs()
    f_coeffs = f_poly.all_coeffs()
    
    def is_zero_expr(expr):
        expr = rem(expand(expr), y**2 + B*y + C, y)
        return simplify(expr) == 0

    if not f_coeffs or all(is_zero_expr(c) for c in f_coeffs):
        return None, False
        
    while f_coeffs and is_zero_expr(f_coeffs[0]):
        f_coeffs.pop(0)
    while g_coeffs and is_zero_expr(g_coeffs[0]):
        g_coeffs.pop(0)
        
    if not g_coeffs:
        return [0], True
        
    if len(g_coeffs) < len(f_coeffs):
        return [], False
        
    lc_f = f_coeffs[0]
    try:
        inv_lc_f = invert_F(lc_f, y, B, C)
    except ValueError:
        return None, False
        
    q_coeffs = [0] * (len(g_coeffs) - len(f_coeffs) + 1)
    r_coeffs = list(g_coeffs)
    
    for i in range(len(q_coeffs)):
        if is_zero_expr(r_coeffs[i]):
            continue
        term = mul_F(r_coeffs[i], inv_lc_f, y, B, C)
        q_coeffs[i] = term
        for j in range(len(f_coeffs)):
            r_coeffs[i+j] = expand(r_coeffs[i+j] - mul_F(term, f_coeffs[j], y, B, C))
            r_coeffs[i+j] = rem(r_coeffs[i+j], y**2 + B*y + C, y)
            
    is_zero = True
    for c in r_coeffs:
        if not is_zero_expr(c):
            is_zero = False
            break
            
    return q_coeffs, is_zero

def divides_in_F(g, f, x, y, B, C):
    q_coeffs, is_zero = poly_div_F(g, f, x, y, B, C)
    return is_zero

def divides_in_R(g, f, x, y, B, C):
    q_coeffs, is_zero = poly_div_F(g, f, x, y, B, C)
    if not is_zero:
        return False
    for c in q_coeffs:
        if not is_in_R(c, y, B, C):
            return False
    return True

def conditions(witness):
    try:
        f, g, x, y, minpoly = witness
    except Exception:
        return [False] * 5
        
    try:
        B, C = extract_B_C(minpoly, y)
    except Exception:
        return [False] * 5
        
    try:
        h1 = (B**2 - 4*C < 0)
    except Exception:
        h1 = False
        
    try:
        h2 = is_poly_in_R(f, x, y, B, C) and is_poly_in_R(g, x, y, B, C)
    except Exception:
        h2 = False
        
    try:
        h3 = is_primitive(f, x, y, B, C)
    except Exception:
        h3 = False
        
    try:
        h4 = divides_in_F(g, f, x, y, B, C)
    except Exception:
        h4 = False
        
    try:
        neg_q = not divides_in_R(g, f, x, y, B, C)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is the field of fractions of R",
    "H_2: f and g are polynomials over R",
    "H_3: f is a primitive polynomial",
    "H_4: f divides g in the polynomial ring over F",
    "not_Q: f does not divide g in the polynomial ring over R"
]

N_HYP = 4
NEG_Q_INDEX = 4