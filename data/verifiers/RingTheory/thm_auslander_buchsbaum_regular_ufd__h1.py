import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC, EX
from sympy.abc import x, y, z

Z = ZZ
Q = QQ

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture.
    The conjecture claims that any ring is a UFD.
    We check if the witness is NOT a UFD.
    """
    try:
        # In sympy, domains have the is_UFD property.
        is_ufd = bool(witness.is_UFD)
        neg_q = not is_ufd
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is not a unique factorization domain"
]

N_HYP = 0
NEG_Q_INDEX = 0