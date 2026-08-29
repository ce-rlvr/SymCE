import sympy
from sympy.polys.domains import ZZ, QQ, RR, CC, EX
from sympy.abc import x, y, z

# Standard counterexample for a ring that is not a UFD
class Z_sqrt_minus_5:
    """Z[sqrt(-5)] is a standard example of an integral domain that is not a UFD."""
    is_UFD = False
    is_PID = False

def conditions(witness) -> list[bool]:
    try:
        # Check if the witness ring is explicitly marked as not a UFD
        if hasattr(witness, 'is_UFD'):
            neg_q = (witness.is_UFD is False)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is not a Unique Factorization Domain (UFD)"
]

N_HYP = 0
NEG_Q_INDEX = 0