import math
import sympy

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        a, n = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and int(n) > 1
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(a, (int, sympy.Integer)) and 0 <= int(a) < int(n)
    except Exception:
        h2 = False
        
    try:
        a_int = int(a)
        n_int = int(n)
        
        try:
            pow(a_int, -1, n_int)
            is_unit = True
        except ValueError:
            is_unit = False
            
        gcd_is_1 = (math.gcd(a_int, n_int) == 1)
        
        neg_q = not (is_unit == gcd_is_1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: a is an element of Z_n",
    "¬Q: it is not the case that a is a unit in Z_n iff gcd(a, n) == 1"
]

N_HYP = 2
NEG_Q_INDEX = 2