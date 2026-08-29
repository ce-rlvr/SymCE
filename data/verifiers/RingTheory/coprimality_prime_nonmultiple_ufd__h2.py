import sympy
from sympy import gcd, rem
from sympy.abc import x, y, z

# Top-level setup
# No special named groups needed for this ring theory theorem, 
# but we provide symbols for convenience if the witness uses polynomials.

def conditions(witness) -> list[bool]:
    try:
        p, a = witness
    except Exception:
        return [False, False, False]
        
    # H_1: a is non-zero
    try:
        h1 = bool(a != 0)
    except Exception:
        h1 = False
        
    # H_2: p does not divide a
    try:
        if p == 0:
            h2 = bool(a != 0)
        elif isinstance(p, int) and isinstance(a, int):
            h2 = bool(a % p != 0)
        else:
            h2 = bool(sympy.rem(a, p) != 0)
    except Exception:
        h2 = False
        
    # neg_Q: gcd(p, a) != 1
    try:
        g = sympy.gcd(p, a)
        neg_q = bool(g != 1 and g != -1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is non-zero",
    "H_2: p does not divide a",
    "¬Q: gcd(p, a) != 1"
]

N_HYP = 2
NEG_Q_INDEX = 2