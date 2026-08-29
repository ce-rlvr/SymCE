import sympy
from sympy.ntheory import isprime, legendre_symbol
from sympy import Rational

def conditions(witness):
    try:
        p, q = witness
    except Exception:
        return [False, False, False]
        
    # H_1: q is an odd prime
    try:
        h1 = isprime(q) and q % 2 == 1
    except Exception:
        h1 = False
        
    # H_2: p and q are distinct
    try:
        h2 = (p != q)
    except Exception:
        h2 = False
        
    # ¬Q: The Legendre symbols satisfy (p/q)(q/p) = (-1)^(((p-1)/2) * ((q-1)/2))
    try:
        lhs = legendre_symbol(p, q) * legendre_symbol(q, p)
        rhs = (-1)**(Rational(p - 1, 2) * Rational(q - 1, 2))
        neg_q = (lhs != rhs)
    except Exception:
        # If the Legendre symbol is undefined (e.g., p is not an odd prime),
        # the conclusion fails, so its negation is True.
        neg_q = True
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: q is an odd prime",
    "H_2: p and q are distinct",
    "¬Q: (p/q)(q/p) != (-1)^(((p-1)/2) * ((q-1)/2)) or undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2