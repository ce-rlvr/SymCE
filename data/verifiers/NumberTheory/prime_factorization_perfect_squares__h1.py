import sympy
from sympy.ntheory import factorint
import math

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
        if n != witness:
            return [False]
    except Exception:
        return [False]
        
    try:
        # Check if n is a perfect square
        if n < 0:
            is_sq = False
        else:
            root = math.isqrt(n)
            is_sq = (root * root == n)
            
        # Check if every prime factor occurs with an even exponent
        if n == 0:
            all_even = True
        else:
            factors = factorint(n)
            all_even = True
            for p, exp in factors.items():
                if p > 1 and sympy.isprime(p):
                    if exp % 2 != 0:
                        all_even = False
                        break
                        
        # The conclusion is (is_sq == all_even)
        # We want the negated conclusion, so we check if they differ
        neg_q = (is_sq != all_even)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: n is a perfect square iff every prime factor has an even exponent fails"
]

N_HYP = 0
NEG_Q_INDEX = 0