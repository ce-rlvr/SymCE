import sympy
from sympy.polys.domains import CC
from sympy import Symbol

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        F, K, alpha = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(F == CC)
    except Exception:
        h1 = False
        
    try:
        h2 = False
        if getattr(K, 'is_Field', False):
            if K == F or getattr(K, 'domain', None) == F:
                try:
                    K.from_sympy(alpha)
                    h2 = True
                except Exception:
                    h2 = False
    except Exception:
        h2 = False
        
    try:
        try:
            F.from_sympy(alpha)
            in_F = True
        except Exception:
            in_F = False
            
        neg_q = not in_F
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is an algebraically closed field",
    "H_2: K is an extension field of F",
    "¬Q: The minimal polynomial of alpha over F is not x - alpha"
]

N_HYP = 2
NEG_Q_INDEX = 2