import sympy
from sympy import Symbol, Poly
from sympy.ntheory import isprime

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        f, p = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        poly_f = Poly(f, x)
        h1_ok = all(c.is_integer for c in poly_f.coeffs())
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(poly_f.degree() >= 1)
    except Exception:
        h2_ok = False

    try:
        a_n = poly_f.LC()
        h3_ok = bool(isprime(p) and (a_n % p != 0))
    except Exception:
        h3_ok = False

    try:
        a_0 = poly_f.nth(0)
        h4_ok = bool((a_0 % (p**2)) != 0)
    except Exception:
        h4_ok = False

    try:
        factors = sympy.factor_list(f, domain='QQ')
        is_irred = (len(factors[1]) == 1) and (factors[1][0][1] == 1)
        neg_q_ok = not is_irred
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, h4_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain with field of fractions K",
    "H_2: f(x) is a polynomial over R of degree n >= 1",
    "H_3: There exists a prime element p in R such that p does not divide a_n",
    "H_4: p^2 does not divide a_0",
    "¬Q: f(x) is reducible over K"
]

N_HYP = 4
NEG_Q_INDEX = 4