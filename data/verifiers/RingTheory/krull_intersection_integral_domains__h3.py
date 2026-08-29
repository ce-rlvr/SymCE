import math
import sympy
from sympy import Rational, Integer

# Top-level setup
# Witness is expected to be a tuple (n, a) representing the ring Z/nZ and the principal ideal (a).

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False, False]
        
        n_val, a_val = witness
        n = int(n_val)
        a = int(a_val)
        
        # H_1: R is a commutative ring
        # Z/nZ is a commutative ring for any n > 1
        h1 = (n > 1)
        
        # H_2: R is a Noetherian ring
        # Z/nZ is finite, hence it is always a Noetherian ring
        h2 = (n > 1)
        
        # H_3: I is a proper ideal of R
        # In Z/nZ, the principal ideal (a) is proper iff gcd(a, n) > 1
        h3 = (n > 1) and (math.gcd(a % n, n) > 1)
        
        # ¬Q: The intersection of I^k is not the zero ideal
        # In Z/nZ, the sequence of ideals (a) >= (a^2) >= (a^3) ... stabilizes.
        # The intersection is (0) iff 'a' is nilpotent modulo n.
        # 'a' is nilpotent mod n iff a^n % n == 0.
        # Therefore, the intersection is NOT (0) iff a^n % n != 0.
        neg_q = (n > 1) and (pow(a, n, n) != 0)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a Noetherian ring",
    "H_3: I is a proper ideal of R",
    "¬Q: The intersection of I^n is not the zero ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3