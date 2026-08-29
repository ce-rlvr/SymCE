import sympy as sp
import math

x = sp.Symbol('x')

# Expected witness format:
# A tuple (d, f_coeffs, g_coeffs) representing polynomials over Z[\sqrt{d}]
# where d is a negative integer (e.g., -5).
# f_coeffs and g_coeffs are lists of tuples (a, b) representing the coefficient a + b\sqrt{d}
# for each power of x, in ascending order of degree.
#
# Alternatively, the witness can be a tuple of SymPy expressions (f_expr, g_expr)
# or (d, f_expr, g_expr).

def get_divisors(c_a, c_b, d):
    if c_a == 0 and c_b == 0:
        return None
    norm = c_a**2 - d * c_b**2
    norm = abs(norm)
    if norm > 10**12:
        raise ValueError("Norm too large")
        
    int_divs = set()
    for i in range(1, math.isqrt(norm) + 1):
        if norm % i == 0:
            int_divs.add(i)
            int_divs.add(norm // i)
            
    divisors = set()
    abs_d = -d
    for k in int_divs:
        max_y = int(math.isqrt(k // abs_d)) + 1
        for y in range(-max_y, max_y + 1):
            rem = k - abs_d * y**2
            if rem >= 0:
                x_val = math.isqrt(rem)
                if x_val**2 == rem:
                    if k != 0:
                        if (c_a * x_val - c_b * y * d) % k == 0 and (c_b * x_val - c_a * y) % k == 0:
                            divisors.add((x_val, y))
                    if x_val != 0 and k != 0:
                        if (c_a * (-x_val) - c_b * y * d) % k == 0 and (c_b * (-x_val) - c_a * y) % k == 0:
                            divisors.add((-x_val, y))
    return divisors

def is_primitive(coeffs, d):
    if not coeffs:
        return False
    common_divs = None
    for c_a, c_b in coeffs:
        divs = get_divisors(c_a, c_b, d)
        if divs is None:
            continue
        if common_divs is None:
            common_divs = divs
        else:
            common_divs = common_divs.intersection(divs)
            
    if common_divs is None:
        return False
        
    for x_val, y in common_divs:
        if x_val**2 - d * y**2 != 1:
            return False
    return True

def mul_coeffs(f, g, d):
    deg_f = len(f) - 1
    deg_g = len(g) - 1
    if deg_f < 0 or deg_g < 0:
        return []
    res = [(0, 0)] * (deg_f + deg_g + 1)
    for i in range(deg_f + 1):
        for j in range(deg_g + 1):
            a1, b1 = f[i]
            a2, b2 = g[j]
            ra, rb = res[i+j]
            res[i+j] = (ra + a1*a2 + b1*b2*d, rb + a1*b2 + b1*a2)
    return res

def parse_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 3:
        d, f, g = witness
        if isinstance(d, int) and d < 0 and isinstance(f, list) and isinstance(g, list):
            return d, f, g
            
    if isinstance(witness, tuple) and len(witness) == 3:
        d, f_expr, g_expr = witness
        if isinstance(d, int) and d < 0:
            try:
                f_expr = sp.sympify(f_expr)
                g_expr = sp.sympify(g_expr)
                def get_coeffs(expr):
                    poly = sp.Poly(expr, x)
                    coeffs = poly.all_coeffs()
                    res = []
                    for c in coeffs:
                        c = sp.expand(c)
                        re, im = c.as_real_imag()
                        a = int(re)
                        if d == -1:
                            b = int(im)
                        else:
                            b_expr = sp.simplify(im / sp.sqrt(-d))
                            b = int(b_expr)
                        res.append((a, b))
                    return res[::-1]
                return d, get_coeffs(f_expr), get_coeffs(g_expr)
            except Exception:
                pass

    if isinstance(witness, tuple) and len(witness) == 2:
        try:
            f_expr, g_expr = witness
            f_expr = sp.sympify(f_expr)
            g_expr = sp.sympify(g_expr)
            
            d = None
            for expr in (f_expr, g_expr):
                if sp.I in expr.atoms():
                    has_sqrt = False
                    for atom in expr.atoms(sp.Pow):
                        if atom.exp == sp.Rational(1, 2) or atom.exp == 0.5:
                            base = atom.base
                            if base.is_Integer and base > 0:
                                d = -int(base)
                                has_sqrt = True
                                break
                    if not has_sqrt:
                        d = -1
                if d is not None:
                    break
            if d is None:
                d = -1
                
            def get_coeffs(expr):
                poly = sp.Poly(expr, x)
                coeffs = poly.all_coeffs()
                res = []
                for c in coeffs:
                    c = sp.expand(c)
                    re, im = c.as_real_imag()
                    a = int(re)
                    if d == -1:
                        b = int(im)
                    else:
                        b_expr = sp.simplify(im / sp.sqrt(-d))
                        b = int(b_expr)
                    res.append((a, b))
                return res[::-1]
                
            return d, get_coeffs(f_expr), get_coeffs(g_expr)
        except Exception:
            pass
            
    return None, None, None

def conditions(witness):
    try:
        d, f_coeffs, g_coeffs = parse_witness(witness)
        if d is None or d >= 0:
            return [False, False, False]
            
        h1 = is_primitive(f_coeffs, d)
        h2 = is_primitive(g_coeffs, d)
        
        fg_coeffs = mul_coeffs(f_coeffs, g_coeffs, d)
        q = is_primitive(fg_coeffs, d)
        neg_q = not q
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = ["H_1: f is a primitive polynomial", "H_2: g is a primitive polynomial", "¬Q: The product polynomial fg is not primitive"]
N_HYP = 2
NEG_Q_INDEX = 2