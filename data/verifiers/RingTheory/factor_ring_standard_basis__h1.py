import sympy
from sympy import Poly, Symbol

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        if isinstance(witness, Poly):
            p = witness
        else:
            p = Poly(witness)
        h1 = len(p.gens) == 1 and isinstance(p.gens[0], Symbol)
    except Exception:
        h1 = False
        p = None

    try:
        h2 = False
        if h1 and p is not None:
            h2 = p.degree() > 0
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1 and p is not None:
            domain = p.domain
            lc = p.LC()
            
            def is_unit(dom, el):
                if dom.is_Field:
                    return el != dom.zero
                if hasattr(dom, 'is_unit'):
                    return dom.is_unit(el)
                if dom == sympy.ZZ:
                    return abs(el) == 1
                try:
                    dom.exquo(dom.one, el)
                    return True
                except Exception:
                    return False
            
            # The conclusion fails if the domain is not a field (so it cannot form a vector space)
            # or if the leading coefficient is not a unit (so it doesn't form a basis as a free module)
            neg_q = (not domain.is_Field) or (not is_unit(domain, lc))
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = ["H_1: p is a polynomial", "H_2: degree of p is positive", "¬Q: powers of x do not form a basis"]

N_HYP = 2
NEG_Q_INDEX = 2