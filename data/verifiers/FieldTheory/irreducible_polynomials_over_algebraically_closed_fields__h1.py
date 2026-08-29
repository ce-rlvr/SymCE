import sympy
from sympy import Poly
from sympy.abc import x, y, z
from sympy import QQ, ZZ, RR, CC

def conditions(witness) -> list[bool]:
    # H_1: p(x) is a polynomial in K[x] (K must be a field and p(x) univariate)
    try:
        h1 = isinstance(witness, Poly) and witness.domain.is_Field and witness.is_univariate
    except Exception:
        h1 = False

    # H_2: p(x) is irreducible over K
    try:
        h2 = bool(witness.is_irreducible)
    except Exception:
        h2 = False

    # ¬Q: The degree of p(x) is not exactly 1
    try:
        neg_q = witness.degree() != 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p(x) is a univariate polynomial over a field K",
    "H_2: p(x) is irreducible over K",
    "¬Q: The degree of p(x) is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2