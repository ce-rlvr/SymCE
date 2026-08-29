import sympy
from sympy import Poly
from sympy.abc import x, y, z

QQ = sympy.QQ
ZZ = sympy.ZZ

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness)
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(not f.is_zero)
    except Exception:
        h1 = False
        
    try:
        domain = f.domain
        if domain.is_Field:
            is_artinian = bool(not f.is_zero)
        else:
            try:
                if f.degree() == 0:
                    c = f.LC()
                    try:
                        is_artinian = bool(domain.is_unit(c))
                    except Exception:
                        is_artinian = (c in [1, -1])
                else:
                    is_artinian = False
            except Exception:
                is_artinian = False
                
        neg_q = not is_artinian
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a non-zero polynomial",
    "¬Q: The factor ring is not an Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1