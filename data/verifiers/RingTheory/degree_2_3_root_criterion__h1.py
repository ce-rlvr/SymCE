import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, Poly) and witness.is_univariate
    except Exception:
        h1 = False

    try:
        h2 = witness.degree() in (2, 3)
    except Exception:
        h2 = False

    try:
        h3 = len(witness.ground_roots()) == 0
    except Exception:
        h3 = False

    try:
        neg_q = (witness.is_irreducible is False)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a univariate polynomial over F",
    "H_2: The degree of f is either 2 or 3",
    "H_3: f has no roots in F",
    "¬Q: f is reducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3