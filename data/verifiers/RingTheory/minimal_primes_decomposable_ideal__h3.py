import sympy
from sympy.ntheory import primefactors

# Top-level setup
# The witness is expected to be a tuple of two integers (n, m)
# representing the ideal I = (n) and the ideal P = (m) in the ring of integers Z.
# Z is a commutative ring with identity, and all its ideals admit a primary decomposition.

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = int(witness.get('n', 0))
            m = int(witness.get('m', 0))
        else:
            n, m = witness
            n = int(n)
            m = int(m)
            
        # H_1: R is a commutative ring with identity
        # We use R = Z, which is always a commutative ring with identity.
        h1 = True
        
        # H_2: I is a proper ideal of R that admits a primary decomposition
        # In Z, all ideals admit a primary decomposition.
        # Proper ideal means I != Z, so abs(n) != 1.
        h2 = (abs(n) != 1)
        
        # Q: P contains at least one minimal associated prime ideal of I.
        # Minimal associated primes of (n) in Z:
        if n == 0:
            min_primes = [0]
        else:
            min_primes = primefactors(n)
            
        # P = (m) contains (p) iff m divides p.
        q = False
        for p in min_primes:
            if p == 0:
                # (m) contains (0) iff m divides 0, which is true for all m.
                q = True
                break
            else:
                if m != 0 and p % m == 0:
                    q = True
                    break
                    
        neg_q = not q
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is a proper ideal of R that admits a primary decomposition",
    "¬Q: P does not contain any minimal associated prime ideal of I"
]

N_HYP = 2
NEG_Q_INDEX = 2