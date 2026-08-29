import sympy as sp
from sympy import Poly, Symbol
import math

# Top-level setup for witness expressions
x = Symbol('x')
a = Symbol('a')

def get_common_divisors(coeffs, D):
    def norm(c):
        c_poly = sp.Poly(c, a, domain='ZZ')
        if c_poly.degree() > 1:
            _, rem = c_poly.div(sp.Poly(a**2 + D, a, domain='ZZ'))
            c_poly = rem
        if c_poly.degree() == 1:
            v = int(c_poly.coeffs()[0])
            u = int(c_poly.coeffs()[1])
        elif c_poly.degree() == 0:
            v = 0
            u = int(c_poly.coeffs()[0])
        else:
            v = 0
            u = 0
        return u**2 + D * v**2

    norms = [norm(c) for c in coeffs]
    non_zero_norms = [n for n in norms if n != 0]
    if not non_zero_norms:
        return [(2, 0)] # Dummy non-unit divisor for zero polynomial
        
    g = math.gcd(*non_zero_norms)
    
    divisors = []
    max_y = int(math.isqrt(g // D)) if D > 0 else 0
    for y in range(-max_y, max_y + 1):
        rem = g - D * y**2
        if rem < 0: continue
        max_x = int(math.isqrt(rem))
        for x_val in range(-max_x, max_x + 1):
            n_d = x_val**2 + D * y**2
            if n_d == 0: continue
            if g % n_d == 0:
                divides_all = True
                for c in coeffs:
                    c_poly = sp.Poly(c, a, domain='ZZ')
                    if c_poly.degree() > 1:
                        _, rem_poly = c_poly.div(sp.Poly(a**2 + D, a, domain='ZZ'))
                        c_poly = rem_poly
                    if c_poly.degree() == 1:
                        v = int(c_poly.coeffs()[0])
                        u = int(c_poly.coeffs()[1])
                    elif c_poly.degree() == 0:
                        v = 0
                        u = int(c_poly.coeffs()[0])
                    else:
                        v = 0
                        u = 0
                    
                    real_part = u*x_val + D*v*y
                    imag_part = v*x_val - u*y
                    if real_part % n_d != 0 or imag_part % n_d != 0:
                        divides_all = False
                        break
                if divides_all:
                    divisors.append((x_val, y))
    return divisors

def is_primitive(poly_expr, D):
    try:
        p = sp.Poly(poly_expr, x)
        coeffs = p.all_coeffs()
        for c in coeffs:
            _ = sp.Poly(c, a, domain='ZZ')
    except Exception:
        return False
    
    divs = get_common_divisors(coeffs, D)
    if not divs:
        return False
    for (dx, dy) in divs:
        if dx**2 + D * dy**2 != 1:
            return False
    return True

def to_ab(c_expr, D):
    c_expr = sp.simplify(c_expr)
    re = sp.re(c_expr)
    im = sp.im(c_expr)
    u = sp.Rational(sp.simplify(re))
    v = sp.Rational(sp.simplify(im / sp.sqrt(D)))
    return u, v

def get_monic_divisors(H_sub, D):
    facs = sp.factor_list(H_sub, x, extension=[sp.sqrt(-D)])
    divs = [sp.Poly(1, x, extension=[sp.sqrt(-D)])]
    for p_expr, exp in facs[1]:
        p = sp.Poly(p_expr, x, extension=[sp.sqrt(-D)]).monic()
        new_divs = []
        for d in divs:
            for k in range(exp + 1):
                new_divs.append(d * p**k)
        divs = new_divs
    return [d for d in divs if d.degree() >= 1]

def check_rp_K(f_expr, g_expr, D):
    f_sub = f_expr.subs(a, sp.sqrt(-D))
    g_sub = g_expr.subs(a, sp.sqrt(-D))
    H_sub = sp.gcd(f_sub, g_sub, extension=[sp.sqrt(-D)])
    H_poly = sp.Poly(H_sub, x, extension=[sp.sqrt(-D)])
    return H_poly.degree() == 0

def check_rp_R(f_expr, g_expr, D):
    f_sub = f_expr.subs(a, sp.sqrt(-D))
    g_sub = g_expr.subs(a, sp.sqrt(-D))
    
    H_sub = sp.gcd(f_sub, g_sub, extension=[sp.sqrt(-D)])
    H_poly = sp.Poly(H_sub, x, extension=[sp.sqrt(-D)])
    
    if H_poly.degree() == 0:
        return True
        
    divs = get_monic_divisors(H_sub, D)
    
    f_poly = sp.Poly(f_sub, x, extension=[sp.sqrt(-D)])
    g_poly = sp.Poly(g_sub, x, extension=[sp.sqrt(-D)])
    
    for P in divs:
        f1_poly, _ = f_poly.div(P)
        g1_poly, _ = g_poly.div(P)
        
        lc_f1 = f1_poly.LC()
        u_lc, v_lc = to_ab(lc_f1, D)
        if u_lc.q != 1 or v_lc.q != 1:
            continue
            
        N_lc = int(u_lc.p)**2 + D * int(v_lc.p)**2
        if N_lc == 0:
            continue
            
        candidates = []
        max_y = int(math.isqrt(N_lc // D)) if D > 0 else 0
        for y in range(-max_y, max_y + 1):
            rem = N_lc - D * y**2
            if rem < 0: continue
            max_x = int(math.isqrt(rem))
            for x_val in range(-max_x, max_x + 1):
                n_c = x_val**2 + D * y**2
                if n_c == 0: continue
                if N_lc % n_c == 0:
                    candidates.append((x_val, y, n_c))
                    
        P_coeffs = [to_ab(c, D) for c in P.all_coeffs()]
        f1_coeffs = [to_ab(c, D) for c in f1_poly.all_coeffs()]
        g1_coeffs = [to_ab(c, D) for c in g1_poly.all_coeffs()]
        
        for x_val, y, n_c in candidates:
            works = True
            for u, v in P_coeffs:
                re = x_val * u - D * y * v
                im = x_val * v + y * u
                if re.q != 1 or im.q != 1:
                    works = False
                    break
            if not works: continue
            
            for u, v in f1_coeffs:
                re = (u * x_val + D * v * y) / n_c
                im = (v * x_val - u * y) / n_c
                if re.q != 1 or im.q != 1:
                    works = False
                    break
            if not works: continue
            
            for u, v in g1_coeffs:
                re = (u * x_val + D * v * y) / n_c
                im = (v * x_val - u * y) / n_c
                if re.q != 1 or im.q != 1:
                    works = False
                    break
            if not works: continue
            
            return False
            
    return True

def conditions(witness):
    try:
        D, f_expr, g_expr = witness
        if not (isinstance(D, int) and D > 0):
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    h1_ok = True
    
    try:
        f_prim = is_primitive(f_expr, D)
        g_prim = is_primitive(g_expr, D)
        h2_ok = bool(f_prim and g_prim)
    except Exception:
        h2_ok = False
        
    try:
        rp_R = check_rp_R(f_expr, g_expr, D)
        rp_K = check_rp_K(f_expr, g_expr, D)
        neg_q = bool(rp_R != rp_K)
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "H_2: f and g are primitive polynomials over R",
    "neg_Q: f and g are relatively prime over R iff they are relatively prime over K"
]

N_HYP = 2
NEG_Q_INDEX = 2