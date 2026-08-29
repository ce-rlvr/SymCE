import sympy
from sympy.abc import x
from sympy.polys.domains import ZZ, QQ, RR, CC, FF

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(witness.is_Field)
    except Exception:
        h1 = False

    try:
        ring = witness.poly_ring(x)
        neg_q = not bool(ring.is_PID)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: F is a field",
    "not Q: F polynomial ring is not a Principal Ideal Domain"
]

N_HYP: int = 1
NEG_Q_INDEX: int = 1