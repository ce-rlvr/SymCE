import sympy
import math

# Top-level setup for rings
class RingZn:
    def __init__(self, n):
        self.n = n
    def __repr__(self):
        return f"Z_{self.n}"

def Z_n(n):
    return RingZn(n)

Z = sympy.ZZ
Q = sympy.QQ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Expected witness format: (ring, ideal_generator)
    Examples:
      (Z, 3)       -> R = Z, P = (3)
      (Z_n(4), 2)  -> R = Z/4Z, P = (2)
    """
    H1 = False
    H2 = False
    neg_Q = False
    
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
            
        ring, p = witness
        
        # Unpack single-element lists/tuples if the user provided generators like [3]
        if isinstance(p, (list, tuple, set)) and len(p) == 1:
            p = list(p)[0]
            
        # H1: R is a commutative ring with identity
        if ring == sympy.ZZ or ring == sympy.QQ:
            H1 = True
        elif isinstance(ring, RingZn):
            if isinstance(ring.n, int) and ring.n > 1:
                H1 = True
                
        # H2: P is a prime ideal of R
        if ring == sympy.ZZ:
            if isinstance(p, int) or (hasattr(p, 'is_integer') and p.is_integer):
                p_val = int(p)
                if p_val == 0 or sympy.isprime(abs(p_val)):
                    H2 = True
        elif ring == sympy.QQ:
            if isinstance(p, int) or (hasattr(p, 'is_integer') and p.is_integer):
                if int(p) == 0:
                    H2 = True
        elif isinstance(ring, RingZn):
            if (isinstance(p, int) or (hasattr(p, 'is_integer') and p.is_integer)) and isinstance(ring.n, int) and ring.n > 1:
                p_val = int(p)
                d = math.gcd(ring.n, p_val)
                if sympy.isprime(d):
                    H2 = True
                    
        # neg_Q: R_P is NOT isomorphic to Z/2Z
        if ring == sympy.ZZ or ring == sympy.QQ:
            neg_Q = True
        elif isinstance(ring, RingZn):
            if (isinstance(p, int) or (hasattr(p, 'is_integer') and p.is_integer)) and isinstance(ring.n, int) and ring.n > 1:
                p_val = int(p)
                d = math.gcd(ring.n, p_val)
                if sympy.isprime(d):
                    # The localization of Z/nZ at the prime ideal (d) is isomorphic to Z/(d^k)Z,
                    # where d^k is the exact power of d dividing n.
                    temp = ring.n
                    power = 1
                    while temp % d == 0:
                        temp //= d
                        power *= d
                    if power != 2:
                        neg_Q = True
                else:
                    # If it's not a prime ideal, the conclusion fails vacuously.
                    neg_Q = True
                    
    except Exception:
        pass
        
    return [H1, H2, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: P is a prime ideal of R",
    "¬Q: The localization R_P is not isomorphic to Z/2Z"
]

N_HYP = 2
NEG_Q_INDEX = 2