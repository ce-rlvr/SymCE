import sympy
from sympy import Poly, minpoly
from sympy.abc import x

QQ = sympy.QQ

def get_poly(witness):
    if isinstance(witness, (tuple, list)):
        witness = witness[0]
    try:
        if isinstance(witness, Poly):
            return Poly(witness.as_expr(), x, domain='QQ')
        if hasattr(witness, 'has') and witness.has(x):
            return Poly(witness, x, domain='QQ')
        return Poly(minpoly(witness, x), x, domain='QQ')
    except Exception:
        return None

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    f = get_poly(witness)
    if f is not None:
        try:
            h1 = bool(f.is_irreducible)
        except Exception:
            h1 = False
            
        try:
            h2 = bool(f.degree() >= 1)
        except Exception:
            h2 = False
            
        try:
            if h1 and h2:
                G = f.galois_group()
                neg_q = bool(G.order() != f.degree())
        except Exception:
            neg_q = False
            
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field extension of F",
    "H_2: The extension K/F is finite",
    "¬Q: The order of the Galois group Gal(K/F) is not equal to the degree of K over F"
]

N_HYP = 2
NEG_Q_INDEX = 2