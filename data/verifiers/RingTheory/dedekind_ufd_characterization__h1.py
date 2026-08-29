import sympy
from sympy import symbols
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def conditions(witness):
    """
    Check if the witness is a counterexample to the conjecture:
    "R is a unique factorization domain if and only if R is a principal ideal domain."
    
    Since there are no remaining hypotheses, we only check if the conclusion fails.
    The conclusion fails if R is a UFD but not a PID, or R is a PID but not a UFD.
    """
    try:
        is_ufd = witness.is_UFD
        is_pid = witness.is_PID
        
        # If sympy cannot determine the properties, we cannot confirm it's a counterexample
        if is_ufd is None or is_pid is None:
            neg_q = False
        else:
            neg_q = (bool(is_ufd) != bool(is_pid))
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is a UFD but not a PID (or R is a PID but not a UFD)"
]

N_HYP = 0
NEG_Q_INDEX = 0