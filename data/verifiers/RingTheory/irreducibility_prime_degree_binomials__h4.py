import sympy
from sympy import Poly, isprime
from sympy.abc import x
from sympy.polys.domains import QQ, RR, CC, GF, ZZ

# Top-level setup: named object bindings that the witness expression may reference.
# The witness is expected to be a tuple: (F, p, a)
# where F is a SymPy field domain (e.g., QQ, GF(5)), p is a prime, and a is an element of F.

def conditions(witness):
    try:
        F, p, a = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = isprime(p)
    except Exception:
        h2 = False
        
    # H_3: a is an element of F
    try:
        h3 = a in F
    except Exception:
        h3 = False
        
    # ¬Q: x^p - a is reducible over F
    try:
        poly = Poly(x**p - a, x, domain=F)
        neg_q = not poly.is_irreducible
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: p is a prime number",
    "H_3: a is an element of F",
    "¬Q: x^p - a is reducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3