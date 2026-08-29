import sympy
from sympy import ZZ, QQ, RR, CC

# Top-level setup for witness expressions
Z = ZZ
Q = QQ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be a principal ideal domain. Let M be a torsion-free module. Then M is a free R-module."
    """
    try:
        # The witness can be a tuple (R, M) or just M (in which case we assume R = Z)
        if isinstance(witness, (list, tuple)) and len(witness) == 2:
            R, M = witness
        else:
            R = ZZ
            M = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a principal ideal domain
    try:
        h1 = False
        if getattr(R, 'is_PID', False):
            h1 = True
        elif R in (ZZ, QQ, RR, CC):
            h1 = True
    except Exception:
        h1 = False
        
    # H_2: M is a torsion-free module
    try:
        h2 = False
        if R == ZZ and M in (ZZ, QQ, RR, CC):
            h2 = True
        elif getattr(R, 'is_Field', False) and getattr(M, 'is_Field', False):
            h2 = True
        elif R in (QQ, RR, CC) and M in (QQ, RR, CC):
            h2 = True
        elif R == M:
            h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: M is NOT a free R-module
    try:
        neg_q = False
        if R == ZZ and M in (QQ, RR, CC):
            # Q, R, C are torsion-free over Z but not free Z-modules
            neg_q = True
        elif R == M:
            # R is a free R-module of rank 1
            neg_q = False
        elif getattr(R, 'is_Field', False):
            # Every module (vector space) over a field is free
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