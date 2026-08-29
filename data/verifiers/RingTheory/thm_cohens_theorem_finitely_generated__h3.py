import sympy
from sympy import ZZ, QQ
from sympy.ntheory import isprime
import math
from functools import reduce

# Top-level setup
Z = ZZ

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
        else:
            R = ZZ
            I = witness
            
        # H1: R is a commutative ring
        if R in (ZZ, QQ):
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
            
        # H2: I is an ideal of R
        if R == ZZ:
            if isinstance(I, (int, sympy.Integer)):
                h2 = True
            elif isinstance(I, (list, tuple)) and all(isinstance(x, (int, sympy.Integer)) for x in I):
                h2 = True
                
        # neg_Q: I is not a prime ideal
        if R == ZZ and h2:
            if isinstance(I, (int, sympy.Integer)):
                val = abs(int(I))
            elif len(I) == 0:
                val = 0
            else:
                val = abs(reduce(math.gcd, [int(x) for x in I]))
                
            # In ZZ, an ideal nZ is prime iff n is prime or n == 0.
            # The whole ring (n=1) is not a prime ideal.
            if val == 0:
                neg_q = False
            elif val == 1:
                neg_q = True
            elif not isprime(val):
                neg_q = True
            else:
                neg_q = False
                
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: I is not a prime ideal"
]

N_HYP = 2
NEG_Q_INDEX = 2