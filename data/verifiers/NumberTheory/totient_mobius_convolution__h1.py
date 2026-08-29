import sympy
from sympy.ntheory import divisors, primefactors, mobius, totient
import math

# No specific named bindings needed for Number Theory

CONDITION_LABELS = [
    "¬Q: The equation sum_{d|n} mu(d)phi(d) = prod_{p|n} (2-p) fails to hold"
]
N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        n = sympy.sympify(witness)
        
        # Calculate LHS: sum_{d|n} mu(d) * phi(d)
        # The sum is over all positive divisors d of n
        divs = divisors(n)
        lhs = sum(mobius(d) * totient(d) for d in divs if d > 0)
        
        # Calculate RHS: prod_{p|n} (2 - p)
        # The product is over all distinct prime divisors p of n
        primes = primefactors(n)
        rhs = math.prod((2 - p) for p in primes)
        
        conclusion = (lhs == rhs)
    except Exception:
        # If divisors or primefactors cannot be computed (e.g., for n=0 or non-integers),
        # the conclusion is considered to fail.
        conclusion = False
        
    neg_q = not conclusion
    return [neg_q]