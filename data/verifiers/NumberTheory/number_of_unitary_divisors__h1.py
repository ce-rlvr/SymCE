import sympy
import math
from sympy.ntheory import divisors, primefactors

# Top-level setup
# (No specific named objects required for the Number Theory domain; use integers directly)

def conditions(witness) -> list[bool]:
    try:
        # Check if witness is an integer (and not a boolean)
        if not isinstance(witness, (int, sympy.Integer)) or isinstance(witness, bool):
            return [False]
        
        n = int(witness)
        
        # Calculate tau^*(n), the number of positive unitary divisors
        if n == 0:
            # For n=0, the only positive divisor d such that gcd(d, 0/d) == 1 is d=1.
            t_star = 1
        else:
            t_star = 0
            for d in divisors(abs(n)):
                if math.gcd(d, abs(n) // d) == 1:
                    t_star += 1
                    
        # Calculate omega(n), the number of distinct prime factors
        # For n=0, primefactors(0) raises a ValueError, which will be caught.
        w = len(primefactors(n))
        
        # The conclusion is tau^*(n) == 2^omega(n)
        conclusion = (t_star == 2**w)
        neg_q = not conclusion
        
    except Exception:
        # If an exception occurs (e.g., evaluating omega(0)), the formula is undefined,
        # meaning the conclusion fails at this witness.
        neg_q = True
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: tau^*(n) != 2^omega(n) (or is undefined)"
]

N_HYP = 0
NEG_Q_INDEX = 0