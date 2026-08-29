import sympy
from sympy import I, sqrt
from sympy.polys.domains import ZZ, QQ

K = QQ.algebraic_field(I*sqrt(19))

def conditions(witness):
    try:
        # H_1: Let K be the imaginary quadratic field Q(sqrt(-19)).
        # This hypothesis establishes the context but does not constrain the witness R.
        h1 = True
    except Exception:
        h1 = False
        
    try:
        # Check if the witness is a Principal Ideal Domain (PID)
        is_pid = False
        if witness in (sympy.ZZ, sympy.QQ, ZZ, QQ):
            is_pid = True
        elif getattr(witness, 'is_PID', False):
            is_pid = True
        elif getattr(witness, 'is_Field', False):
            is_pid = True
            
        # Check if the witness is a Euclidean domain
        is_euclidean = False
        if witness in (sympy.ZZ, sympy.QQ, ZZ, QQ):
            is_euclidean = True
        elif getattr(witness, 'is_Field', False):
            is_euclidean = True
        elif getattr(witness, 'is_Poly', False) and getattr(getattr(witness, 'domain', None), 'is_Field', False):
            if hasattr(witness, 'gens') and len(witness.gens) == 1:
                is_euclidean = True
                
        # Q: R is a principal ideal domain but is not a Euclidean domain
        q = is_pid and (not is_euclidean)
        
        # neg_Q is True when the conclusion fails
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is the imaginary quadratic field Q(sqrt(-19))",
    "¬Q: R is not a PID or is a Euclidean domain"
]

N_HYP = 1
NEG_Q_INDEX = 1