import sympy
from sympy import Poly, QQ, RR, CC
from sympy.abc import x
import math

# Top-level setup
Z2 = sympy.GF(2)
Z3 = sympy.GF(3)
Z5 = sympy.GF(5)

def conditions(witness) -> list[bool]:
    F = None
    p = None
    n = None
    
    # Unpack witness
    if isinstance(witness, tuple):
        if len(witness) == 3:
            F, p, n = witness
        elif len(witness) == 2:
            # Distinguish between (F, p) and (p, n)
            if hasattr(witness[0], 'is_Field') or witness[0] in [QQ, RR, CC] or hasattr(witness[0], 'is_field'):
                F, p = witness
            else:
                p, n = witness
        elif len(witness) == 1:
            p = witness[0]
    else:
        p = witness

    # Default F to the domain of p, or QQ
    if F is None:
        if hasattr(p, 'domain'):
            F = p.domain
        else:
            F = QQ
            
    # Default n to the degree of p
    if n is None:
        try:
            poly_p = Poly(p, domain=F)
            n = poly_p.degree()
        except Exception:
            n = 0

    # H1: F is a field
    h1 = False
    try:
        if hasattr(F, 'is_Field'):
            h1 = bool(F.is_Field)
        elif F in [QQ, RR, CC]:
            h1 = True
        elif hasattr(F, 'is_field'):
            h1 = bool(F.is_field)
    except Exception:
        pass

    # H2: p is a polynomial
    h2 = False
    try:
        poly_p = Poly(p, domain=F)
        if len(poly_p.gens) <= 1:
            h2 = True
    except Exception:
        pass

    # neg_Q: The factor ring does NOT have dimension n
    neg_q = False
    try:
        poly_p = Poly(p, domain=F)
        if poly_p.is_zero:
            dim = sympy.oo
        else:
            dim = poly_p.degree()
        
        if dim != n:
            neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: p is a polynomial over F",
    "not Q: The factor ring does not have dimension n over F"
]

N_HYP = 2
NEG_Q_INDEX = 2