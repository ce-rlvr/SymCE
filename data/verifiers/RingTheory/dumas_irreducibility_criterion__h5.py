import sympy
from sympy import Poly, isprime
from sympy.abc import x
from sympy import factor_list

def conditions(witness):
    try:
        f_expr, p = witness
    except Exception:
        return [False] * 5
    
    try:
        f_poly = Poly(f_expr, x)
        h1 = f_poly.domain.is_ZZ and f_poly.degree() >= 1
    except Exception:
        h1 = False

    try:
        if h1:
            coeffs = f_poly.all_coeffs()
            a_n = coeffs[0]
            a_0 = coeffs[-1]
            h2 = (a_n != 0) and (a_0 != 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        h3 = isprime(p)
    except Exception:
        h3 = False

    try:
        if h1 and h2 and h3:
            def v_p(n_val, p_val):
                if n_val == 0:
                    return float('inf')
                v = 0
                n_val = abs(n_val)
                while n_val % p_val == 0:
                    v += 1
                    n_val //= p_val
                return v
            
            n = f_poly.degree()
            coeffs = f_poly.all_coeffs()
            a = {i: coeffs[n - i] for i in range(n + 1)}
            
            v0 = v_p(a[0], p)
            vn = v_p(a[n], p)
            
            h4 = True
            for i in range(1, n):
                vi = v_p(a[i], p)
                if vi == float('inf'):
                    continue
                if n * vi < n * v0 + i * (vn - v0):
                    h4 = False
                    break
        else:
            h4 = False
    except Exception:
        h4 = False

    try:
        if h1:
            factors = factor_list(f_expr, domain='QQ')[1]
            neg_q = sum(mult for factor, mult in factors) > 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Z of degree n >= 1",
    "H_2: The leading coefficient and the constant term of f(x) are both non-zero",
    "H_3: p is a prime number",
    "H_4: The Newton polygon of f(x) with respect to the p-adic valuation consists of a single line segment",
    "¬Q: f(x) is reducible over Q"
]

N_HYP = 4
NEG_Q_INDEX = 4