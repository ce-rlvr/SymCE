import math
import sympy

# Top-level setup
# The witness should be a tuple of three integers: (k, m, n)
# This represents the ring R = k*Z, its ideal M = m*Z, and the power n.
# (This provides a counterexample in a commutative ring without identity).

def conditions(witness):
    try:
        if not (isinstance(witness, tuple) and len(witness) == 3):
            return [False, False, False]
        k, m, n = witness
        if not all(isinstance(x, int) for x in (k, m, n)):
            return [False, False, False]
            
        if k <= 0 or m <= 0:
            return [False, False, False]
            
        # H_1: M is a maximal ideal of R
        # M = m*Z is an ideal of R = k*Z iff k divides m
        if m % k != 0:
            h1 = False
        elif m == k:
            h1 = False # M must be a proper ideal
        else:
            # M is maximal iff m/k is prime
            h1 = sympy.isprime(m // k)
            
        # H_2: n is a positive integer
        h2 = (n >= 1)
        
        # Conclusion: M^n is an M-primary ideal
        if n > 1000:
            return [False, False, False]
        a = m**n
        if a > 10**18:
            return [False, False, False]
            
        # Calculate the radical of M^n = a*Z in R = k*Z
        rad_a = 1
        for p in sympy.primefactors(a):
            rad_a *= p
        r = (k * rad_a) // math.gcd(k, rad_a)
        
        # Check if a*Z is a primary ideal in k*Z
        A = a // math.gcd(k**2, a)
        B = a // math.gcd(k, a)
        C = r // math.gcd(k, r)
        
        is_primary = True
        if a == k:
            is_primary = False
        else:
            divs = set()
            for i in range(1, int(A**0.5) + 1):
                if A % i == 0:
                    divs.add(i)
                    divs.add(A // i)
            
            for u in divs:
                v = A // u
                if (u % B != 0) and (v % C != 0):
                    is_primary = False
                    break
                    
        # M^n is M-primary iff it is primary and its radical is M
        is_M_primary = is_primary and (r == m)
        
        neg_q = not is_M_primary
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: M is a maximal ideal of R",
    "H_2: n is a positive integer",
    "not Q: The ideal power M^n is not an M-primary ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2