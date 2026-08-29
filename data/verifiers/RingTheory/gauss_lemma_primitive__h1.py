import math
from functools import reduce

def conditions(witness):
    try:
        f_coeffs, g_coeffs, d = witness
        d = int(d)
        if d <= 0:
            return [False, False, False]
        if not isinstance(f_coeffs, (list, tuple)) or not isinstance(g_coeffs, (list, tuple)):
            return [False, False, False]
        f_coeffs = [(int(a), int(b)) for a, b in f_coeffs]
        g_coeffs = [(int(a), int(b)) for a, b in g_coeffs]
    except Exception:
        return [False, False, False]

    def norm(a, b):
        return a**2 + d * b**2

    def divides(c_a, c_b, a, b):
        N = norm(c_a, c_b)
        if N == 0: 
            return False
        real_part = a * c_a + d * b * c_b
        imag_part = b * c_a - a * c_b
        return real_part % N == 0 and imag_part % N == 0

    def is_primitive(coeffs):
        norms = [norm(a, b) for a, b in coeffs]
        if not norms or all(n == 0 for n in norms):
            return False
            
        G = reduce(math.gcd, norms)
        
        divs = []
        for i in range(1, math.isqrt(G) + 1):
            if G % i == 0:
                divs.append(i)
                if i * i != G:
                    divs.append(G // i)
                    
        for k in divs:
            if k == 1: 
                continue
            max_y = math.isqrt(k // d)
            for y in range(-max_y, max_y + 1):
                rem = k - d * y**2
                if rem < 0: 
                    continue
                x = math.isqrt(rem)
                if x * x == rem:
                    for c_a, c_b in [(x, y), (-x, y)]:
                        if all(divides(c_a, c_b, a, b) for a, b in coeffs):
                            return False
        return True

    def poly_mul(f, g):
        if not f or not g: 
            return []
        deg_f = len(f) - 1
        deg_g = len(g) - 1
        res = [(0, 0)] * (deg_f + deg_g + 1)
        for i, (fa, fb) in enumerate(f):
            for j, (ga, gb) in enumerate(g):
                ra, rb = res[i+j]
                ca = fa * ga - d * fb * gb
                cb = fa * gb + fb * ga
                res[i+j] = (ra + ca, rb + cb)
        return res

    try:
        h1 = is_primitive(f_coeffs)
    except Exception:
        h1 = False

    try:
        h2 = is_primitive(g_coeffs)
    except Exception:
        h2 = False

    try:
        fg_coeffs = poly_mul(f_coeffs, g_coeffs)
        neg_q = not is_primitive(fg_coeffs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a primitive polynomial",
    "H_2: g is a primitive polynomial",
    "not Q: f*g is not a primitive polynomial"
]

N_HYP = 2
NEG_Q_INDEX = 2