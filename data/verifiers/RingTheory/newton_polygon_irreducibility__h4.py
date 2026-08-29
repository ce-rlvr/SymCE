import sympy
from sympy import Poly, Rational
from sympy.abc import x
import sympy.ntheory
import math

# Top-level setup
# x is available for polynomial expressions

def conditions(witness):
    try:
        f, p = witness
    except Exception:
        return [False] * 5

    # H_1: f is a polynomial over Q with degree n >= 1
    try:
        poly_f = Poly(f, x, domain='QQ')
        n = poly_f.degree()
        h1 = bool(n >= 1)
    except Exception:
        h1 = False

    # H_2: a_0 != 0
    try:
        a0 = poly_f.nth(0)
        h2 = bool(a0 != 0)
    except Exception:
        h2 = False

    # H_3: p is a prime number
    try:
        h3 = bool(sympy.ntheory.isprime(p))
    except Exception:
        h3 = False

    # H_4: gcd(n, v_p(a_n) - v_p(a_0)) == 1
    try:
        an = poly_f.nth(n)
        
        def vp(c, p_val):
            c_rat = Rational(c)
            return sympy.ntheory.multiplicity(p_val, c_rat.p) - sympy.ntheory.multiplicity(p_val, c_rat.q)
            
        vp_an = vp(an, p)
        vp_a0 = vp(a0, p)
        
        h4 = bool(math.gcd(int(n), int(abs(vp_an - vp_a0))) == 1)
    except Exception:
        h4 = False

    # ¬Q: f is reducible over Q
    try:
        factors = sympy.factor_list(poly_f)[1]
        is_irred = (len(factors) == 1 and factors[0][1] == 1)
        neg_q = not is_irred
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial over Q with degree n >= 1",
    "H_2: a_0 != 0",
    "H_3: p is a prime number",
    "H_4: gcd(n, v_p(a_n) - v_p(a_0)) == 1",
    "not Q: f is reducible over Q"
]

N_HYP = 4
NEG_Q_INDEX = 4