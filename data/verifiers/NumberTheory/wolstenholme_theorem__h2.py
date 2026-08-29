import math
import sympy
from sympy.ntheory import isprime

def conditions(witness):
    """
    Checks if the given witness is a counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, neg_Q_ok].
    """
    try:
        p = int(witness)
    except Exception:
        return [False, False]
    
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # ¬Q: The binomial coefficient \binom{2p-1}{p-1} is NOT congruent to 1 modulo p^3
    try:
        if p >= 1:
            val = math.comb(2 * p - 1, p - 1)
            neg_q = bool((val % (p**3)) != 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: binomial(2p-1, p-1) is not congruent to 1 modulo p^3"
]

N_HYP = 1
NEG_Q_INDEX = 1