import math
import sympy
from sympy import Rational, Integer

# Top-level setup for potential witness expressions
# For this domain, witnesses are typically integers n (representing R = Z/nZ and M = Z/nZ)
# or tuples (n, m) (representing R = Z/nZ and M = Z/mZ).
# No special named bindings are required for number theory / rings as per instructions,
# but we provide a few common cyclic ring sizes just in case.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z12 = 12

def extract_int(obj):
    """Helper to safely extract an integer from a witness object."""
    try:
        val = int(obj)
        # Ensure it's exactly equal to avoid truncating floats
        if val == obj:
            return val
    except Exception:
        pass
    return None

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If M is a flat module over R, then M is a torsion-free R-module."
    
    The witness is expected to be an integer n (meaning R = Z/nZ, M = Z/nZ)
    or a tuple (n, m) (meaning R = Z/nZ, M = Z/mZ).
    """
    try:
        n, m = None, None
        if isinstance(witness, tuple) and len(witness) == 2:
            n = extract_int(witness[0])
            m = extract_int(witness[1])
        else:
            n = extract_int(witness)
            m = n
            
        if n is None or m is None:
            return [False, False]
            
        # R and M must be non-trivial
        if n <= 1 or m <= 0:
            return [False, False]
            
        # For M = Z/mZ to be a valid R-module over R = Z/nZ, m must divide n
        if n % m != 0:
            return [False, False]
            
        # H_1: M is a flat module over R
        # Over the Artinian ring Z/nZ, a module Z/mZ is flat iff it is projective,
        # which happens iff it is a direct summand of Z/nZ.
        # This is true iff gcd(m, n/m) == 1.
        is_flat = (math.gcd(m, n // m) == 1)
        
        # ¬Q: M is not a torsion-free R-module
        # M is torsion-free if for all r in R and x in M, r*x = 0 implies r = 0 or x = 0.
        # We look for a counterexample: r != 0 in R, x != 0 in M, such that r*x == 0 in M.
        is_not_torsion_free = False
        for r in range(1, n):
            for x in range(1, m):
                if (r * x) % m == 0:
                    is_not_torsion_free = True
                    break
            if is_not_torsion_free:
                break
                
        return [is_flat, is_not_torsion_free]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: M is a flat module over R",
    "¬Q: M is not a torsion-free R-module"
]

N_HYP = 1
NEG_Q_INDEX = 1