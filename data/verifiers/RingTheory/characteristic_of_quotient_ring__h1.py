import math
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness references
Z = sympy.S.Integers
Q = sympy.S.Rationals

def conditions(witness) -> list[bool]:
    """
    Given a witness representing (R, I, n) where:
      - R is the ring Z_m (represented by its characteristic m, with m=0 meaning Z)
      - I is the principal ideal <k> in Z_m (represented by the generator k)
      - n is an integer
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        m, k, n = witness
        
        # Allow sympy.S.Integers to represent the ring of integers (characteristic 0)
        if m == Z:
            m = 0
            
        m = abs(int(m))
        k = int(k)
        n = int(n)
        
        # H_1: I is a proper ideal of R
        # In Z_m, <k> is proper if it does not generate the whole ring.
        if m == 1:
            h1_ok = False  # Z_1 is the zero ring, has no proper ideals
        elif m == 0:
            h1_ok = abs(k) != 1
        else:
            h1_ok = math.gcd(m, k) != 1
            
        # neg_Q: The characteristic of R/I does NOT divide n
        # The quotient ring Z_m / <k> is isomorphic to Z_c where c = gcd(m, k) (or abs(k) if m=0)
        if m == 0:
            c = abs(k)
        else:
            c = math.gcd(m, k)
            
        if c == 0:
            divides = (n == 0)
        else:
            divides = (n % c == 0)
            
        neg_q_ok = not divides
        
        return [bool(h1_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: The characteristic of R/I does not divide n"
]

N_HYP = 1
NEG_Q_INDEX = 1