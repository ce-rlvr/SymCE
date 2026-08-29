import math
import sympy

# Top-level setup
# (No named bindings needed for number theory)

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        if p != witness:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(p > 2)
    except Exception:
        h1 = False
        
    try:
        if p < 0:
            sum_of_squares = False
        else:
            sum_of_squares = False
            limit = int(math.isqrt(p))
            for x in range(limit + 1):
                y2 = p - x*x
                y = int(math.isqrt(y2))
                if y*y == y2:
                    sum_of_squares = True
                    break
        
        mod_4_is_1 = (p % 4 == 1)
        neg_q = bool(sum_of_squares != mod_4_is_1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p > 2",
    "¬Q: (p is a sum of two squares) is not equivalent to (p ≡ 1 mod 4)"
]

N_HYP = 1
NEG_Q_INDEX = 1