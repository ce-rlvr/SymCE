import sympy
from sympy import Poly, Symbol, GF, QQ

x = Symbol('x')
t = Symbol('t')

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, Poly):
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = witness.degree() >= 1 and witness.is_irreducible
    except Exception:
        h1 = False
        
    try:
        f_prime = witness.diff()
        g = witness.gcd(f_prime)
        h2 = g.degree() == 0
    except Exception:
        h2 = False
        
    try:
        char = witness.domain.char
        deg = witness.degree()
        if char == 0:
            neg_q = False
        else:
            neg_q = (0 != deg)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: E over K is a finite field extension",
    "H_2: E over K is a separable extension",
    "not Q: The number of K-algebra homomorphisms from E into C is not the degree of E over K"
]

N_HYP = 2
NEG_Q_INDEX = 2