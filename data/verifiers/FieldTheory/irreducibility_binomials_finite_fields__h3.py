import sympy
from sympy import factorint, isprime

# Top-level setup
# (No specific named objects required for this domain)

def conditions(witness) -> list[bool]:
    try:
        q, p, a = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F_q is a finite field with q elements
    try:
        q_int = int(q)
        factors = factorint(q_int)
        h1_ok = (len(factors) == 1)
    except Exception:
        h1_ok = False
        
    # H_2: p is a prime number dividing q-1
    try:
        p_int = int(p)
        q_int = int(q)
        h2_ok = isprime(p_int) and ((q_int - 1) % p_int == 0)
    except Exception:
        h2_ok = False
        
    # neg_Q: The binomial x^p - a is reducible over F_q
    try:
        q_int = int(q)
        p_int = int(p)
        factors_q = factorint(q_int)
        if len(factors_q) != 1:
            neg_q_ok = False
        else:
            r = list(factors_q.keys())[0]
            power = (q_int - 1) // p_int
            a_int = int(a)
            a_mod = a_int % r
            if a_mod == 0:
                neg_q_ok = True
            else:
                neg_q_ok = (pow(a_mod, power, r) == 1)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: p is a prime number dividing q-1",
    "¬Q: The binomial x^p - a is reducible over F_q"
]

N_HYP = 2
NEG_Q_INDEX = 2