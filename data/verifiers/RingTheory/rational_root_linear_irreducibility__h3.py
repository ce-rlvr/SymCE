import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    try:
        f = Poly(witness, x, domain='ZZ')
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        f = Poly(witness, x)
        h2_ok = bool(f.degree() >= 2)
    except Exception:
        h2_ok = False

    try:
        factors = sympy.factor_list(witness, x, domain='QQ')[1]
        neg_q_ok = bool(any(sympy.degree(fac, x) == 1 for fac, mult in factors))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a polynomial over Z",
    "H_2: The degree of f is at least 2",
    "not Q: f has a linear factor over Q"
]

N_HYP = 2
NEG_Q_INDEX = 2