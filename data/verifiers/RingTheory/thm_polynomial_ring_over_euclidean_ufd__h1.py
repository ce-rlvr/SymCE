import sympy
from sympy.polys.domains import ZZ, QQ, EX, RR, CC

def conditions(witness) -> list[bool]:
    try:
        h1 = hasattr(witness, 'poly_ring') or hasattr(witness, 'is_Ring')
    except Exception:
        h1 = False

    try:
        x_sym = sympy.Symbol('x')
        if hasattr(witness, 'poly_ring'):
            Rx = witness.poly_ring(x_sym)
            neg_q = (getattr(Rx, 'is_UFD', None) is False)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "¬Q: polynomial ring over R is not a unique factorization domain"
]

N_HYP = 1
NEG_Q_INDEX = 1