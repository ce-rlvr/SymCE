import math
from sympy import isprime
from sympy.polys import cyclotomic_poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness['p']
            a = witness['a']
            d = witness['d']
        else:
            p, a, d = witness
    except Exception:
        return [False, False, False]

    try:
        d_int = int(d)
        h1 = bool(isprime(p)) and (d_int == d) and (d_int >= 1)
    except Exception:
        h1 = False

    try:
        a_int = int(a)
        p_int = int(p)
        h2 = (a_int == a) and (math.gcd(a_int, p_int) == 1)
    except Exception:
        h2 = False

    try:
        poly = cyclotomic_poly(int(d), x)
        val = int(poly.subs(x, int(a)))
        neg_q = (val % int(p)) != 0
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number and d is a positive integer",
    "H_2: a is an integer coprime to p",
    "¬Q: p does not divide Phi_d(a)"
]

N_HYP = 2
NEG_Q_INDEX = 2