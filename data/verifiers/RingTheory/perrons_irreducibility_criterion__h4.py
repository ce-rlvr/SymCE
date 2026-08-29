import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    # H_1: n is an integer with n >= 2
    try:
        p = Poly(witness, x)
        n = p.degree()
        h1 = bool(n >= 2)
    except Exception:
        h1 = False

    # H_2: f(x) is a monic polynomial with integer coefficients
    try:
        p = Poly(witness, x)
        is_monic = (p.LC() == 1)
        is_Z_x = (p.domain == sympy.ZZ)
        h2 = bool(is_monic and is_Z_x)
    except Exception:
        h2 = False

    # H_3: a_0 is not equal to 0
    try:
        p = Poly(witness, x)
        a_0 = p.nth(0)
        h3 = bool(a_0 != 0)
    except Exception:
        h3 = False

    # ¬Q: f(x) is reducible over the rational numbers Q
    try:
        factors = sympy.factor_list(witness, domain='QQ')
        num_factors = sum(mult for fac, mult in factors[1])
        neg_q = bool(num_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer with n >= 2",
    "H_2: f(x) is a monic polynomial with integer coefficients",
    "H_3: a_0 is not equal to 0",
    "¬Q: f(x) is reducible over the rational numbers Q"
]

N_HYP = 3
NEG_Q_INDEX = 3