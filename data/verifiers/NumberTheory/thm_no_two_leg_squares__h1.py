import math
import sympy
from sympy import Rational, Integer

def is_perfect_square(n):
    try:
        if n < 0:
            return False
        root = math.isqrt(n)
        return root * root == n
    except Exception:
        return False

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple of three integers (a, b, c).
    """
    try:
        # Unpack the witness
        if len(witness) != 3:
            return [False, False]
        a, b, c = witness
        
        # Ensure they are integers
        a_int, b_int, c_int = int(a), int(b), int(c)
        if a != a_int or b != b_int or c != c_int:
            return [False, False]
        a, b, c = a_int, b_int, c_int
    except Exception:
        return [False, False]
    
    # H_1: a^2 + b^2 = c^2
    try:
        h1 = (a**2 + b**2 == c**2)
    except Exception:
        h1 = False
        
    # ¬Q: both a and b are perfect squares of integers
    try:
        neg_q = is_perfect_square(a) and is_perfect_square(b)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a^2 + b^2 = c^2",
    "¬Q: both a and b are perfect squares of integers"
]

N_HYP = 1
NEG_Q_INDEX = 1