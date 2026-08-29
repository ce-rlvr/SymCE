import sympy
from sympy import ZZ, QQ
import math
from math import gcd
from functools import reduce

# Top-level setup for standard ring objects
Z = ZZ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a commutative ring with 1 != 0, and I is a proper ideal, then I^n is a proper ideal."
    (The dropped hypothesis is n > 0. The counterexample is n = 0, since I^0 = R is not proper.)
    
    Expected witness formats:
      - A tuple (R, I, n) where R is the ring (e.g., ZZ or an integer m for Z/mZ), 
        I is the ideal generator (int or list of ints), and n is the power.
      - A dict {'R': R, 'I': I, 'n': n}
      - An integer n (defaults to R=ZZ, I=2, n=n)
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R', sympy.ZZ)
            I = witness.get('I', 2)
            n = witness.get('n', 0)
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, I, n = witness
        elif isinstance(witness, (int, sympy.Integer)):
            R = sympy.ZZ
            I = 2
            n = int(witness)
        else:
            return [False] * 4

        # Normalize R=0 to ZZ
        if isinstance(R, (int, sympy.Integer)) and int(R) == 0:
            R = sympy.ZZ

        # Normalize ideal generator I
        if isinstance(I, (list, tuple)):
            I = reduce(gcd, [int(x) for x in I])
        else:
            I = int(I)
            
        n = int(n)
    except Exception:
        return [False] * 4

    # H_1: R is a commutative ring
    try:
        h1 = False
        if R in (sympy.ZZ, sympy.QQ):
            h1 = True
        elif isinstance(R, (int, sympy.Integer)) and int(R) >= 0:
            h1 = True
        elif hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
    except Exception:
        h1 = False

    # H_2: R has an identity element 1 != 0
    try:
        h2 = False
        if R in (sympy.ZZ, sympy.QQ):
            h2 = True
        elif isinstance(R, (int, sympy.Integer)) and int(R) != 1:
            h2 = True
        elif hasattr(R, 'has') and hasattr(R, 'one') and hasattr(R, 'zero'):
            h2 = (R.one != R.zero)
    except Exception:
        h2 = False

    # H_3: I is a proper ideal of R
    try:
        h3 = False
        if R == sympy.ZZ:
            h3 = (abs(I) != 1)
        elif isinstance(R, (int, sympy.Integer)) and int(R) > 1:
            h3 = (gcd(I, int(R)) > 1)
        elif R == sympy.QQ:
            h3 = (I == 0)
    except Exception:
        h3 = False

    # neg_Q: I^n is NOT a proper ideal of R
    try:
        neg_q = False
        if R == sympy.ZZ:
            if n == 0:
                neg_q = True
            elif n > 0:
                neg_q = (abs(I) == 1)
            else:
                neg_q = True
        elif isinstance(R, (int, sympy.Integer)) and int(R) > 1:
            if n == 0:
                neg_q = True
            elif n > 0:
                val = pow(I, n, int(R))
                neg_q = (gcd(val, int(R)) == 1)
            else:
                neg_q = True
        elif R == sympy.QQ:
            if n == 0:
                neg_q = True
            elif n > 0:
                neg_q = (I != 0)
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R has an identity element 1 != 0",
    "H_3: I is a proper ideal of R",
    "¬Q: I^n is not a proper ideal of R"
]

N_HYP = 3
NEG_Q_INDEX = 3