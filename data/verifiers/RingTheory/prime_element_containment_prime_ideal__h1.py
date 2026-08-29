import math
from sympy import isprime

class QuadraticIdeal:
    """
    Represents an ideal in the ring Z[sqrt(d)] for d < 0.
    Elements are represented as tuples (a, b) for a + b*sqrt(d).
    """
    def __init__(self, d: int, generators: list[tuple[int, int]]):
        self.d = d
        self.generators = generators

    def norm(self) -> int:
        """
        Computes the norm of the ideal, which is the index [Z[sqrt(d)] : I].
        This is done by finding the GCD of all 2x2 minors of the Z-basis matrix.
        """
        rows = []
        for (a, b) in self.generators:
            rows.append((a, b))
            rows.append((self.d * b, a))
        
        minors = []
        n = len(rows)
        for i in range(n):
            for j in range(i+1, n):
                a1, b1 = rows[i]
                a2, b2 = rows[j]
                minor = abs(a1 * b2 - a2 * b1)
                minors.append(minor)
        
        g = 0
        for m in minors:
            g = math.gcd(g, m)
        return g

    def is_non_zero(self) -> bool:
        return any(a != 0 or b != 0 for (a, b) in self.generators)

    def is_prime_ideal(self) -> bool:
        """
        Checks if the ideal is a prime ideal in Z[sqrt(d)].
        In such domains, an ideal is prime if its norm is a prime number p,
        or if its norm is p^2 where p is an inert prime.
        """
        n = self.norm()
        if n <= 1:
            return False
        if isprime(n):
            return True
        
        root = math.isqrt(n)
        if root**2 == n and isprime(root):
            p = root
            # Check if p is inert in Z[sqrt(d)] (i.e., x^2 - d has no roots mod p)
            for x in range(p):
                if (x**2 - self.d) % p == 0:
                    return False
            return True
            
        return False

    def contains_prime_element(self) -> bool:
        """
        Checks if the ideal contains a prime element.
        In a one-dimensional domain, a proper ideal contains a prime element 
        if and only if it is a principal prime ideal.
        """
        N = self.norm()
        if N == 1:
            return True
        if N == 0:
            return False
            
        if not self.is_prime_ideal():
            return False
        
        if self.d >= 0:
            raise ValueError("Only implemented for d < 0")
            
        # Check if the ideal is principal by looking for an element of norm N
        max_b = int(math.isqrt(N // (-self.d)))
        for b in range(-max_b, max_b + 1):
            rem = N + self.d * b**2
            if rem >= 0:
                a = math.isqrt(rem)
                if a**2 == rem:
                    return True
        return False

# Predefined counterexample for convenience: the ideal (2, 1 + sqrt(-5)) in Z[sqrt(-5)].
# This ideal is prime (norm 2) but contains no prime elements (no element has norm 2).
P_counterexample = QuadraticIdeal(-5, [(2, 0), (1, 1)])

def conditions(witness) -> list[bool]:
    # Allow the witness to be passed as a tuple (Ring, Ideal) or just the Ideal
    if isinstance(witness, tuple) and len(witness) == 2:
        witness = witness[1]
        
    try:
        h1 = bool(witness.is_non_zero() and witness.is_prime_ideal())
    except Exception:
        h1 = False
        
    try:
        neg_q = not bool(witness.contains_prime_element())
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a non-zero prime ideal of R",
    "¬Q: P does not contain a non-zero prime element of R"
]

N_HYP = 1
NEG_Q_INDEX = 1