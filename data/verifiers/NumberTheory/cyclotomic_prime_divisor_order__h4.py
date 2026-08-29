import sympy
from sympy.ntheory import isprime, n_order

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        n, a, p = witness
    except Exception:
        return [False, False, False, False]

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and not isinstance(n, bool) and int(n) > 0
    except Exception:
        h1 = False

    # H_2: a is an integer strictly greater than 1
    try:
        h2 = isinstance(a, (int, sympy.Integer)) and not isinstance(a, bool) and int(a) > 1
    except Exception:
        h2 = False

    # H_3: p is a prime number
    try:
        h3 = isinstance(p, (int, sympy.Integer)) and not isinstance(p, bool) and isprime(int(p))
    except Exception:
        h3 = False

    # neg_Q: p does not divide n and the multiplicative order of a modulo p is not exactly n
    try:
        n_val = int(n)
        a_val = int(a)
        p_val = int(p)
        
        p_divides_n = (n_val % p_val == 0)
        
        if a_val % p_val == 0:
            order_is_n = False
        else:
            order_is_n = (n_order(a_val, p_val) == n_val)
            
        neg_q = (not p_divides_n) and (not order_is_n)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: a is an integer strictly greater than 1",
    "H_3: p is a prime number",
    "¬Q: p does not divide n and the multiplicative order of a modulo p is not exactly n"
]

N_HYP = 3
NEG_Q_INDEX = 3