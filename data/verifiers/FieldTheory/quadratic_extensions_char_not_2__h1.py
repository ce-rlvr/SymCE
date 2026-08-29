import sympy
from sympy import Poly, Symbol, QQ, ZZ, GF
from sympy.abc import x, y, z, t

def conditions(witness):
    try:
        h1 = bool(witness.domain.char != 2)
    except Exception:
        h1 = False

    try:
        h2 = bool(witness.domain.is_Field and witness.is_univariate and witness.degree() == 2 and witness.is_irreducible)
    except Exception:
        h2 = False

    try:
        neg_q = not bool(witness.gcd(witness.diff()).degree() == 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: The characteristic of F is not equal to 2",
    "H_2: E is a field extension of F such that the degree of E over F is exactly 2",
    "not Q: E is not a Galois extension of F"
]

N_HYP = 2
NEG_Q_INDEX = 2