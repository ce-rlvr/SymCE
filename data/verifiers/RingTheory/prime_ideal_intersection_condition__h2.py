import sympy
import math

# Top-level setup
# We evaluate the conjecture in the ring of integers Z, which is a commutative ring.
# The witness is expected to be a tuple (a, b) representing the ideals aZ and bZ in Z.
# It may also be provided as (R, a, b) where R is ignored.

def conditions(witness) -> list[bool]:
    try:
        # Parse the witness
        if isinstance(witness, tuple):
            if len(witness) == 3:
                _, a, b = witness
            elif len(witness) == 2:
                a, b = witness
            else:
                return [False, False]
        else:
            return [False, False]
            
        a = int(a)
        b = int(b)
        
        # H_1: R is a commutative ring
        # Since we are working in Z, this is always True for valid integer inputs.
        h1_ok = True
        
        # Helper: (x) is a subset of (y) in Z iff y divides x
        def subset(x, y):
            if y == 0:
                return x == 0
            return x % y == 0
            
        # Helper: generator of the intersection of (x) and (y), which is lcm(x, y)
        def intersect(x, y):
            if x == 0 or y == 0:
                return 0
            return abs(x * y) // math.gcd(x, y)
            
        # Helper: (m) is a prime ideal in Z iff m = 0 or |m| is a prime number
        # Note: (1) is not a prime ideal because prime ideals must be proper.
        def is_prime_ideal(m):
            if m == 0:
                return True
            return sympy.isprime(abs(m))
            
        p1_sub_p2 = subset(a, b)
        p2_sub_p1 = subset(b, a)
        
        intersection_gen = intersect(a, b)
        is_prime = is_prime_ideal(intersection_gen)
        
        # Conclusion Q: P_1 \cap P_2 is a prime ideal iff P_1 \subseteq P_2 or P_2 \subseteq P_1
        q = (is_prime == (p1_sub_p2 or p2_sub_p1))
        
        # We want the conclusion to FAIL
        neg_q = not q
        
        return [h1_ok, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The equivalence (P_1 \\cap P_2 is prime iff P_1 \\subseteq P_2 or P_2 \\subseteq P_1) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1