import sympy
from sympy.ntheory import totient

def conditions(witness):
    """
    Given a witness (n, p), checks if it is a valid counterexample to the false conjecture.
    """
    try:
        n, p = witness
    except Exception:
        return [False, False, False]
    
    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False
        
    # H_2: p does not divide n
    try:
        if not isinstance(p, (int, sympy.Integer)):
            h2 = False
        elif p == 0:
            h2 = (n != 0)
        else:
            h2 = (n % p != 0)
    except Exception:
        h2 = False
        
    # ¬Q: \phi(pn) != (p-1)\phi(n)
    try:
        neg_q = totient(p * n) != (p - 1) * totient(n)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: p does not divide n",
    "¬Q: phi(pn) != (p-1)phi(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2