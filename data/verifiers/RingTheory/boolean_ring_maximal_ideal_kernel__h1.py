import sympy
from sympy import isprime, gcd

class IdealZ:
    """Represents an ideal mZ in the ring of integers Z."""
    def __init__(self, m):
        self.m = abs(int(m))

class IdealZn:
    """Represents an ideal mZn in the ring Zn."""
    def __init__(self, n, m):
        self.n = int(n)
        self.m = gcd(self.n, abs(int(m)))

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, IdealZ):
            m = witness.m
            is_proper = (m >= 2 or m == 0)
            is_maximal = isprime(m)
            is_kernel_Z2 = (m == 2)
        elif isinstance(witness, IdealZn):
            n = witness.n
            m = witness.m
            is_proper = (m > 1 and n > 1)
            is_maximal = isprime(m)
            is_kernel_Z2 = (m == 2 and n % 2 == 0)
        elif isinstance(witness, tuple) and len(witness) == 2:
            n, m = int(witness[0]), int(witness[1])
            m = gcd(n, abs(m))
            is_proper = (m > 1 and n > 1)
            is_maximal = isprime(m)
            is_kernel_Z2 = (m == 2 and n % 2 == 0)
        else:
            m = abs(int(witness))
            is_proper = (m >= 2 or m == 0)
            is_maximal = isprime(m)
            is_kernel_Z2 = (m == 2)
            
        h1 = is_proper
        q = (is_maximal == is_kernel_Z2)
        neg_q = not q
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: M is a proper ideal of R",
    "¬Q: M is a maximal ideal iff M is the kernel of a surjective ring homomorphism to Z_2 (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1