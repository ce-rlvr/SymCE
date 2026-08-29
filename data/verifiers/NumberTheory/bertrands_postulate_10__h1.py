import sympy
from sympy.ntheory import nextprime

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, bool):
            return [False]
        n = int(witness)
        if n != witness:
            return [False]
        
        if n < 2 * n:
            p = nextprime(n)
            found_prime = bool(p < 2 * n)
        else:
            found_prime = False
            
        neg_q = not found_prime
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: There is no prime p such that n < p < 2n"
]

N_HYP = 0
NEG_Q_INDEX = 0