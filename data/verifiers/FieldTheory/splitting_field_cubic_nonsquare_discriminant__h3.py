import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import x

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, Poly):
            p = witness
        else:
            p = Poly(witness)
            
        if len(p.gens) == 1:
            domain = p.domain
            if domain == ZZ:
                p = p.set_domain(QQ)
                domain = QQ
        else:
            p = None
            domain = None
    except Exception:
        p = None
        domain = None

    try:
        if p is not None:
            is_field = getattr(domain, 'is_Field', False)
            if is_field:
                char = getattr(domain, 'characteristic', 0)
                if callable(char):
                    char = char()
                if char != 2:
                    h1 = True
    except Exception:
        h1 = False

    try:
        if p is not None:
            if p.degree() == 3 and p.is_irreducible:
                h2 = True
    except Exception:
        h2 = False

    try:
        if p is not None:
            if p.degree() == 3 and p.is_irreducible:
                D = p.discriminant()
                x_sym = p.gen
                test_poly = Poly(x_sym**2 - D, x_sym, domain=domain)
                neg_q = not test_poly.is_irreducible
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: f is an irreducible polynomial of degree 3 over F",
    "¬Q: The degree of the splitting field of f over F is not exactly 6"
]

N_HYP = 2
NEG_Q_INDEX = 2