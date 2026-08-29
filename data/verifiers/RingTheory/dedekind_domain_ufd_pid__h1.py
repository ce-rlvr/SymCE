import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y

# Top-level setup: named object bindings that the witness expression may reference.
Z_x = ZZ[x]
Q_x_y = QQ[x, y]
Q_x = QQ[x]

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture:
    'R is a unique factorization domain if and only if R is a principal ideal domain.'
    """
    try:
        # Evaluate whether the witness is a UFD and a PID.
        is_ufd = bool(witness.is_UFD)
        is_pid = bool(witness.is_PID)
        
        # The conclusion is "R is a UFD iff R is a PID".
        # The negation is that one is true and the other is false.
        neg_q = (is_ufd != is_pid)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is a UFD but not a PID (or vice versa)"
]

N_HYP = 0
NEG_Q_INDEX = 0