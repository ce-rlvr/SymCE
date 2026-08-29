import sympy as sp
from sympy.ntheory import factorint

def is_prime_power(q):
    try:
        if not isinstance(q, int) or q < 2:
            return False
        factors = factorint(q)
        return len(factors) == 1
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            q = witness.get('q', 0)
            n = witness.get('n', -1)
        elif isinstance(witness, tuple) and len(witness) == 2:
            a, b = witness
            if is_prime_power(a) and not is_prime_power(b):
                q, n = a, b
            elif is_prime_power(b) and not is_prime_power(a):
                q, n = b, a
            else:
                q, n = a, b
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_prime_power(q)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(n, int) and n >= 0
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            if n == 0:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field of order q",
    "H_2: F_{q^n} is the field extension of F_q of degree n",
    "¬Q: Minimal polynomials do not exactly match irreducible polynomials of dividing degree"
]

N_HYP = 2
NEG_Q_INDEX = 2