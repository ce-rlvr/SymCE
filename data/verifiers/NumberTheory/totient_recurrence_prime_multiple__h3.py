import sympy
from sympy.ntheory import isprime, totient

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        n, p = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(p, (int, sympy.Integer)) and isprime(p)
    except Exception:
        h2 = False
        
    try:
        neg_q = bool(totient(p * n) != p * totient(n))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: n is a positive integer",
    "H_2: p is a prime number",
    "¬Q: phi(pn) != p*phi(n)"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2