import sympy
from sympy import Poly
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, Poly):
            f = Poly(witness)
        else:
            f = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(f.domain.is_UFD)
    except Exception:
        h1 = False
        
    try:
        cont, _ = f.primitive()
        try:
            f.domain.exquo(f.domain.one, cont)
            is_prim = True
        except Exception:
            is_prim = False
            
        is_irred = bool(f.is_irreducible)
        neg_q = (is_irred != is_prim)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "¬Q: f is irreducible iff f is primitive"
]

N_HYP = 1
NEG_Q_INDEX = 1