import sympy
from sympy import Poly, factor_list
from sympy.abc import x
from sympy.ntheory import multiplicity
import math

def v_p(c, p):
    if c == 0:
        return float('inf')
    c = sympy.Rational(c)
    return multiplicity(p, abs(c.p)) - multiplicity(p, abs(c.q))

def conditions(witness):
    try:
        f, p = witness
        f_poly = Poly(f, x, domain='QQ')
        coeffs = f_poly.all_coeffs()
        coeffs.reverse()
        n = len(coeffs) - 1
        
        # H_1: The leading coefficient and the constant term of f(x) are both non-zero
        try:
            h1 = bool((coeffs[0] != 0) and (coeffs[-1] != 0))
        except Exception:
            h1 = False
            
        # H_2: p is a prime number
        try:
            h2 = bool(sympy.isprime(p))
        except Exception:
            h2 = False
            
        # H_3: The Newton polygon of f(x) with respect to the p-adic valuation consists of a single line segment
        try:
            if n < 0:
                h3 = False
            elif n == 0:
                h3 = True
            else:
                v = [v_p(c, p) for c in coeffs]
                v0 = v[0]
                vn = v[n]
                if v0 == float('inf') or vn == float('inf'):
                    h3 = False
                else:
                    h3 = True
                    for i in range(1, n):
                        if v[i] != float('inf'):
                            if n * v[i] < n * v0 + i * (vn - v0):
                                h3 = False
                                break
        except Exception:
            h3 = False
            
        # H_4: The single line segment of the Newton polygon contains no integer lattice points other than its two endpoints
        try:
            if n < 0:
                h4 = False
            elif n == 0:
                h4 = True
            else:
                v = [v_p(c, p) for c in coeffs]
                v0 = v[0]
                vn = v[n]
                if v0 == float('inf') or vn == float('inf'):
                    h4 = False
                else:
                    h4 = bool(math.gcd(n, abs(vn - v0)) == 1)
        except Exception:
            h4 = False
            
        # ¬Q: f(x) is not irreducible over Q
        try:
            _, factors = factor_list(f_poly)
            num_factors = sum(mult for fac, mult in factors if fac.degree() > 0)
            neg_q = bool(num_factors != 1)
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: The leading coefficient and the constant term of f(x) are both non-zero",
    "H_2: p is a prime number",
    "H_3: The Newton polygon of f(x) with respect to the p-adic valuation consists of a single line segment",
    "H_4: The single line segment of the Newton polygon contains no integer lattice points other than its two endpoints",
    "¬Q: f(x) is not irreducible over Q"
]

N_HYP = 4
NEG_Q_INDEX = 4