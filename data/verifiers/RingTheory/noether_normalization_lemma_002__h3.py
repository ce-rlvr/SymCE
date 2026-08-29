import sympy
from sympy import symbols
import sympy.polys.domains as dom

# Top-level setup
x, y, z = symbols('x y z')
QQ = dom.QQ
ZZ = dom.ZZ
RR = dom.RR
CC = dom.CC

CONDITION_LABELS = [
    "H_1: k is a field",
    "H_2: A is a commutative ring",
    "¬Q: A is not an integral extension of any polynomial subring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        k, A = witness
    except Exception:
        return [False, False, False]
        
    # H_1: k is a field
    try:
        h1 = getattr(k, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H_2: A is a commutative ring
    try:
        # In sympy.polys.domains, all Domain objects are commutative rings.
        h2 = isinstance(A, dom.Domain) or getattr(A, 'is_commutative', False)
    except Exception:
        h2 = False
        
    # ¬Q: A is not an integral extension of any polynomial subring
    try:
        neg_q = False
        if h1 and h2:
            # If A is a field, any integral extension over a subring R implies R is a field.
            # Thus the polynomial subring must be a field, which means m = 0.
            # So A must be integral (algebraic) over k.
            # If A is a FractionField over k, it contains transcendental elements,
            # so it is not algebraic over k. Thus it cannot be an integral extension
            # of any polynomial subring.
            if getattr(A, 'is_Field', False):
                if isinstance(A, dom.FractionField):
                    neg_q = True
            if k == dom.QQ and A in (dom.RR, dom.CC):
                neg_q = True
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]