import sympy
from sympy import ZZ, QQ

def conditions(witness) -> list[bool]:
    try:
        if witness == QQ:
            is_perfect = True
        elif witness == ZZ:
            is_perfect = False
        elif getattr(witness, 'is_Field', False):
            is_perfect = True
        elif hasattr(witness, 'is_PolynomialRing') and witness.is_PolynomialRing:
            is_perfect = False
        else:
            is_perfect = getattr(witness, 'is_Field', False)
            
        neg_q = not is_perfect
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R is not a right perfect ring"
]

N_HYP = 0
NEG_Q_INDEX = 0