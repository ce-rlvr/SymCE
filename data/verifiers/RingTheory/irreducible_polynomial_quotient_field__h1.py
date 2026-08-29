import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    try:
        h1 = isinstance(witness, Poly) and witness.is_univariate
    except Exception:
        h1 = False

    try:
        h2 = not witness.is_zero and witness.is_irreducible
    except Exception:
        h2 = False

    try:
        is_field = witness.domain.is_Field and witness.is_irreducible and witness.degree() > 0
        neg_q = not is_field
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = ["H_1: F is a polynomial ring", "H_2: f is a non-zero irreducible polynomial", "¬Q: The quotient ring is not a field"]

N_HYP = 2
NEG_Q_INDEX = 2