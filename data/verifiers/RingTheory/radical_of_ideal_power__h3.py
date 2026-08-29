import sympy
from sympy.ntheory import factorint
from math import gcd
from functools import reduce

# Top-level setup
ZZ = sympy.S.Integers

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "The radical of the ideal I^n is equal to the radical of I"
    (The dropped hypothesis is that n is a positive integer, n >= 1. 
     For n = 0, I^0 = R, so rad(I^0) = R, which generally does not equal rad(I).)
    """
    try:
        # Parse the witness. We expect it to provide the ideal generator(s) and the power n.
        if isinstance(witness, tuple):
            if len(witness) == 2:
                k, n = witness
            elif len(witness) == 3:
                R, k, n = witness
            else:
                return [False, False, False]
        elif isinstance(witness, dict):
            k = witness.get('I', witness.get('k'))
            n = witness.get('n')
            if k is None or n is None:
                return [False, False, False]
        else:
            return [False, False, False]
            
        # Extract the generator for the ideal in Z
        if isinstance(k, (list, tuple, set)):
            k = reduce(gcd, [int(x) for x in k])
        else:
            k = int(k)
            
        n = int(n)
        
        # H_1: R is a commutative ring (Z is a commutative ring)
        h1 = True
        
        # H_2: I is an ideal of R (Any integer k generates an ideal in Z)
        h2 = True
        
        # If n < 0, I^n is generally undefined for non-invertible ideals
        if n < 0:
            return [h1, h2, False]
            
        def radical_Z(x):
            if x == 0:
                return 0
            x = abs(x)
            if x == 1:
                return 1
            factors = factorint(x)
            rad = 1
            for p in factors:
                rad *= p
            return rad
            
        rad_I = radical_Z(k)
        
        # For n == 0, I^0 = R = (1), so its radical is (1)
        # For n > 0, the prime factors of k^n are exactly the prime factors of k,
        # so rad(I^n) = rad(I). This avoids computing large powers.
        if n == 0:
            rad_In = 1
        else:
            rad_In = rad_I
            
        # neg_Q: The radical of I^n is NOT equal to the radical of I
        neg_q = (rad_In != rad_I)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: The radical of I^n is not equal to the radical of I"
]

N_HYP = 2
NEG_Q_INDEX = 2