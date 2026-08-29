import math
from sympy.ntheory import jacobi_symbol

def is_int(x):
    if isinstance(x, int):
        return True
    if hasattr(x, 'is_integer'):
        if callable(x.is_integer):
            return x.is_integer()
        return x.is_integer
    return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        a, n = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = is_int(a)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = is_int(a) and is_int(n) and math.gcd(int(a), int(n)) == 1
    except Exception:
        h2_ok = False
        
    try:
        if not (is_int(a) and is_int(n)):
            neg_q_ok = True
        else:
            val = jacobi_symbol(int(a)**2, int(n))
            neg_q_ok = (val != 1)
    except Exception:
        # If jacobi_symbol raises an exception (e.g., n is even or negative),
        # the conclusion that it equals 1 fails.
        neg_q_ok = True
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: gcd(a, n) = 1",
    "¬Q: The Jacobi symbol (a^2/n) != 1 or is undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2