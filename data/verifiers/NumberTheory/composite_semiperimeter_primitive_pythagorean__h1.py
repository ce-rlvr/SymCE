import math
import sympy

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and fails the conclusion.
    The witness should be a tuple or list of three integers (a, b, c).
    """
    try:
        a, b, c = witness
        a = int(a)
        b = int(b)
        c = int(c)
    except Exception:
        return [False, False]
    
    # H_1: \gcd(a, b, c) = 1
    try:
        h1 = (math.gcd(math.gcd(a, b), c) == 1)
    except Exception:
        h1 = False
        
    # neg_Q: The semiperimeter s = (a+b+c)/2 is NOT a composite integer.
    # A composite integer is an integer > 1 that is not prime.
    try:
        s_num = a + b + c
        if s_num % 2 != 0:
            # s is not an integer, so it is not a composite integer
            neg_q = True
        else:
            s = s_num // 2
            if s <= 1:
                # Integers <= 1 are not composite
                neg_q = True
            else:
                # If s > 1, it is not composite if it is prime
                neg_q = sympy.isprime(s)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: gcd(a, b, c) = 1",
    "¬Q: The semiperimeter s = (a+b+c)/2 is not a composite integer"
]

N_HYP = 1
NEG_Q_INDEX = 1