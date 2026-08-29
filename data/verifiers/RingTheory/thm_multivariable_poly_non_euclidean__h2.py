import sympy
from sympy.polys.domains import QQ, ZZ, RR, CC
from sympy.abc import x, y, z, t

def conditions(witness):
    try:
        h1 = bool(getattr(witness, 'domain', None) is not None and witness.domain.is_Field)
    except Exception:
        h1 = False

    try:
        is_poly_ring = False
        if getattr(witness, 'is_PolynomialRing', False):
            is_poly_ring = True
        elif 'PolyRing' in type(witness).__name__ or 'PolynomialRing' in type(witness).__name__:
            is_poly_ring = True
        elif hasattr(witness, 'symbols') and hasattr(witness, 'domain') and hasattr(witness, 'from_dict'):
            is_poly_ring = True
        h2 = bool(is_poly_ring)
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            neg_q = len(witness.symbols) <= 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: R is a polynomial ring over F",
    "¬Q: R is a Euclidean domain"
]

N_HYP = 2
NEG_Q_INDEX = 2