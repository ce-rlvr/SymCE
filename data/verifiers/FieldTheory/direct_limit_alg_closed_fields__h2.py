import sympy
from sympy import Symbol

# Top-level setup
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC
x = Symbol('x')

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("I_is_directed", False))
            h2 = bool(witness.get("K_is_direct_limit", False))
            neg_q = not bool(witness.get("K_is_algebraically_closed", True))
        else:
            if hasattr(witness, 'is_Field') and witness.is_Field:
                h1 = True
                h2 = True
                if witness in (sympy.QQ, sympy.RR):
                    neg_q = True
                elif witness == sympy.CC:
                    neg_q = False
                else:
                    neg_q = True
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is a directed set",
    "H_2: K is the direct limit of the system (K_i)_{i in I}",
    "¬Q: The field K is not algebraically closed"
]

N_HYP = 2
NEG_Q_INDEX = 2