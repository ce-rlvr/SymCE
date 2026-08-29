import sympy
from sympy import Poly, Symbol

x = Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness, x)
        h1 = not f.is_zero
    except Exception:
        h1 = False

    try:
        if isinstance(witness, Poly):
            f = witness
        else:
            f = Poly(witness, x)
            
        cont = f.content()
        domain = f.domain
        
        try:
            domain.exquo(domain.one, cont)
            cont_is_unit = True
        except Exception:
            cont_is_unit = False
            
        try:
            is_prim = bool(f.is_primitive)
        except Exception:
            is_prim = cont_is_unit
            
        neg_q = not (cont_is_unit and is_prim)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a non-zero polynomial",
    "¬Q: The content of f(x) is not a unit, or f(x) is not primitive"
]

N_HYP = 1
NEG_Q_INDEX = 1