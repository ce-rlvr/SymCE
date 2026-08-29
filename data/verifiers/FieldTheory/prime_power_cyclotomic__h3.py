import sympy
from sympy import Symbol, expand, cyclotomic_poly

# Top-level setup
# No specific named objects are required for this polynomial/number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        p, k = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    try:
        h2 = (int(k) == k) and (k >= 1)
    except Exception:
        h2 = False
        
    try:
        x = Symbol('x')
        poly1 = cyclotomic_poly(int(p**k), x)
        poly2 = cyclotomic_poly(int(p), x**(int(p**(k-1))))
        neg_q = expand(poly1 - poly2) != 0
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: k >= 1 is an integer",
    "¬Q: Phi_{p^k}(x) != Phi_p(x^{p^{k-1}})"
]

N_HYP = 2
NEG_Q_INDEX = 2