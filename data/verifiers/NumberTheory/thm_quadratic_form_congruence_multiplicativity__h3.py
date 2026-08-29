import sympy
import math
import itertools

def count_sols(a, k):
    if k <= 0:
        return 0
    count = 0
    a_mod = a % k
    for x in range(k):
        for y in range(k):
            if (x*x + x*y + y*y) % k == a_mod:
                count += 1
    return count

def is_int(x):
    return isinstance(x, int) or (hasattr(x, 'is_integer') and x.is_integer)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the conjecture.
    witness is expected to be a tuple (a, m, n).
    """
    try:
        if not (isinstance(witness, (tuple, list)) and len(witness) == 3):
            return [False, False, False]
        a, m, n = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(is_int(a))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(is_int(m) and is_int(n) and m > 0 and n > 0)
    except Exception:
        h2 = False
        
    try:
        if h1 and h2:
            a_val = int(a)
            m_val = int(m)
            n_val = int(n)
            
            # To prevent excessive computation time for unreasonably large witnesses
            if m_val * n_val > 10000:
                neg_q = False
            else:
                sols_mn = count_sols(a_val, m_val * n_val)
                sols_m = count_sols(a_val, m_val)
                sols_n = count_sols(a_val, n_val)
                neg_q = bool(sols_mn != sols_m * sols_n)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: m and n are positive integers",
    "¬Q: The number of solutions modulo mn is not the product of the number of solutions modulo m and modulo n"
]

N_HYP = 2
NEG_Q_INDEX = 2