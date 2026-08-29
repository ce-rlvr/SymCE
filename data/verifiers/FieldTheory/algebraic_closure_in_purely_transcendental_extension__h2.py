import sympy
from sympy import QQ, I, sqrt
from sympy.polys.domains import AlgebraicField, RR, CC
from sympy.abc import x

def conditions(witness):
    try:
        F, E, K = witness
    except Exception:
        return [False, False, False]
    
    # H1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H2: K is the algebraic closure of F within E
    try:
        h2 = False
        if getattr(E, 'is_Field', False):
            if E == F:
                h2 = (K == F)
            elif isinstance(E, AlgebraicField) and getattr(E, 'domain', None) == F:
                # If E is a finite algebraic extension of F, 
                # the algebraic closure of F in E is E itself.
                h2 = (K == E)
            elif F == RR and E == CC:
                # The algebraic closure of RR in CC is CC.
                h2 = (K == CC)
    except Exception:
        h2 = False
        
    # neg_Q: K is not equal to F
    try:
        neg_q = (K != F)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is the algebraic closure of F within E",
    "¬Q: K is not equal to F"
]

N_HYP = 2
NEG_Q_INDEX = 2