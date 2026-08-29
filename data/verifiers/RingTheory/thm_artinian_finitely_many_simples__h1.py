import sympy
from sympy import ZZ, QQ, RR, CC, Symbol

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

def conditions(witness):
    try:
        neg_q = False
        
        if witness == sympy.ZZ or witness == sympy.S.Integers:
            neg_q = True
        elif witness in (sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
            neg_q = False
        elif isinstance(witness, sympy.polys.domains.PolynomialRing):
            neg_q = True
        elif isinstance(witness, sympy.polys.domains.FractionField):
            neg_q = False
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            neg_q = False
        elif isinstance(witness, str):
            w = witness.lower().replace(" ", "")
            if w in ("z", "zz"):
                neg_q = True
            elif "[x]" in w or "[y]" in w or "[z]" in w:
                neg_q = True
            elif w in ("q", "r", "c", "qq", "rr", "cc"):
                neg_q = False
    except Exception:
        neg_q = False

    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: R has infinitely many isomorphism classes of simple right R-modules"
]

N_HYP = 0
NEG_Q_INDEX = 0