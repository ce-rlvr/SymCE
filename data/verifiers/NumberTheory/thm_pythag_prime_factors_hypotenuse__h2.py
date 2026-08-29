import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        a, b, c, p = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = bool(isinstance(a, int) and isinstance(b, int) and isinstance(c, int) and
                  a > 0 and b > 0 and c > 0 and
                  a**2 + b**2 == c**2 and math.gcd(a, b) == 1)
    except Exception:
        h1 = False
        
    try:
        neg_q = bool(sympy.isprime(p) and p % 4 != 1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (a, b, c) is a primitive Pythagorean triple with hypotenuse c",
    "¬Q: The prime p is not congruent to 1 (mod 4)"
]

N_HYP = 1
NEG_Q_INDEX = 1