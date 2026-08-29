import sympy
from sympy import isprime
from sympy.abc import x
from sympy.polys import cyclotomic_poly

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
        else:
            n, p = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = (int(n) == n) and (n >= 1)
    except Exception:
        h1 = False

    try:
        h2 = (int(p) == p) and isprime(p)
    except Exception:
        h2 = False

    try:
        h3 = (n % p == 0)
    except Exception:
        h3 = False

    try:
        poly1 = cyclotomic_poly(int(p) * int(n), x)
        poly2 = cyclotomic_poly(int(n), x**int(p))
        neg_q = sympy.expand(poly1 - poly2) != 0
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: p is a prime number",
    "H_3: p divides n",
    "¬Q: \Phi_{pn}(x) != \Phi_n(x^p)"
]

N_HYP = 3
NEG_Q_INDEX = 3