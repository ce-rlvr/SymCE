import math
import sympy
from sympy import ZZ, QQ

# Top-level setup: named object bindings that the witness expression may reference.
Z2 = 2
Z3 = 3
Z4 = 4
Z6 = 6

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # Check if witness is the ring of integers (ZZ)
    try:
        if witness == ZZ:
            h1 = True
            # In ZZ, elements like 2 are neither units (only 1, -1 are) nor nilpotent (only 0 is).
            neg_q = True
            return [h1, neg_q]
    except Exception:
        pass

    # Check if witness is the field of rationals (QQ)
    try:
        if witness == QQ:
            h1 = True
            # In QQ, every non-zero element is a unit, and 0 is nilpotent.
            neg_q = False
            return [h1, neg_q]
    except Exception:
        pass

    # Check if witness is an integer n > 1, representing the commutative ring Z/nZ
    try:
        n = int(witness)
        if n > 1:
            h1 = True
            # To ensure the function completes quickly, we check up to the first 10000 elements.
            # For any valid counterexample Z/nZ, the smallest witness element is a prime factor,
            # which will be found very quickly.
            limit = min(n, 10000)
            for x in range(limit):
                is_unit = (math.gcd(x, n) == 1)
                is_nilp = (pow(x, n, n) == 0)
                
                if not is_unit and not is_nilp:
                    neg_q = True
                    break
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: There exists an element in R that is neither a unit nor a nilpotent element"
]

N_HYP = 1
NEG_Q_INDEX = 1