import sympy
from sympy.ntheory import isprime, n_order

# Top-level setup (no specific named objects needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        a, p = witness
    except Exception:
        return [False, False, False]
    
    # H1: a is an integer
    try:
        h1 = isinstance(a, (int, sympy.Integer))
    except Exception:
        h1 = False
        
    # H2: p is an odd prime number
    try:
        h2 = isinstance(p, (int, sympy.Integer)) and p % 2 != 0 and isprime(p)
    except Exception:
        h2 = False
        
    # ¬Q: The multiplicative order of a modulo p is not exactly 4
    try:
        if not isinstance(a, (int, sympy.Integer)) or not isinstance(p, (int, sympy.Integer)):
            neg_q = False
        elif sympy.gcd(a, p) != 1:
            # If gcd(a, p) != 1, the multiplicative order is undefined (so it is not 4)
            neg_q = True
        else:
            neg_q = (n_order(a, p) != 4)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a is an integer",
    "H_2: p is an odd prime number",
    "¬Q: The multiplicative order of a modulo p is not exactly 4"
]

N_HYP = 2
NEG_Q_INDEX = 2