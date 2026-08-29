import sympy
from sympy.ntheory import factorint, isprime

# Top-level setup: named object bindings
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9

def conditions(witness) -> list[bool]:
    """
    Given a witness representing the ring Z/nZ (as an integer n),
    checks if it satisfies the hypotheses and falsifies the conclusion.
    """
    try:
        # Parse string representations like "Z/4Z" or "Z_4"
        if isinstance(witness, str):
            s = witness.replace(' ', '')
            if s.startswith('Z/') and s.endswith('Z'):
                witness = int(s[2:-1])
            elif s.startswith('Z_'):
                witness = int(s[2:])
                
        n = int(witness)
        if n <= 1:
            return [False, False, False]
            
        # H_1: R is a commutative Noetherian ring
        # Z/nZ is always commutative and Noetherian for any integer n > 1
        h1 = True
        
        # H_2: R is a local ring with unique maximal ideal m
        # Z/nZ is a local ring if and only if n is a prime power (p^k)
        factors = factorint(n)
        h2 = (len(factors) == 1)
        
        # ¬Q: R is NOT an integral domain
        # Z/nZ is an integral domain if and only if n is prime.
        # Thus, it is NOT an integral domain if n is composite.
        neg_q = not isprime(n)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: R is a local ring",
    "¬Q: R is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2