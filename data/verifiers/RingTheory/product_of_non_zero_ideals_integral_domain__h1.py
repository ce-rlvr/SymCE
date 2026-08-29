import sympy
import math

# Top-level setup
# For this ring theory conjecture, a common counterexample is in Z/nZ.
# The witness is expected to be a tuple (n, I, J) representing the ring Z/nZ
# and the ideals I and J. Ideals can be given as generators or lists of elements.
Z4 = 4
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    try:
        n, I_obj, J_obj = witness
        
        if isinstance(n, (list, tuple)):
            n = n[0]
        n = int(n)
        
        if n <= 1:
            return [False, False, False]
            
        if isinstance(I_obj, (list, tuple, set)):
            a = 0
            for x in I_obj:
                a = math.gcd(a, int(x))
        else:
            a = int(I_obj)
            
        if isinstance(J_obj, (list, tuple, set)):
            b = 0
            for x in J_obj:
                b = math.gcd(b, int(x))
        else:
            b = int(J_obj)
            
        h1 = (a % n) != 0
        h2 = (b % n) != 0
        neg_q = (a * b) % n == 0
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is a non-zero ideal of R",
    "H_2: J is a non-zero ideal of R",
    "¬Q: The product ideal IJ is zero"
]

N_HYP = 2
NEG_Q_INDEX = 2