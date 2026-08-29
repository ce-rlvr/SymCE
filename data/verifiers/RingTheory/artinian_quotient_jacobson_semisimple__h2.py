import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_right_artinian', False))
        else:
            attr = getattr(witness, 'is_right_artinian', False)
            h1 = bool(attr() if callable(attr) else attr)
    except Exception:
        h1 = False
        
    try:
        if isinstance(witness, dict):
            if 'is_quotient_semisimple' in witness:
                neg_q = not bool(witness['is_quotient_semisimple'])
        else:
            if hasattr(witness, 'is_quotient_semisimple'):
                attr = getattr(witness, 'is_quotient_semisimple')
                val = attr() if callable(attr) else attr
                neg_q = not bool(val)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: R/J(R) is not a semisimple ring"
]

N_HYP = 1
NEG_Q_INDEX = 1