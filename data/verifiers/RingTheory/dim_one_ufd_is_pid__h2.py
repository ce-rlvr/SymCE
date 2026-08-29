import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup: named object bindings that the witness expression may reference.
# We provide standard polynomial rings over integers and rationals.
Zx = ZZ.poly_ring(x)
Qx = QQ.poly_ring(x)
Zxy = ZZ.poly_ring(x, y)
Qxy = QQ.poly_ring(x, y)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    """
    # H_1: R is a Unique Factorization Domain that is not a field
    try:
        h1_ok = (witness.is_UFD is True) and (witness.is_Field is False)
    except Exception:
        h1_ok = False

    # ¬Q: R is not a Principal Ideal Domain
    try:
        neg_q_ok = (witness.is_PID is False)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain that is not a field",
    "¬Q: R is not a Principal Ideal Domain"
]

N_HYP = 1
NEG_Q_INDEX = 1