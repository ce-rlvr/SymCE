import sympy
from sympy import Integer

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a tuple or list of three elements: (a, b, c)
        if len(witness) != 3:
            return [False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False]
        
    # H_1: a, b, and c are strictly positive integers
    try:
        h1 = (isinstance(a, (int, Integer)) and 
              isinstance(b, (int, Integer)) and 
              isinstance(c, (int, Integer)) and 
              a > 0 and b > 0 and c > 0)
        h1 = bool(h1)
    except Exception:
        h1 = False
        
    # H_2: a^2 + b^2 = c^2
    try:
        h2 = bool(a**2 + b**2 == c**2)
    except Exception:
        h2 = False
        
    # ¬Q: The hypotenuse c is divisible by 7
    try:
        neg_q = bool(c % 7 == 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "H_2: a^2 + b^2 = c^2",
    "¬Q: The hypotenuse c is divisible by 7"
]

N_HYP = 2
NEG_Q_INDEX = 2