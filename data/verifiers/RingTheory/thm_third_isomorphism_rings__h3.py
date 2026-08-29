import math
import itertools
import functools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for Ring Theory
# We model the rings as Z/kZ (where k=0 represents Z).
# The witness is expected to be a tuple (k, n, m) or (n, m) representing
# the ring R = Z/kZ and the ideals I = nR, J = mR.

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                k, n, m = witness
                if isinstance(k, str) or k == 0:
                    k = 0
                else:
                    k = int(k)
            elif len(witness) == 2:
                k = 0
                n, m = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        n = int(n)
        m = int(m)
        
        # H_1: R is a ring
        # Z/kZ is always a ring.
        h1 = True
        
        # H_2: I and J are ideals of R
        # nR and mR are always ideals of R.
        h2 = True
        
        # ¬Q: J/I is not an ideal of R/I, or (R/I)/(J/I) is not isomorphic to R/J
        # In our model R = Z/kZ, I = nR, J = mR.
        # The quotient (R/I)/(J/I) is naturally isomorphic to R/(I+J).
        # R/(I+J) is isomorphic to Z / gcd(k, n, m)Z.
        # R/J is isomorphic to Z / gcd(k, m)Z.
        # These two finite (or infinite if k=0) cyclic rings are isomorphic 
        # if and only if their characteristic ideals are the same.
        if k == 0:
            neg_q = math.gcd(n, m) != abs(m)
        else:
            k = abs(k)
            gcd_km = math.gcd(k, m)
            gcd_knm = math.gcd(k, math.gcd(n, m))
            neg_q = gcd_knm != gcd_km
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I and J are ideals of R",
    "¬Q: J/I is not an ideal of R/I, or (R/I)/(J/I) is not isomorphic to R/J"
]

N_HYP = 2
NEG_Q_INDEX = 2