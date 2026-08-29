import sympy
from sympy.ntheory import totient

# No named bindings needed for number theory

def conditions(witness):
    try:
        a, n = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = (int(a) == a) and (int(n) == n) and (a > 0) and (n > 0)
    except Exception:
        h1 = False
        
    try:
        if h1:
            a_int = int(a)
            n_int = int(n)
            val = a_int**n_int + 1
            phi_val = totient(val)
            neg_q = (phi_val % (2 * n_int)) != 0
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a and n are positive integers",
    "¬Q: 2n does not divide phi(a^n + 1)"
]

N_HYP = 1
NEG_Q_INDEX = 1