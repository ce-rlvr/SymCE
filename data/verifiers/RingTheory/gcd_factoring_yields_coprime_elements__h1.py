import math
from sympy.ntheory import factorint
from sympy.abc import x, y, z

# Top-level setup
# Witnesses for this ring theory conjecture are expected to be tuples representing 
# elements in the ring Z/nZ. The format can be either (n, a, b, d) or (n, a, b, d, x, y)
# where x and y are the specific quotients a/d and b/d.

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 4:
            n, a, b, d = witness
            x_provided = False
        elif len(witness) == 6:
            n, a, b, d, x_val, y_val = witness
            x_provided = True
        else:
            return [False, False, False]
            
        n = int(n)
        if n < 2:
            return [False, False, False]
            
        a = int(a) % n
        b = int(b) % n
        d = int(d) % n
        
        # H1: a and b are non-zero elements of R
        h1 = (a != 0) and (b != 0)
        
        # H2: d is a greatest common divisor of a and b
        # In Z/nZ, d is a gcd of a and b iff gcd(d, n) == gcd(a, b, n)
        g_ab = math.gcd(math.gcd(a, b), n)
        h2 = (math.gcd(d, n) == g_ab)
        
        # Neg_Q: The greatest common divisor of a/d and b/d is not a unit in R
        # This means there exist valid quotients x and y such that their gcd is not a unit.
        # In Z/nZ, the gcds of x and y are units iff gcd(x, y, n) == 1.
        neg_q = False
        
        if x_provided:
            x_val = int(x_val) % n
            y_val = int(y_val) % n
            if (d * x_val) % n == a and (d * y_val) % n == b:
                if math.gcd(math.gcd(x_val, y_val), n) > 1:
                    neg_q = True
        else:
            g = math.gcd(d, n)
            if a % g == 0 and b % g == 0:
                m = n // g
                d_prime = d // g
                a_prime = a // g
                b_prime = b // g
                
                if m == 1:
                    inv = 0
                else:
                    inv = pow(d_prime, -1, m)
                    
                x0 = (a_prime * inv) % m
                y0 = (b_prime * inv) % m
                
                factors = factorint(n)
                for p in factors:
                    if m % p == 0:
                        if x0 % p == 0 and y0 % p == 0:
                            neg_q = True
                            break
                    else:
                        neg_q = True
                        break
                        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of R",
    "H_2: d is a greatest common divisor of a and b",
    "¬Q: The greatest common divisor of a/d and b/d is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2