import sympy as sp
import math
from sympy.abc import x

def conditions(witness):
    try:
        f_expr, p = witness
    except Exception:
        return [False, False, False, False, False]
        
    # H1: f(x) is a polynomial with integer coefficients of degree n >= 1
    try:
        if isinstance(f_expr, sp.Poly):
            f_poly = f_expr
            gen = f_poly.gen
        else:
            f_expr = sp.sympify(f_expr)
            symbols = f_expr.free_symbols
            if len(symbols) == 1:
                gen = list(symbols)[0]
            else:
                gen = x
            f_poly = sp.Poly(f_expr, gen)
            
        h1 = bool(f_poly.domain.is_ZZ and f_poly.degree() >= 1)
    except Exception:
        h1 = False

    # H2: The leading coefficient and the constant term of f(x) are both non-zero
    try:
        if not h1:
            h2 = False
        else:
            coeffs = f_poly.all_coeffs()
            a_n = coeffs[0]
            a_0 = coeffs[-1]
            h2 = bool((a_n != 0) and (a_0 != 0))
    except Exception:
        h2 = False

    # H3: p is a prime number
    try:
        h3 = bool(sp.isprime(p))
    except Exception:
        h3 = False

    # H4: The single line segment of the Newton polygon contains no integer lattice points other than its two endpoints
    try:
        if not (h1 and h2 and h3):
            h4 = False
        else:
            n = f_poly.degree()
            def v_p(c, p):
                if c == 0: return math.inf
                v = 0
                c = abs(c)
                while c % p == 0:
                    v += 1
                    c //= p
                return v
            
            v_n = v_p(a_n, p)
            v_0 = v_p(a_0, p)
            h4 = bool(math.gcd(n, abs(v_n - v_0)) == 1)
    except Exception:
        h4 = False

    # neg_Q: f(x) is NOT irreducible over Q (i.e., it is reducible over Q)
    try:
        if not h1:
            neg_q = False
        else:
            f_poly_Q = sp.Poly(f_poly, domain='QQ')
            _, factors = f_poly_Q.factor_list()
            # It is irreducible if there is exactly 1 factor and its multiplicity is 1
            is_irreducible = (len(factors) == 1 and factors[0][1] == 1)
            neg_q = not is_irreducible
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial with integer coefficients of degree n >= 1",
    "H_2: The leading coefficient and the constant term of f(x) are both non-zero",
    "H_3: p is a prime number",
    "H_4: The single line segment of the Newton polygon contains no integer lattice points other than its two endpoints",
    "¬Q: f(x) is reducible over Q"
]

N_HYP = 4
NEG_Q_INDEX = 4