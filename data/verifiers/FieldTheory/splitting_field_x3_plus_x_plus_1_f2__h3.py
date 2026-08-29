import sympy
from sympy import GF, Poly, Symbol

x = Symbol('x')
F2 = GF(2)
f = x**3 + x + 1

def conditions(witness):
    h1 = True
    h2 = True
    try:
        E = witness
        size = None
        if isinstance(E, int):
            size = E
        elif isinstance(E, (list, set, tuple)):
            size = len(E)
        elif hasattr(E, 'is_Poly') and E.is_Poly:
            if hasattr(E.domain, 'order'):
                size = E.domain.order ** E.degree()
        elif hasattr(E, 'order'):
            if callable(E.order):
                size = E.order()
            else:
                size = E.order
        elif hasattr(E, 'mod'):
            size = int(E.mod)
        elif hasattr(E, 'domain') and hasattr(E.domain, 'order'):
            size = E.domain.order
            
        if size is not None:
            neg_q = (size != 8)
        else:
            neg_q = True
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_2 is the finite field with 2 elements",
    "H_2: f(x) = x^3 + x + 1 is a polynomial over F_2",
    "¬Q: The degree of E over F_2 is not 3, or E is not isomorphic to F_8"
]

N_HYP = 2
NEG_Q_INDEX = 2