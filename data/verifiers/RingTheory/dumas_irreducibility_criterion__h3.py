import sympy as sp
import math

x = sp.Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            f, p_val = witness
            p_list = [p_val]
        else:
            f = witness
            p_list = range(2, 100)
        
        f = f.as_expr() if hasattr(f, 'as_expr') else f
    except Exception:
        return [False] * 5

    try:
        poly_f = sp.Poly(f, x)
        h1 = poly_f.domain.is_ZZ and poly_f.degree() >= 1
    except Exception:
        h1 = False

    try:
        if h1:
            coeffs = poly_f.all_coeffs()
            lc = coeffs[0]
            ct = coeffs[-1]
            h2 = (lc != 0) and (ct != 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    h3 = False
    h4 = False
    try:
        if h1 and h2:
            n = poly_f.degree()
            coeffs = poly_f.all_coeffs()
            
            def vp(c, p):
                if c == 0:
                    return float('inf')
                v = 0
                while c % p == 0:
                    v += 1
                    c //= p
                return v
            
            for p in p_list:
                if not isinstance(p, int) or p < 2:
                    continue
                
                points = []
                for i in range(n + 1):
                    c = coeffs[n - i]
                    if c != 0:
                        points.append((i, vp(c, p)))
                
                v0 = vp(coeffs[-1], p)
                vn = vp(coeffs[0], p)
                
                is_single_segment = True
                for i, v in points:
                    if i == 0 or i == n:
                        continue
                    if n * v < n * v0 + (vn - v0) * i:
                        is_single_segment = False
                        break
                
                if is_single_segment:
                    h3 = True
                    if math.gcd(n, abs(vn - v0)) == 1:
                        h4 = True
                        break
    except Exception:
        pass

    try:
        factors = sp.factor_list(f)
        num_factors = sum(mult for poly, mult in factors[1] if poly.as_poly(x).degree() > 0)
        neg_q = num_factors > 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial in Z(x) of degree n >= 1",
    "H_2: The leading coefficient and the constant term of f(x) are both non-zero",
    "H_3: The Newton polygon of f(x) with respect to the p-adic valuation consists of a single line segment",
    "H_4: The single line segment of the Newton polygon contains no integer lattice points other than its two endpoints",
    "not Q: f(x) is reducible over Q"
]

N_HYP = 4
NEG_Q_INDEX = 4