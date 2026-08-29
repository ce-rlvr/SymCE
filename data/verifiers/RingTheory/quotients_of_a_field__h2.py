import sympy
from sympy import QQ, ZZ, RR, CC
from sympy.polys.domains import GF
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        F, I = witness
    except Exception:
        return [False, False]
        
    # H_1: F is a field
    try:
        h1 = False
        if hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif hasattr(F, 'is_field') and F.is_field:
            h1 = True
    except Exception:
        h1 = False
        
    # ¬Q: The quotient ring F/I is neither isomorphic to F nor the zero ring.
    # This conclusion fails (i.e., ¬Q is True) if I is NOT an ideal of F.
    # Since F is a field, its only ideals are the zero ideal and F itself.
    try:
        is_ideal = False
        if I == F:
            is_ideal = True
        elif I == 0 or I == [0] or I == {0} or I == (0,):
            is_ideal = True
        elif hasattr(I, 'is_zero') and I.is_zero:
            is_ideal = True
        elif isinstance(I, set) and len(I) == 1 and 0 in I:
            is_ideal = True
        elif isinstance(I, list) and len(I) == 1 and I[0] == 0:
            is_ideal = True
            
        neg_q = not is_ideal
    except Exception:
        # If equality checks fail (e.g., due to incompatible types), I is not an ideal of F.
        neg_q = True
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "¬Q: The quotient ring F/I is neither isomorphic to F nor the zero ring (e.g. I is not an ideal)"
]

N_HYP = 1
NEG_Q_INDEX = 1