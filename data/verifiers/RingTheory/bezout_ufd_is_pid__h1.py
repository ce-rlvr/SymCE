import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
Z = ZZ
Q = QQ

def conditions(witness) -> list[bool]:
    # H_1: R is a Bezout domain
    try:
        h1_ok = False
        if hasattr(witness, 'is_Bezout') and witness.is_Bezout is not None:
            h1_ok = bool(witness.is_Bezout)
        elif hasattr(witness, 'is_bezout') and witness.is_bezout is not None:
            h1_ok = bool(witness.is_bezout)
        elif hasattr(witness, 'is_PID') and witness.is_PID:
            h1_ok = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h1_ok = True
        elif isinstance(witness, str):
            s = witness.lower()
            if "algebraic integer" in s or "entire function" in s or "non-discrete valuation" in s:
                h1_ok = True
    except Exception:
        h1_ok = False

    # ¬Q: R is NOT a Principal Ideal Domain
    try:
        is_pid = True # Default to True to prevent false positives on neg_Q
        if hasattr(witness, 'is_PID') and witness.is_PID is not None:
            is_pid = bool(witness.is_PID)
        elif hasattr(witness, 'is_pid') and witness.is_pid is not None:
            is_pid = bool(witness.is_pid)
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            is_pid = True
        elif isinstance(witness, str):
            s = witness.lower()
            if "algebraic integer" in s or "entire function" in s or "non-discrete valuation" in s:
                is_pid = False
            else:
                is_pid = True
        
        neg_q = not is_pid
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Bezout domain",
    "¬Q: R is not a Principal Ideal Domain"
]

N_HYP = 1
NEG_Q_INDEX = 1