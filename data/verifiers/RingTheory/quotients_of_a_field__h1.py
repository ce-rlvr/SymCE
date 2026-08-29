import sympy
from sympy import ZZ, QQ
from sympy.abc import x
import math

CONDITION_LABELS = [
    "H_1: I is an ideal of F",
    "¬Q: F/I is neither isomorphic to F nor the zero ring"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # The witness can be a tuple (F, I) or just I (assuming F = ZZ)
        if isinstance(witness, tuple) and len(witness) == 2:
            F, I = witness
        else:
            F = ZZ
            I = witness
    except Exception:
        return [False, False]
        
    # H_1: I is an ideal of F
    try:
        is_ring = hasattr(F, 'is_Ring') and F.is_Ring
        if not is_ring:
            h1 = False
        else:
            if isinstance(I, (list, tuple, set)):
                h1 = all(i in F for i in I)
            else:
                h1 = I in F
    except Exception:
        h1 = False
        
    # ¬Q: F/I is neither isomorphic to F nor the zero ring
    try:
        if F == ZZ:
            if isinstance(I, (list, tuple, set)):
                g = math.gcd(*[int(i) for i in I])
            else:
                g = abs(int(I))
            is_iso_to_F = (g == 0)
            is_zero_ring = (g == 1)
            neg_q = not (is_iso_to_F or is_zero_ring)
        else:
            if isinstance(I, (list, tuple, set)):
                is_zero = all(i == F.zero for i in I)
                is_unit_ideal = any(F.is_unit(i) for i in I)
            else:
                is_zero = (I == F.zero)
                is_unit_ideal = F.is_unit(I)
            
            is_iso_to_F = is_zero
            is_zero_ring = is_unit_ideal
            neg_q = not (is_iso_to_F or is_zero_ring)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]