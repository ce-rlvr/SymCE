import math
import sympy
from sympy import Integer

# Top-level setup
# (No named bindings needed for this number theory conjecture; witnesses are integers)

def conditions(witness) -> list[bool]:
    try:
        # Witness must be an integer
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
            
        p = int(witness)
        
        # Condition A: x^2 + y^2 = p has a solution in integers x, y
        if p < 0:
            A = False
        else:
            A = False
            limit = math.isqrt(p)
            for x in range(limit + 1):
                rem = p - x*x
                y = math.isqrt(rem)
                if y*y == rem:
                    A = True
                    break
                    
        # Condition B: p is congruent to 1 modulo 4
        B = (p % 4 == 1)
        
        # The conclusion is A <=> B.
        # The negated conclusion is A XOR B (i.e., A != B).
        neg_q = bool(A != B)
        
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: (x^2 + y^2 = p has integer solutions) XOR (p ≡ 1 mod 4)"
]

N_HYP = 0
NEG_Q_INDEX = 0