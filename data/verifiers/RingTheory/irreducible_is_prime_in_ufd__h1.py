import math
import sympy
from sympy import isprime

class Z_sqrt_md_Element:
    """
    Represents an element a + b*sqrt(-d) in the ring Z[sqrt(-d)].
    """
    def __init__(self, d, a, b=0):
        self.d = d
        self.a = a
        self.b = b
    
    def norm(self):
        return self.a**2 + self.d * self.b**2

    def is_norm(self, n):
        if n < 0: 
            return False
        for b in range(int(math.isqrt(n // self.d)) + 1):
            rem = n - self.d * b**2
            a = int(math.isqrt(rem))
            if a**2 == rem:
                return True
        return False

    def is_irreducible(self):
        n = self.norm()
        if n <= 1:
            return False
        for k in range(2, int(math.isqrt(n)) + 1):
            if n % k == 0:
                if self.is_norm(k) and self.is_norm(n // k):
                    return False
        return True

    def divides(self, other):
        if not isinstance(other, Z_sqrt_md_Element):
            try:
                other = Z_sqrt_md_Element(self.d, int(other), 0)
            except Exception:
                return False
        n = self.norm()
        if n == 0:
            return False
        real_num = other.a * self.a + self.d * other.b * self.b
        imag_num = other.b * self.a - other.a * self.b
        return real_num % n == 0 and imag_num % n == 0

    def __mul__(self, other):
        if not isinstance(other, Z_sqrt_md_Element):
            try:
                other = Z_sqrt_md_Element(self.d, int(other), 0)
            except Exception:
                return NotImplemented
        if self.d != other.d:
            return NotImplemented
        return Z_sqrt_md_Element(self.d,
                                 self.a * other.a - self.d * self.b * other.b,
                                 self.a * other.b + self.b * other.a)

    def is_prime(self):
        n = self.norm()
        if n <= 1:
            return False
        
        # Bounded search for a counterexample to primality
        limit = 12
        elements = [Z_sqrt_md_Element(self.d, a, b) 
                    for a in range(-limit, limit + 1) 
                    for b in range(-limit, limit + 1)]
        
        non_multiples = [x for x in elements if not self.divides(x)]
        
        for i in range(len(non_multiples)):
            x = non_multiples[i]
            for j in range(i, len(non_multiples)):
                y = non_multiples[j]
                xy = x * y
                if self.divides(xy):
                    return False
        return True

    def __repr__(self):
        return f"Z_sqrt_m{self.d}({self.a}, {self.b})"

# Standard non-UFD rings of integers for testing counterexamples
def Z_sqrt_m3(a, b=0): return Z_sqrt_md_Element(3, a, b)
def Z_sqrt_m5(a, b=0): return Z_sqrt_md_Element(5, a, b)
def Z_sqrt_m6(a, b=0): return Z_sqrt_md_Element(6, a, b)
def Z_sqrt_m7(a, b=0): return Z_sqrt_md_Element(7, a, b)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        if hasattr(witness, 'is_irreducible'):
            irr = witness.is_irreducible
            if callable(irr):
                h1 = bool(irr())
            else:
                h1 = bool(irr)
        else:
            h1 = bool(isprime(witness))
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'is_prime'):
            prm = witness.is_prime
            if callable(prm):
                neg_q = not bool(prm())
            else:
                neg_q = not bool(prm)
        else:
            neg_q = not bool(isprime(witness))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is an irreducible element in R",
    "¬Q: p is not a prime element in R"
]

N_HYP = 1
NEG_Q_INDEX = 1