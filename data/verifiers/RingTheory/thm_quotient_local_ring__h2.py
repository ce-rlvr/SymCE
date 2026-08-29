import sympy
from sympy import factorint
import math

# Top-level setup
# Witnesses for this conjecture are expected to be tuples of integers (n, m),
# representing the ring R = Z/nZ and the ideal I = mZ/nZ.

def conditions(witness) -> list[bool]:
    try:
        n, m = witness
        n = int(n)
        m = int(m)
    except Exception:
        return [False, False]
        
    # H_1: R is a local ring
    # R = Z/nZ is a local ring iff n has exactly one prime factor.
    try:
        n_abs = abs(n)
        if n_abs == 0 or n_abs == 1:
            h1 = False
        else:
            h1 = len(factorint(n_abs)) == 1
    except Exception:
        h1 = False
        
    # ¬Q: The quotient ring R/I is not a local ring
    # R/I is isomorphic to Z/gZ where g = gcd(n, m).
    # It is a local ring iff g has exactly one prime factor.
    try:
        g = math.gcd(n, m)
        if g == 0 or g == 1:
            is_local_quotient = False
        else:
            is_local_quotient = len(factorint(g)) == 1
        neg_q = not is_local_quotient
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a local ring",
    "¬Q: The quotient ring R/I is not a local ring"
]

N_HYP = 1
NEG_Q_INDEX = 1