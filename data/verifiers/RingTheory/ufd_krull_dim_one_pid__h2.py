import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup: common rings that might be used as witnesses
Z_x = ZZ[x]
Q_x = QQ[x]
Z_x_y = ZZ[x, y]
Q_x_y = QQ[x, y]

def conditions(witness) -> list[bool]:
    try:
        # Check if the witness is explicitly a UFD
        h1 = getattr(witness, 'is_UFD', False) is True
    except Exception:
        h1 = False

    try:
        # Check if the witness is explicitly NOT a PID
        is_pid = getattr(witness, 'is_PID', None)
        neg_q = (is_pid is False)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "¬Q: R is not a principal ideal domain"
]

N_HYP = 1
NEG_Q_INDEX = 1