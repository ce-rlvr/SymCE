import sympy
from sympy.polys.domains import ZZ, QQ
from sympy.abc import x

# Top-level setup
Z = ZZ
Q = QQ

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        h1 = False
        if R == sympy.S.Integers or R == ZZ:
            h1 = True
        elif hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
    except Exception:
        h1 = False
        
    try:
        neg_q = False
        if h1:
            field = False
            if R == sympy.S.Integers or R == ZZ:
                field = False
            elif hasattr(R, 'is_Field'):
                field = bool(R.is_Field)
                
            zero_ideal = False
            if I == 0:
                zero_ideal = True
            elif hasattr(R, 'zero') and I == R.zero:
                zero_ideal = True
            elif isinstance(I, (list, tuple, set)):
                if len(I) == 0:
                    zero_ideal = True
                elif all(i == 0 for i in I):
                    zero_ideal = True
            elif hasattr(I, 'is_zero'):
                if callable(I.is_zero):
                    zero_ideal = I.is_zero()
                else:
                    zero_ideal = bool(I.is_zero)
                    
            if zero_ideal and not field:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: The quotient ring R/I is not an Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1