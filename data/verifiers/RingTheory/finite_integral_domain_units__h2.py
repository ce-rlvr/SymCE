import math
import sympy

# Top-level setup: named objects that a witness expression might reference.
# In the context of finite rings, an integer n naturally represents the ring Z/nZ.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # We interpret an integer witness n as the ring Z/nZ.
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n > 1:
                h1 = True
                # In Z/nZ, an element 'a' is a unit iff gcd(a, n) == 1.
                # The conclusion is that EVERY non-zero element is a unit.
                # The negation is that there exists a non-zero element (1 <= a < n)
                # which is NOT a unit (i.e., gcd(a, n) > 1).
                neg_q = any(math.gcd(a, n) > 1 for a in range(1, n))
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with finitely many elements",
    "¬Q: There exists a non-zero element in R which is not a unit"
]

N_HYP = 1
NEG_Q_INDEX = 1