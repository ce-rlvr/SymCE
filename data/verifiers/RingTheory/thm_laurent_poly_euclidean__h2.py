import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: R is not a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    if isinstance(witness, dict):
        F = witness.get('F')
        R = witness.get('R')
    elif hasattr(witness, 'F') and hasattr(witness, 'R'):
        F = witness.F
        R = witness.R
    elif isinstance(witness, (tuple, list)) and len(witness) == 2:
        F, R = witness
    else:
        return [False, False]

    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False

    try:
        # In SymPy, all implemented PIDs (fields, ZZ, K[x]) are Euclidean domains.
        # If R is not a PID, it is not a Euclidean domain.
        # If R does not have the is_PID attribute, we assume it is not a Euclidean domain.
        if hasattr(R, 'is_PID'):
            is_pid = R.is_PID
        else:
            is_pid = False
        neg_q = not bool(is_pid)
    except Exception:
        neg_q = False

    return [h1, neg_q]