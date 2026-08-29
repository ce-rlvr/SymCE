import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        if p != witness:
            return [False]
        
        is_sum = False
        if p >= 0:
            limit = math.isqrt(p)
            for x in range(limit + 1):
                y2 = p - x * x
                y = math.isqrt(y2)
                if y * y == y2:
                    is_sum = True
                    break
                    
        is_mod_1 = (p % 4 == 1)
        
        neg_q = bool(is_sum != is_mod_1)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: p is a sum of two squares XOR p ≡ 1 (mod 4)"
]

N_HYP = 0
NEG_Q_INDEX = 0