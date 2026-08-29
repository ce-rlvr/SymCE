import sympy
from sympy import Rational
from math import gcd
from sympy.ntheory import factorint
from sympy.abc import x, y, z

# Top-level setup
# Witness is expected to be an integer x (for ring Z) or a tuple (n, x) for ring Z/nZ.

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "If R is a commutative ring and x is a nilpotent element, then x is a zero divisor in R."
    
    The witness is expected to be either:
      - An integer x, representing the element x in the ring R = Z.
      - A tuple (n, x), representing the element x in the ring R = Z/nZ.
    """
    try:
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            n, val = witness
            n = abs(int(n))
            val = int(val)
        else:
            n = 0
            val = int(witness)
    except Exception:
        return [False, False, False]
        
    # H1: R is a commutative ring
    # Z and Z/nZ are always commutative rings.
    h1 = True
    
    # H2: x is a nilpotent element
    try:
        if n == 0:
            h2 = (val == 0)
        elif n == 1:
            h2 = True
        else:
            factors = factorint(n)
            h2 = all((val % p == 0) for p in factors.keys())
    except Exception:
        h2 = False
        
    # neg_Q: x is NOT a zero divisor in R
    # Note: The true theorem is "Non-zero nilpotent elements are zero divisors",
    # which implies that 0 is not considered a zero divisor in this context.
    try:
        if n == 0:
            # In Z, 0 is not a zero divisor (requires a non-zero element)
            is_zd = False
        elif n == 1:
            # In Z/1Z, there are no non-zero elements, so no zero divisors
            is_zd = False
        else:
            val_mod = val % n
            if val_mod == 0:
                # 0 is not considered a zero divisor
                is_zd = False
            else:
                is_zd = (gcd(val_mod, n) > 1)
        neg_q = not is_zd
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: x is a nilpotent element",
    "¬Q: x is not a zero divisor in R"
]

N_HYP = 2
NEG_Q_INDEX = 2