import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: The global dimension of R is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        h1 = bool(getattr(witness, 'is_PID', False))
    except Exception:
        h1 = False

    try:
        # The global dimension of a field is 0.
        # The global dimension of a PID that is not a field is 1.
        if getattr(witness, 'is_Field', False):
            gdim_is_1 = False
        elif getattr(witness, 'is_PID', False):
            gdim_is_1 = True
        else:
            # For rings that are not PIDs, the global dimension is generally not 1
            # (with the exception of some Dedekind domains, but we only need to 
            # evaluate this accurately for valid witnesses where H_1 holds).
            gdim_is_1 = False
            
        neg_q = not gdim_is_1
    except Exception:
        neg_q = False

    return [h1, neg_q]