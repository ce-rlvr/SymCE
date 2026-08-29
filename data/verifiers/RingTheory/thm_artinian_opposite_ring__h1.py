import sympy
import sympy.polys
from sympy.abc import x, y, z

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        neg_q = False
        
        if witness == ZZ or witness == sympy.S.Integers:
            neg_q = True
        elif isinstance(witness, sympy.polys.domains.polyring.PolyRing):
            neg_q = True
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            neg_q = False
        elif witness == QQ or witness == sympy.S.Rationals:
            neg_q = False
        else:
            s = str(witness)
            if ('ZZ' in s or 'QQ' in s or 'Integers' in s) and '[' in s and ']' in s:
                neg_q = True
                
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The opposite ring R^{op} is not a left Artinian ring"
]

N_HYP = 0
NEG_Q_INDEX = 0