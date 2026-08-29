import sympy
from sympy import Poly, isprime
from sympy.abc import x

Z2 = sympy.polys.domains.IntegerModRing(2)
Z3 = sympy.polys.domains.IntegerModRing(3)
Z4 = sympy.polys.domains.IntegerModRing(4)
Z5 = sympy.polys.domains.IntegerModRing(5)
Z6 = sympy.polys.domains.IntegerModRing(6)

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False

    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            expr, mod = witness
            if isinstance(mod, int) and mod > 1:
                p = Poly(expr, x)
                h1 = True
                h2 = p.degree() > 0
                neg_q = not isprime(mod)
                return [h1, h2, neg_q]
    except Exception:
        pass

    domain = None
    try:
        from sympy.polys.rings import PolyElement
        if isinstance(witness, Poly):
            h1 = True
            domain = witness.domain
        elif isinstance(witness, PolyElement):
            h1 = True
            domain = witness.ring.domain
    except Exception:
        pass

    if h1:
        try:
            h2 = witness.degree() > 0
        except Exception:
            h2 = False

    try:
        if h1 and domain is not None:
            while hasattr(domain, 'domain') and not domain.is_Field:
                domain = domain.domain
            
            if domain.is_Field:
                neg_q = False
            elif hasattr(domain, 'mod'):
                neg_q = not isprime(domain.mod)
            elif 'IntegerModRing' in domain.__class__.__name__:
                neg_q = not isprime(domain.mod)
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial over F",
    "H_2: The degree of f is strictly greater than 0",
    "neg_Q: There does not exist an extension field E of F containing a root"
]

N_HYP = 2
NEG_Q_INDEX = 2