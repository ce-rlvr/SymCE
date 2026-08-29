import sympy
from sympy import Poly
from sympy.abc import x
from sympy.ntheory import isprime

def conditions(witness):
    try:
        p = Poly(witness, x)
        h1 = p.is_monic and all(sympy.S(c).is_integer for c in p.coeffs())
    except Exception:
        h1 = False

    try:
        p = Poly(witness, x)
        h2 = p.degree() >= 1
    except Exception:
        h2 = False

    try:
        p = Poly(witness, x)
        a0 = p.nth(0)
        if not sympy.S(a0).is_integer:
            h3 = False
        else:
            h3 = isprime(abs(int(a0)))
    except Exception:
        h3 = False

    try:
        _, factors = sympy.factor_list(witness, domain='QQ')
        num_factors = sum(exp for f, exp in factors if Poly(f, x).degree() >= 1)
        neg_q = num_factors > 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f(x) is a monic polynomial over Z",
    "H_2: The degree n of f(x) is at least 1",
    "H_3: a_0 = p or a_0 = -p for some prime number p",
    "¬Q: f(x) is reducible over Q"
]

N_HYP = 3
NEG_Q_INDEX = 3