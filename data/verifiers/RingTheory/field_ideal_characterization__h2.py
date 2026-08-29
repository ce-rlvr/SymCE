import sympy
from sympy.polys import domains
from sympy.abc import x

# Top-level setup: named object bindings
Z = domains.ZZ
Q = domains.QQ
R = domains.RR
C = domains.CC
Z_x = domains.ZZ[x]
Q_x = domains.QQ[x]

def conditions(witness) -> list[bool]:
    try:
        # H_1: R is an integral domain
        # Check if it's a standard SymPy set that is an integral domain,
        # or a SymPy polynomial domain (which are integral domains).
        if witness in (sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
            h1 = True
        else:
            h1 = hasattr(witness, 'is_Field') and hasattr(witness, 'get_field')
    except Exception:
        h1 = False

    try:
        # ¬Q: R is not a field
        if witness == sympy.S.Integers:
            neg_q = True
        elif witness in (sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
            neg_q = False
        else:
            neg_q = not bool(witness.is_Field)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: R is not a field"
]

N_HYP = 1
NEG_Q_INDEX = 1