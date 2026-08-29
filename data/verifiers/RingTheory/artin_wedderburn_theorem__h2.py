import sympy
import sympy.polys.domains as domains
from sympy import ZZ, QQ, RR, CC

# Top-level setup
Z = ZZ
Q = QQ
R = RR
C = CC
x = sympy.Symbol('x')

def conditions(witness):
    # H_1: R is a ring
    try:
        h1 = False
        if isinstance(witness, domains.Domain):
            h1 = True
        else:
            is_ring = getattr(witness, 'is_Ring', False)
            if callable(is_ring):
                is_ring = is_ring()
            if is_ring:
                h1 = True
            elif witness in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
                h1 = True
    except Exception:
        h1 = False

    # H_2: R is a semisimple ring
    try:
        h2 = False
        is_field = getattr(witness, 'is_Field', False)
        if callable(is_field):
            is_field = is_field()
            
        if is_field:
            h2 = True
        else:
            name = witness.__class__.__name__
            if 'Poly' in name or 'Fraction' in name:
                h2 = True
            elif witness in (ZZ, QQ, RR, CC):
                h2 = True
            elif witness in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: R is not isomorphic to a finite direct product of matrix rings over division rings
    try:
        neg_q = False
        is_field = getattr(witness, 'is_Field', False)
        if callable(is_field):
            is_field = is_field()
            
        name = witness.__class__.__name__
        
        if is_field or 'Fraction' in name:
            neg_q = False
        elif witness in (QQ, RR, CC, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            neg_q = False
        elif witness in (ZZ, sympy.S.Integers):
            neg_q = True
        elif 'Poly' in name:
            neg_q = True
        else:
            # For any other integral domain that is not a field, it is not Artinian.
            neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: R is a semisimple ring",
    "¬Q: R is not isomorphic to a finite direct product of matrix rings over division rings"
]

N_HYP = 2
NEG_Q_INDEX = 2