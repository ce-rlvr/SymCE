import sympy
from sympy import Poly, factor_list
from sympy.abc import x, y

def conditions(witness) -> list[bool]:
    try:
        p = Poly(witness, x, y)
        h1 = bool(p.degree(y) <= 1)
    except Exception:
        h1 = False

    try:
        p = Poly(witness, x, y)
        h2 = bool(p.degree(y) == 1)
    except Exception:
        h2 = False

    try:
        _, factors = factor_list(witness, x, y)
        total_factors = sum(mult for f, mult in factors)
        neg_q = bool(total_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial of the form g(x)y + h(x)",
    "H_2: g(x) is not the zero polynomial",
    "¬Q: f is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2