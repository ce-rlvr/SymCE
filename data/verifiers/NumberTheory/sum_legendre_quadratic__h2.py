import sympy
from sympy.ntheory import isprime, legendre_symbol

def conditions(witness):
    """
    Given a witness (p, a), checks if it is a counterexample to the conjecture.
    """
    try:
        p, a = witness
    except Exception:
        return [False, False, False]
    
    # H_1: p is an odd prime
    try:
        h1 = bool(isprime(p) and int(p) % 2 != 0)
    except Exception:
        h1 = False
        
    # H_2: p does not divide a
    try:
        h2 = bool(int(a) % int(p) != 0)
    except Exception:
        h2 = False
        
    # neg_Q: sum_{x=0}^{p-1} ( (x^2+a)/p ) != -1
    try:
        p_int = int(p)
        a_int = int(a)
        s = sum(legendre_symbol(x**2 + a_int, p_int) for x in range(p_int))
        neg_q = bool(s != -1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: p does not divide a",
    "¬Q: sum_{x=0}^{p-1} ((x^2+a)/p) != -1"
]

N_HYP = 2
NEG_Q_INDEX = 2