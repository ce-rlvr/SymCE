import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y

# Top-level setup
# The witness should be a tuple of three integers: (k, m, n).
# This represents the commutative ring R = k*Z, its ideal M = m*Z,
# and the positive integer n.

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        
        k, m, n = witness
        k = int(k)
        m = int(m)
        n = int(n)
        
        # H1: M is a maximal ideal of R
        # R = kZ, M = mZ
        # M is an ideal if m is a multiple of k
        is_ideal = (k > 0) and (m > 0) and (m % k == 0)
        
        if is_ideal:
            p = m // k
            # M is maximal if the index p is prime
            is_maximal = sympy.isprime(p)
        else:
            is_maximal = False
            
        h1 = is_ideal and is_maximal
        
        # H2: n is a positive integer
        h2 = (n > 0)
        
        # Conclusion: M^n / M^{n+1} is a vector space over the field R/M
        # This requires R/M to be a field.
        # R/M has size p = m/k.
        # It is a field iff there is an identity element, which means k is not a multiple of p.
        if h1:
            p = m // k
            is_field = (k % p != 0)
        else:
            is_field = False
            
        neg_q = not is_field
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: M is a maximal ideal of R",
    "H_2: n is a positive integer",
    "¬Q: R/M is not a field, so M^n / M^{n+1} cannot be a vector space over it"
]

N_HYP = 2
NEG_Q_INDEX = 2