import sympy
from sympy import Symbol, Poly, sympify

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        F, p, a = witness
    except Exception:
        return [False, False, False]
    
    try:
        is_field = getattr(F, 'is_Field', False)
        if hasattr(F, 'characteristic'):
            char_attr = F.characteristic
            char = char_attr() if callable(char_attr) else char_attr
        else:
            char = getattr(F, 'char', None)
        h1 = bool(is_field and char == p and p > 0 and isinstance(p, int))
    except Exception:
        h1 = False

    try:
        a_sym = sympify(a)
        if hasattr(F, 'from_sympy'):
            a_F = F.from_sympy(a_sym)
            h2 = a_F is not None
        else:
            _ = F(a)
            h2 = True
    except Exception:
        h2 = False

    try:
        a_sym = sympify(a)
        poly = Poly(x**p - a_sym, x, domain=F)
        is_irred = poly.is_irreducible
        
        if is_irred is False:
            neg_q = True
        elif is_irred is True:
            neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic p > 0",
    "H_2: a in F",
    "¬Q: x^p - a is reducible over F or the degree of its splitting field over F is not p"
]

N_HYP = 2
NEG_Q_INDEX = 2