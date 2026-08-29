import sympy
from sympy import abc

# Top-level setup: named object bindings that the witness expression may reference.
ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC
x = abc.x

def conditions(witness) -> list[bool]:
    """
    Given a witness (R, M), checks if it is a valid counterexample to the conjecture:
    "If R is a principal ideal domain and M is a torsion-free module, then M is a free R-module."
    """
    try:
        R, M = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a principal ideal domain
    try:
        h1 = bool(R.is_PID)
    except Exception:
        h1 = False
        
    # H_2: M is a torsion-free module
    try:
        # M is torsion-free over R if M is the fraction field of R,
        # or if M is a field of characteristic 0 and R is ZZ,
        # or trivially if M == R.
        if hasattr(R, 'get_field') and M == R.get_field():
            h2 = True
        elif R == ZZ and M in (QQ, RR, CC):
            h2 = True
        elif M == R:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: M is not a free R-module
    try:
        if M == R:
            # R is a free R-module of rank 1
            neg_q = False
        elif hasattr(R, 'get_field') and M == R.get_field():
            # The fraction field of a domain R is a free R-module iff R is already a field.
            neg_q = not bool(R.is_Field)
        elif R == ZZ and M in (QQ, RR, CC):
            # Q, R, C are not free Z-modules
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a torsion-free module",
    "¬Q: M is not a free R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2