import sympy
from sympy import ZZ, QQ, Symbol
from sympy.abc import x

# Top-level setup
ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)

def conditions(witness) -> list[bool]:
    # H_1: R is a polynomial ring in one variable
    try:
        h1 = bool(getattr(witness, 'is_PolynomialRing', False) and len(witness.gens) == 1)
    except Exception:
        h1 = False

    # ¬Q: R is not a Euclidean domain with respect to the degree function
    try:
        base_ring = witness.domain
        neg_q = not bool(getattr(base_ring, 'is_Field', False))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a polynomial ring in one variable",
    "¬Q: R is not a Euclidean domain with respect to the degree function"
]

N_HYP = 1
NEG_Q_INDEX = 1