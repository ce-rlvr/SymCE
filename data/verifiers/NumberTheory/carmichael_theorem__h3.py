import math
from sympy import lcm
from sympy.ntheory import factorint

def carmichael_lambda(n):
    if n < 1:
        raise ValueError("n must be a positive integer")
    if n == 1:
        return 1
    factors = factorint(n)
    res = 1
    for p, k in factors.items():
        if p == 2:
            if k == 1:
                val = 1
            elif k == 2:
                val = 2
            else:
                val = 2**(k-2)
        else:
            val = (p**(k-1)) * (p - 1)
        res = lcm(res, val)
    return int(res)

def is_integer(x):
    if isinstance(x, bool):
        return False
    try:
        return int(x) == x
    except Exception:
        return False

def conditions(witness):
    try:
        a, n = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = is_integer(n) and int(n) > 0
    except Exception:
        h1 = False
        
    try:
        h2 = is_integer(a) and math.gcd(int(a), int(n)) == 1
    except Exception:
        h2 = False
        
    try:
        if h1:
            a_int = int(a)
            n_int = int(n)
            lam = carmichael_lambda(n_int)
            q = (pow(a_int, lam, n_int) == 1 % n_int)
            neg_q = not q
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: a is an integer such that gcd(a, n) = 1",
    "¬Q: a^{\\lambda(n)} is not congruent to 1 mod n"
]

N_HYP = 2
NEG_Q_INDEX = 2