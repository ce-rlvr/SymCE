import sympy
from sympy import Poly, Symbol
import math

x = Symbol('x')

def conditions(witness):
    try:
        f, p = witness
    except Exception:
        return [False] * 5

    # H_1: f(x) is a polynomial in Z[x] of degree n >= 1
    try:
        if not isinstance(f, sympy.Expr):
            h1 = False
        else:
            poly_f = Poly(f, x)
            if poly_f.degree() >= 1 and all(isinstance(c, (int, sympy.Integer)) for c in poly_f.all_coeffs()):
                h1 = True
            else:
                h1 = False
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        if isinstance(p, (int, sympy.Integer)) and sympy.isprime(p):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    def v_p(a, p):
        if a == 0:
            return float('inf')
        v = 0
        a = abs(int(a))
        while a > 0 and a % p == 0:
            v += 1
            a //= p
        return v

    # H_3 and H_4
    try:
        if h1 and h2:
            poly_f = Poly(f, x)
            coeffs = poly_f.all_coeffs()
            points = []
            for i, c in enumerate(reversed(coeffs)):
                if c != 0:
                    points.append((i, v_p(c, p)))
            
            if len(points) >= 2:
                x0, y0 = points[0]
                xm, ym = points[-1]
                
                # H_3: The Newton polygon consists of a single line segment
                is_single_segment = True
                for k in range(1, len(points) - 1):
                    xk, yk = points[k]
                    # Check if point is strictly below the segment
                    if (yk - y0) * (xm - x0) < (ym - y0) * (xk - x0):
                        is_single_segment = False
                        break
                h3 = is_single_segment
                
                # H_4: The segment contains no integer lattice points other than its two endpoints
                if h3:
                    if math.gcd(xm - x0, abs(ym - y0)) == 1:
                        h4 = True
                    else:
                        h4 = False
                else:
                    h4 = False
            else:
                h3 = False
                h4 = False
        else:
            h3 = False
            h4 = False
    except Exception:
        h3 = False
        h4 = False

    # neg_Q: f(x) is NOT irreducible over Q
    try:
        if h1:
            factors = sympy.factor_list(f)
            num_non_constant_factors = sum(mult for fac, mult in factors[1] if fac.as_poly(x).degree() > 0)
            if num_non_constant_factors > 1:
                neg_q = True
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial in Z(x) of degree n >= 1",
    "H_2: p is a prime number",
    "H_3: The Newton polygon of f(x) with respect to the p-adic valuation consists of a single line segment",
    "H_4: The single line segment of the Newton polygon contains no integer lattice points other than its two endpoints",
    "¬Q: f(x) is not irreducible over Q"
]

N_HYP = 4
NEG_Q_INDEX = 4