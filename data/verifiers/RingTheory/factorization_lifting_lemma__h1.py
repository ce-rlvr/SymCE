import sympy
import math

x = sympy.Symbol('x')

def is_integer(val):
    try:
        res = sympy.sympify(val).is_integer
        return res is True
    except Exception:
        return False

def is_rational(val):
    try:
        res = sympy.sympify(val).is_rational
        return res is True
    except Exception:
        return False

def get_uv(expr, d):
    expr = sympy.sympify(expr)
    if d is not None:
        expr = sympy.radsimp(expr)
    expr = sympy.expand(expr)
    if d is None:
        return expr, sympy.Integer(0)
    sq = sympy.sqrt(d)
    v = expr.coeff(sq)
    u = sympy.expand(expr - v * sq)
    return u, v

def is_in_R(expr, d):
    u, v = get_uv(expr, d)
    return is_integer(u) and is_integer(v)

def is_in_F(expr, d):
    u, v = get_uv(expr, d)
    return is_rational(u) and is_rational(v)

def check_a_exists(G_coeffs, H_coeffs, d):
    sq = sympy.sqrt(d)
    
    c_G = None
    min_norm_G = None
    for c in G_coeffs:
        u, v = get_uv(c, d)
        n = u**2 - d * v**2
        if n != 0:
            if min_norm_G is None or n < min_norm_G:
                min_norm_G = n
                c_G = c
                
    c_H = None
    min_norm_H = None
    for c in H_coeffs:
        u, v = get_uv(c, d)
        n = u**2 - d * v**2
        if n != 0:
            if min_norm_H is None or n < min_norm_H:
                min_norm_H = n
                c_H = c
                
    if c_G is None or c_H is None:
        return True
        
    MaxN = min_norm_G * min_norm_H
    
    max_u = math.floor(math.sqrt(float(MaxN)))
    max_v = math.floor(math.sqrt(float(MaxN / (-d))))
    
    for u in range(-max_u - 1, max_u + 2):
        for v in range(-max_v - 1, max_v + 2):
            r = u + v * sq
            n_r = u**2 - d * v**2
            if n_r == 0 or n_r > MaxN:
                continue
                
            a = sympy.radsimp(r / c_H)
            if a == 0:
                continue
                
            aH_ok = True
            for c in H_coeffs:
                if not is_in_R(a * c, d):
                    aH_ok = False
                    break
            if not aH_ok:
                continue
                
            Ga_ok = True
            for c in G_coeffs:
                if not is_in_R(c / a, d):
                    Ga_ok = False
                    break
            if not Ga_ok:
                continue
                
            return True
            
    return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            d, f, G, H = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H1: F is the field of fractions of R
    try:
        h1 = isinstance(d, int) and d < 0
    except Exception:
        h1 = False
        
    # H2: f is a polynomial in R[x]
    try:
        f_poly = sympy.Poly(f, x)
        h2 = all(is_in_R(c, d) for c in f_poly.all_coeffs())
    except Exception:
        h2 = False
        
    # H3: G and H are polynomials in F[x] such that f = GH
    try:
        G_poly = sympy.Poly(G, x)
        H_poly = sympy.Poly(H, x)
        G_in_F = all(is_in_F(c, d) for c in G_poly.all_coeffs())
        H_in_F = all(is_in_F(c, d) for c in H_poly.all_coeffs())
        f_eq_GH = sympy.expand(f - G * H) == 0
        h3 = G_in_F and H_in_F and f_eq_GH
    except Exception:
        h3 = False
        
    # neg_Q: The conclusion fails
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            G_coeffs = G_poly.all_coeffs()
            H_coeffs = H_poly.all_coeffs()
            a_exists = check_a_exists(G_coeffs, H_coeffs, d)
            neg_q = not a_exists
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: F is the field of fractions of R", "H_2: f is a polynomial over R", "H_3: G and H are polynomials over F such that f = GH", "not_Q: There do not exist g, h over R and non-zero a, b in F such that G = ag, H = bh, and f = gh"]

N_HYP = 3
NEG_Q_INDEX = 3