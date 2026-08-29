import sympy
from sympy.ntheory import divisor_sigma
import math

def conditions(witness) -> list[bool]:
    try:
        # The witness must be an integer
        n = int(witness)
        if n != witness:
            return [False]
            
        # Evaluate LHS: sigma(n) is an odd integer
        # divisor_sigma is defined for positive integers.
        # For n < 1, it does not have a sum of divisors that is an odd integer.
        if n < 1:
            lhs = False
        else:
            lhs = bool(divisor_sigma(n) % 2 == 1)
            
        # Evaluate RHS: n = k^2 or n = 2k^2 for some integer k
        if n < 0:
            rhs = False
        else:
            r1 = math.isqrt(n)
            if r1 * r1 == n:
                rhs = True
            elif n % 2 == 0:
                r2 = math.isqrt(n // 2)
                if 2 * r2 * r2 == n:
                    rhs = True
                else:
                    rhs = False
            else:
                rhs = False
                
        # The conclusion is LHS <-> RHS. We want the negation of the conclusion.
        neg_q = not (lhs == rhs)
        
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: It is not the case that (sigma(n) is odd iff n=k^2 or n=2k^2)"
]

N_HYP = 0
NEG_Q_INDEX = 0