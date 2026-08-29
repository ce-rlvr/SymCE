import math
import sympy
from sympy.ntheory import totient

def is_int(x):
    return (isinstance(x, int) or isinstance(x, sympy.Integer)) and not isinstance(x, bool)

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, S_wit = witness
            h1 = is_int(n)
            if h1:
                n_int = int(n)
                if n_int <= 1:
                    S_calc = 0
                else:
                    S_calc = int(n_int * totient(n_int) // 2)
                h2 = (S_wit == S_calc)
                n_val = n_int
                S_val = S_wit
        else:
            n_val = witness
            h1 = is_int(n_val)
            if h1:
                n_int = int(n_val)
                if n_int <= 1:
                    S_val = 0
                else:
                    S_val = int(n_int * totient(n_int) // 2)
                h2 = True
                n_val = n_int
    except Exception:
        pass

    try:
        if h1 and h2:
            if n_val == 0:
                neg_q = (S_val != 0)
            else:
                neg_q = (S_val % n_val) != 0
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "H_2: S is the sum of all positive integers k such that 1 <= k < n and gcd(k, n) = 1",
    "¬Q: S is not congruent to 0 mod n"
]

N_HYP = 2
NEG_Q_INDEX = 2