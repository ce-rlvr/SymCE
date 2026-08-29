import sympy
from sympy import Poly, Symbol

x = Symbol('x')

def conditions(witness):
    try:
        h1_ok = isinstance(witness, Poly) and witness.is_univariate
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(witness.degree() > 0)
    except Exception:
        h2_ok = False

    try:
        domain = witness.domain
        neg_q_ok = not domain.is_Field
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: p is a polynomial over F",
    "H_2: The degree of p is n > 0",
    "¬Q: The factor ring is not a vector space over F of dimension n"
]

N_HYP = 2
NEG_Q_INDEX = 2