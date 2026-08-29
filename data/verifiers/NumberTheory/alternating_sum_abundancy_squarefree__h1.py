import sympy
from sympy import Rational
from sympy.ntheory import mobius, divisor_sigma, primefactors, divisors

# Top-level setup
# (No specific named objects needed for this Number Theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        # Ensure witness is exactly an integer
        if int(witness) != witness:
            return [False]
        n = int(witness)
        
        # The sum over divisors of 0 is undefined, so the identity fails.
        if n == 0:
            return [True]
            
        lhs = sum(Rational(mobius(d) * divisor_sigma(d), d) for d in divisors(n))
        
        p_factors = primefactors(n)
        omega = len(p_factors)
        rad = 1
        for p in p_factors:
            rad *= p
            
        rhs = Rational((-1)**omega, rad)
        
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = ["¬Q: The identity fails at n"]
N_HYP = 0
NEG_Q_INDEX = 0