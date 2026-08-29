import sympy
from sympy import ZZ, QQ, Symbol
import sympy.polys.rings

# Top-level setup: named object bindings
x = Symbol('x')
Z = ZZ
Q = QQ
Qx = QQ[x]

def is_zero_ideal(I):
    if isinstance(I, (list, tuple, set)):
        return all(g == 0 for g in I)
    return I == 0

def generators_in_ring(R, I):
    if isinstance(I, (list, tuple, set)):
        gens = I
    else:
        gens = [I]
        
    for g in gens:
        if R in (ZZ, "Z", Z):
            if not isinstance(g, (int, sympy.Integer)) and g != 0:
                return False
        elif R in (QQ, "Q", Q):
            if not isinstance(g, (int, float, sympy.Rational, sympy.Integer)) and g != 0:
                return False
        elif isinstance(R, sympy.polys.rings.PolyRing) or R in ("Q[x]", "R[x]", Qx):
            if not isinstance(g, (int, sympy.Integer, sympy.Rational, sympy.Expr)) and g != 0:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        R, I = witness
    except Exception:
        return [False, False]
    
    # H_1: I is a two-sided ideal of R
    h1 = False
    try:
        h1 = generators_in_ring(R, I)
    except Exception:
        pass

    # ¬Q: R/I is not a left Artinian ring
    neg_q = False
    try:
        zero_ideal = is_zero_ideal(I)
        is_artinian = True # Default to True so neg_q becomes False if unknown
        
        if zero_ideal:
            if R in (ZZ, "Z", Z):
                is_artinian = False
            elif isinstance(R, sympy.polys.rings.PolyRing) or R in ("Q[x]", "R[x]", Qx):
                is_artinian = False
            elif R in (QQ, "Q", Q):
                is_artinian = True
        else:
            if R in (ZZ, "Z", Z):
                is_artinian = True
            elif isinstance(R, sympy.polys.rings.PolyRing) or R in ("Q[x]", "R[x]", Qx):
                is_artinian = True
            elif R in (QQ, "Q", Q):
                is_artinian = True
                
        neg_q = not is_artinian
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I is a two-sided ideal of R",
    "¬Q: R/I is not a left Artinian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1