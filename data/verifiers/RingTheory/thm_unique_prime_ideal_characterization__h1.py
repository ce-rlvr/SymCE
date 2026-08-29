import math
from sympy.ntheory import primefactors
import sympy.abc

# Top-level setup for potential witness expressions
x, y, z = sympy.abc.x, sympy.abc.y, sympy.abc.z

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the conjecture.
    We interpret the witness as an integer n representing the ring Z/nZ.
    The only commutative ring satisfying the hypothesis but failing the conclusion
    is the zero ring (n = 1).
    """
    try:
        # Parse the witness to an integer n representing Z/nZ
        if isinstance(witness, str):
            s = witness.strip()
            if s.startswith("Z/") and s.endswith("Z"):
                n = int(s[2:-1])
            else:
                n = int(s)
        else:
            n = int(witness)
            
        # We only consider finite rings Z/nZ for n >= 1
        if n < 1 or n > 10000:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        # H_1: Every element of R is either a unit or a nilpotent element
        h1 = True
        
        # In Z/nZ, an element is nilpotent iff it is divisible by the radical of n
        rad_n = 1
        for p in primefactors(n):
            rad_n *= p
            
        for i in range(n):
            is_unit = (math.gcd(i, n) == 1)
            is_nilpotent = (i % rad_n == 0)
            
            if not (is_unit or is_nilpotent):
                h1 = False
                break
    except Exception:
        h1 = False

    try:
        # ¬Q: R does not have exactly one prime ideal
        # In Z/nZ, the prime ideals correspond to the distinct prime factors of n.
        num_prime_ideals = len(primefactors(n))
        neg_q = (num_prime_ideals != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Every element of R is either a unit or a nilpotent element",
    "¬Q: R does not have exactly one prime ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1